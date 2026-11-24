"""Tests for the robustness of model calls: waiting at a rate limit, repairing an answer that is no valid JSON
(DECISIONS 108). Run with `pytest tests/test_llm.py`."""
import json


import llm as L
from fastapi import HTTPException


class CFG:
    provider, model, api_key, base_url = "rwthgpt", "gpt-6-sol", "k", None


class RateLimitError(Exception):
    """Like the SDKs' error: status 429, optionally with a Retry-After header."""
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.status_code = 429
        self.response = type("R", (), {"headers": {"retry-after": retry_after} if retry_after else {}})()


def provider(*outcomes):
    """A fake _call_llm: raises or returns the outcomes in order."""
    calls = []
    def call(cfg, messages, effort="high"):
        calls.append(messages)
        x = outcomes[len(calls) - 1]
        if isinstance(x, Exception):
            raise x
        return x
    call.calls = calls
    return call


def with_fakes(fake, fn):
    real_call, real_sleep, waits = L._call_llm, L._sleep, []
    L._call_llm, L._sleep = fake, waits.append
    try:
        return fn(), waits
    finally:
        L._call_llm, L._sleep = real_call, real_sleep


def test_the_server_key_is_used_only_when_the_request_has_none(monkeypatch):
    # DECISIONS 139: no key in the code; the server may hold one for RWTHgpt
    from types import SimpleNamespace as NS
    from fastapi.testclient import TestClient
    import app as A
    monkeypatch.delenv("LITMO_RWTHGPT_KEY", raising=False)
    monkeypatch.delenv("LITMO_ANTHROPIC_KEY", raising=False)
    assert L.api_key_of(NS(provider="rwthgpt", api_key="")) == ""
    assert TestClient(A.app).get("/api/config").json() == {"server_keys": {"rwthgpt": False, "anthropic": False}}
    monkeypatch.setenv("LITMO_RWTHGPT_KEY", "server-key")
    assert L.api_key_of(NS(provider="rwthgpt", api_key="")) == "server-key"
    assert L.api_key_of(NS(provider="rwthgpt", api_key="own-key")) == "own-key"
    assert L.api_key_of(NS(provider="anthropic", api_key="")) == ""          # only for the provider it is set for
    r = TestClient(A.app).get("/api/config").json()
    assert r == {"server_keys": {"rwthgpt": True, "anthropic": False}} and "server-key" not in str(r)
    monkeypatch.setenv("LITMO_ANTHROPIC_KEY", "anthropic-key")               # DECISIONS 152
    assert L.api_key_of(NS(provider="anthropic", api_key="")) == "anthropic-key"
    assert L.api_key_of(NS(provider="openai", api_key="")) == ""


def test_the_models_thinking_is_switched_off_only_on_request_and_only_on_an_own_endpoint(monkeypatch):
    # DECISIONS 144: qwen3.8-27b thought past the time limit on the plan call (wine run 7, three attempts of 10 min)
    from types import SimpleNamespace as NS
    import openai
    sent = []
    class Client:
        def __init__(self, **kw):
            self.chat = NS(completions=NS(create=lambda **a: sent.append(a) or NS(
                usage=None, choices=[NS(finish_reason="stop", message=NS(content="{}"))])))
    monkeypatch.setattr(openai, "OpenAI", Client)
    cfg = lambda provider, thinking, base_url="": NS(provider=provider, model="m", api_key="k", base_url=base_url,
                                                    thinking=thinking)
    L._call_llm(cfg("rwthgpt", False), [{"role": "user", "content": "x"}])
    L._call_llm(cfg("rwthgpt", True), [{"role": "user", "content": "x"}])
    L._call_llm(cfg("openai", False, "http://localhost:8001/v1"), [{"role": "user", "content": "x"}])
    L._call_llm(cfg("openai", False), [{"role": "user", "content": "x"}])          # the OpenAI API itself
    L._call_llm(cfg("gemini", False), [{"role": "user", "content": "x"}])
    off = {"chat_template_kwargs": {"enable_thinking": False}}
    assert [a.get("extra_body") for a in sent] == [off, None, off, None, None]


def test_a_custom_endpoint_gets_a_new_user_id_per_call_so_a_cache_cannot_answer(monkeypatch):
    # DECISIONS 145: FhGenie answered an identical request from its cache in 0 s; Evaluate 3x would test three copies
    from types import SimpleNamespace as NS
    import openai
    sent = []
    class Client:
        def __init__(self, **kw):
            self.chat = NS(completions=NS(create=lambda **a: sent.append(a) or NS(
                usage=None, choices=[NS(finish_reason="stop", message=NS(content="{}"))])))
    monkeypatch.setattr(openai, "OpenAI", Client)
    cfg = lambda provider, base_url="": NS(provider=provider, model="m", api_key="k", base_url=base_url)
    for c in (cfg("openai", "https://gateway.example.org/v1"), cfg("openai", "https://gateway.example.org/v1"),
              cfg("openai"), cfg("rwthgpt"), cfg("gemini")):
        L._call_llm(c, [{"role": "user", "content": "same question"}])
    users = [a.get("user") for a in sent]
    assert users[0].startswith("litmo-") and users[1].startswith("litmo-") and users[0] != users[1]
    assert users[2:] == [None, None, None]          # the OpenAI API, KI:connect and Gemini: unchanged


def test_a_rate_limit_is_waited_out():
    limit = RateLimitError("Requests have exceeded token rate limit")
    result, waits = with_fakes(provider(limit, limit, "answer"), lambda: L.call_llm(CFG, []))
    assert result == "answer" and waits == [15, 30]
    # the provider's own waiting time counts; if it is longer than RATE_LIMIT_MAX_WAIT (a quota for the day),
    # waiting does not help: the limit is reported at once
    fake = provider(RateLimitError("slow down", "7"), RateLimitError("come back tomorrow", "900"), "ok")
    try:
        with_fakes(fake, lambda: L.call_llm(CFG, []))
        assert False, "no error"
    except HTTPException as ex:
        assert ex.status_code == 429 and "come back tomorrow" in ex.detail
    assert len(fake.calls) == 2


def test_errors_that_only_mention_a_limit_are_not_waited_for():
    class BadRequest(Exception):
        status_code = 400
    fake = provider(BadRequest("context_length_exceeded: the input exceeds the model's limit"))
    waits = []
    real_call, real_sleep = L._call_llm, L._sleep
    L._call_llm, L._sleep = fake, waits.append
    try:
        L.call_llm(CFG, [])
        assert False, "no error"
    except HTTPException as ex:
        assert ex.status_code == 429                     # reported as before (DECISIONS 81) - but without waiting
    finally:
        L._call_llm, L._sleep = real_call, real_sleep
    assert waits == [] and len(fake.calls) == 1


def test_a_lasting_limit_is_reported_after_the_waits_and_a_used_up_quota_at_once():
    fake = provider(*[RateLimitError("You exceeded your current quota for this period")] * 4)
    try:
        with_fakes(fake, lambda: L.call_llm(CFG, []))
        assert False, "no error"
    except HTTPException as ex:
        assert ex.status_code == 429 and "The model's limit was reached" in ex.detail
    assert len(fake.calls) == 4
    fake = provider(RateLimitError("insufficient_quota: check your plan and billing"))
    try:
        with_fakes(fake, lambda: L.call_llm(CFG, []))
    except HTTPException as ex:
        assert ex.status_code == 429
    assert len(fake.calls) == 1


def test_an_answer_that_is_no_valid_json_is_repaired_once():
    broken = '{"tests": [{"cq": 1, "expected": "the "best" wine"}]}'
    fixed = json.dumps({"tests": [{"cq": 1, "expected": 'the "best" wine'}]})
    fake = provider(broken, fixed)
    result, _ = with_fakes(fake, lambda: L.call_llm_json(CFG, [{"role": "user", "content": "test"}]))
    assert result["tests"][0]["expected"] == 'the "best" wine'
    repair = fake.calls[1]
    assert "Return exactly the same content as valid JSON" in repair[0]["content"]
    assert repair[1]["content"].startswith("Parser error: ") and broken in repair[1]["content"]
    # if the repair fails too, the original error stands - and _run_llm_json reports it as before
    fake = provider(broken, "still {not json")
    try:
        with_fakes(fake, lambda: L._run_llm_json(CFG, []))
        assert False, "no error"
    except HTTPException as ex:
        assert ex.status_code == 500 and "JSONDecodeError" in ex.detail
    # a valid answer needs no second call
    fake = provider('{"a": 1}')
    assert with_fakes(fake, lambda: L.call_llm_json(CFG, []))[0] == {"a": 1} and len(fake.calls) == 1


def test_the_repair_is_counted_as_its_own_step():
    fake = provider("{broken", '{"a": 1}')
    def run():
        with L.track_usage() as log, L.usage_step("Module plan"):
            real = L._call_llm
            def counting(cfg, messages, effort="high"):
                L._record_usage(10, 1)
                return real(cfg, messages, effort)
            L._call_llm = counting
            try:
                L.call_llm_json(CFG, [])
            finally:
                L._call_llm = real
            return [c["step"] for c in log]
    steps, _ = with_fakes(fake, run)
    assert steps == ["Module plan", "Module plan (JSON repair)"]


def test_the_effort_chosen_in_step_1_only_lowers_the_effort_of_a_call(monkeypatch):
    # DECISIONS 154: the choice caps the effort of every Anthropic call; it never raises one (paper cards: medium)
    from types import SimpleNamespace as NS
    import anthropic
    sent = []

    class Stream:
        def __init__(self, **kw):
            sent.append(kw["output_config"]["effort"])
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def get_final_message(self):
            return NS(usage=NS(input_tokens=1, output_tokens=1, cache_read_input_tokens=0, cache_creation_input_tokens=0),
                      stop_reason="end_turn", content=[NS(type="text", text="{}")])

    class Client:
        def __init__(self, **kw):
            self.messages = NS(stream=lambda **k: Stream(**k))
            self.beta = NS(messages=NS(stream=lambda **k: Stream(**k)))

    monkeypatch.setattr(anthropic, "Anthropic", Client)
    msgs = [{"role": "user", "content": "x"}]
    for cap, call, want in (("", "high", "high"), ("medium", "high", "medium"), ("low", "medium", "low"),
                            ("high", "medium", "medium"), ("bogus", "high", "high")):
        L._call_llm(NS(provider="anthropic", api_key="k", model="claude-opus-5-5", effort=cap), msgs, effort=call)
        assert sent[-1] == want, (cap, call)
    L._call_llm(NS(provider="anthropic", api_key="k", model="claude-sonnet-5-5"), msgs)   # no effort field at all
    assert sent[-1] == "high"


def test_other_providers_get_an_effort_only_when_one_is_chosen(monkeypatch):
    # DECISIONS 154: without a choice the model's own default stays (earlier runs stay comparable)
    from types import SimpleNamespace as NS
    import openai
    sent = []

    class Client:
        def __init__(self, **kw):
            def create(**k):
                sent.append(k.get("reasoning_effort"))
                return NS(usage=NS(prompt_tokens=1, completion_tokens=1),
                          choices=[NS(finish_reason="stop", message=NS(content="{}"))])
            self.chat = NS(completions=NS(create=create))

    monkeypatch.setattr(openai, "OpenAI", Client)
    msgs = [{"role": "user", "content": "x"}]
    for cap, call, want in (("", "high", None), ("medium", "high", "medium"), ("low", "medium", "low"),
                            ("high", "medium", "medium")):
        L._call_llm(NS(provider="rwthgpt", api_key="k", model="gpt-6-sol", base_url="", effort=cap), msgs, effort=call)
        assert sent[-1] == want, (cap, call)


def test_batch_results_are_read_from_the_sdk_response_types(monkeypatch):
    # DECISIONS 155: succeeded with text and usage, errors with their message, cancelled without one
    from types import SimpleNamespace as NS
    import anthropic
    from anthropic.types.messages import MessageBatchIndividualResponse as R
    usage = {"input_tokens": 7, "output_tokens": 3, "cache_read_input_tokens": 2, "cache_creation_input_tokens": 0}
    rows = [R.model_validate({"custom_id": "d1", "result": {"type": "succeeded", "message": {
                "id": "m", "type": "message", "role": "assistant", "model": "claude-opus-5-5", "stop_reason": "end_turn",
                "stop_sequence": None, "usage": usage, "content": [{"type": "text", "text": "{\"a\": 1}"}]}}}),
            R.model_validate({"custom_id": "d2", "result": {"type": "errored", "error": {
                "type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}}}),
            R.model_validate({"custom_id": "d3", "result": {"type": "canceled"}})]
    class Client:
        def __init__(self, **kw):
            self.messages = NS(batches=NS(results=lambda bid: iter(rows)))
    monkeypatch.setattr(anthropic, "Anthropic", Client)
    out = L.anthropic_batch_results(NS(provider="anthropic", api_key="k", model="claude-opus-5-5"), "b")
    assert out["d1"] == {"text": "{\"a\": 1}", "stop_reason": "end_turn", "input_tokens": 9, "output_tokens": 3}
    assert out["d2"] == {"type": "errored", "error": "errored: Overloaded"}
    assert out["d3"] == {"type": "canceled", "error": "canceled"}


def test_the_server_key_goes_only_to_the_providers_own_address(monkeypatch):
    # DECISIONS 166 (code review): an empty key field plus any base URL - e.g. from a shared project file - sent the
    # server's key to that host
    from types import SimpleNamespace as NS
    from fastapi import HTTPException
    from fastapi.testclient import TestClient
    import app as A
    monkeypatch.setenv("LITMO_RWTHGPT_KEY", "server-key")
    assert L.api_key_of(NS(provider="rwthgpt", api_key="", base_url="")) == "server-key"
    assert L.api_key_of(NS(provider="rwthgpt", api_key="", base_url="https://chat.kiconnect.nrw/api/v1/")) == "server-key"
    try:
        L.api_key_of(NS(provider="rwthgpt", api_key="", base_url="https://evil.example.org/v1"))
        assert False, "the server key went to another host"
    except HTTPException as ex:
        assert ex.status_code == 400 and "server-key" not in ex.detail and "evil.example.org" in ex.detail
    assert L.api_key_of(NS(provider="rwthgpt", api_key="own", base_url="https://evil.example.org/v1")) == "own"
    r = TestClient(A.app).post("/api/models", json={"provider": "rwthgpt", "model": "m", "api_key": "",
                                                    "base_url": "https://evil.example.org/v1"})
    assert r.status_code == 400 and "server-key" not in r.text
