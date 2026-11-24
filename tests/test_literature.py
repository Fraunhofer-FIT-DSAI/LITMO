"""Tests for the literature: reading files, grouping the concepts of the paper cards, and linking
classes to them."""
import json
import corpus as C
import generation as G
import llm as L
from helpers import CFG, FakeLLM


def test_literature_files_in_windows_encoding_keep_their_umlauts():
    raw = "Größe;Wert\nÄpfel;1\n".encode("cp1252")
    assert C._decode_text(raw).startswith("Größe") and C._decode_text("\ufeffä".encode("utf-8")) == "ä"
    assert "Größe" in C._profile_csv(raw, "t.csv")


def test_an_abbreviation_is_grouped_under_its_full_form():
    card = lambda term, *syn: {"card": {"concepts": [{"term": term, "synonyms": list(syn), "definition": ""}]}}
    docs = [{"id": "d1", **card("VA", "visual analytics")}, {"id": "d2", **card("visual analytics")},
            {"id": "d3", **card("VA", "visual attention")}, {"id": "d4", **card("visual attention")}]
    groups = {c["label"]: c["papers"] for c in C.group_concepts(docs)}
    assert groups == {"visual analytics": 2, "visual attention": 2}


def test_a_failed_consolidation_leaves_the_name_grouping_unchanged():
    s = {"corpus": {"docs": [{"id": "d1", "status": "done", "card": {"concepts": [
        {"term": "task", "synonyms": [], "definition": "x"}, {"term": "goal", "synonyms": [], "definition": "y"}]}}]}}
    old_apply, old_llm = C.apply_consolidation, L.call_llm
    def broken(concepts, result, doc_ids):
        concepts[0]["sources"] += concepts[1]["sources"]           # half done ...
        raise KeyError("ids")                                       # ... then it fails
    C.apply_consolidation, L.call_llm = broken, FakeLLM({"merges": []})
    try:
        inv = C.build_inventory(s, CFG)
    finally:
        C.apply_consolidation, L.call_llm = old_apply, old_llm
    assert "Consolidation failed" in inv["warning"] and [len(c["sources"]) for c in inv["concepts"]] == [1, 1]


def test_modular_generation_links_classes_to_inventory_concepts():
    inv = {"concepts": [{"id": "c1", "label": "visual encoding", "variants": [], "papers": 2,
                         "sources": [{"doc": "d1", "definition": "maps data", "uri": ""}], "definition": ""}],
           "themes": [], "relations": []}
    session = {"corpus": {"docs": [{"id": "d1", "name": "p.pdf", "card": {"title": "T", "authors": "Doe, J.", "year": "2020"}}],
                          "inventory": inv}, "momo": {"patterns": []}, "context": {}}
    plan = {"modules": [{"name": "Vis", "classes": [{"name": "VisualEncoding", "concepts": ["c1"]},
                                                    {"name": "Forgotten", "concepts": ["c1"]}], "other": []}]}
    results = {"Vis": {"module": {"documentation": "d"}, "classes": [{"name": "VisualEncoding", "sources": ["d1"]}]}}
    onto, _ = G.merge_modules(plan, results, [{"name": "Vis"}], session)
    by = {c["name"]: c for c in onto["classes"]}
    assert by["VisualEncoding"]["inventory_concepts"] == ["visual encoding"]
    assert by["Forgotten"]["inventory_concepts"] == ["visual encoding"]       # fallback class keeps the link too


def _batch_session(client, A, papers):
    """A session with papers whose full texts are on the server (as after an upload)."""
    sid = client.post("/api/session/create").json()["session_id"]
    s = A.sessions[sid]
    s["momo"]["use_case"] = "A shop recommends products."
    for i, text in enumerate(papers, 1):
        doc = {"id": f"d{i}", "name": f"p{i}.pdf", "sha1": str(i), "source_type": "paper", "chars": len(text),
               "pages": 1, "truncated": False, "status": "pending", "error": "", "card": None, "extracted_at": "",
               "usage": None, "mapping": None}
        C._corpus(s)["docs"].append(doc)
        C.corpus_text_path(sid, doc["id"]).parent.mkdir(parents=True, exist_ok=True)
        C.corpus_text_path(sid, doc["id"]).write_text(text, encoding="utf-8")
    return sid, s


def test_paper_cards_as_a_batch_are_sent_together_and_fetched_when_the_batch_has_ended():
    # DECISIONS 155: one batch for all papers without a card; the page asks until it has ended, then the cards are read
    import json
    from fastapi.testclient import TestClient
    import app as A
    sent, state = {}, {"status": "in_progress"}
    card = lambda term, quote: json.dumps({"title": "T", "concepts": [{"term": term, "definition": "d", "quote": quote}]})
    L.anthropic_batch_create = lambda cfg, reqs: sent.update(reqs={cid: (m, e) for cid, m, e in reqs}) or "msgbatch_1"
    L.anthropic_batch_status = lambda cfg, bid: {"status": state["status"], "processing": 0, "succeeded": 2,
                                                 "errored": 1, "canceled": 0, "expired": 0}
    L.anthropic_batch_results = lambda cfg, bid: {
        "d1": {"text": card("product", "a shop sells each product"), "stop_reason": "end_turn", "input_tokens": 100, "output_tokens": 50},
        "d2": {"text": "not json", "stop_reason": "max_tokens", "input_tokens": 10, "output_tokens": 64000},
        "d3": {"type": "errored", "error": "errored: overloaded"}}
    client = TestClient(A.app)
    sid, s = _batch_session(client, A, ["Here a shop sells each product to customers.", "x", "y"])
    s["corpus"]["docs"][2]["status"] = "done"                           # already has a card: not sent again ...
    s["corpus"]["docs"][2]["card"] = {"concepts": []}
    r = client.post("/api/corpus/batch/start", json={"session_id": sid, "llm_config": {**CFG, "provider": "openai"}})
    assert r.status_code == 400                                         # Anthropic only
    r = client.post("/api/corpus/batch/start", json={"session_id": sid, "llm_config": CFG}).json()
    assert set(sent["reqs"]) == {"d1", "d2"} and sent["reqs"]["d1"][1] == C.CARD_EFFORT
    assert r["batch"]["id"] == "msgbatch_1" and [d["status"] for d in r["docs"]] == ["batch", "batch", "done"]
    assert client.post("/api/corpus/batch/start", json={"session_id": sid, "llm_config": CFG}).status_code == 409
    assert client.post("/api/corpus/extract", json={"session_id": sid, "doc_id": "d1", "llm_config": CFG}).status_code == 409
    r = client.post("/api/corpus/batch/check", json={"session_id": sid, "llm_config": CFG}).json()
    assert r["batch"]["counts"]["status"] == "in_progress" and r["docs"][0]["status"] == "batch"
    state["status"] = "ended"
    s["corpus"]["docs"][2]["status"] = "batch"                          # ... a result for it would be ignored: none came
    s["corpus"]["batch"]["doc_ids"].append("d3")
    r = client.post("/api/corpus/batch/check", json={"session_id": sid, "llm_config": CFG}).json()
    d1, d2, d3 = r["docs"]
    assert d1["status"] == "done" and d1["card"]["concepts"][0]["quote_ok"] and d1["usage"]["batch"]
    assert d2["status"] == "error" and "token limit" in d2["error"]     # cut off: an error, not a broken card
    assert d3["status"] == "error" and "overloaded" in d3["error"]
    assert r["batch"] is None and r["last_batch"]["done"] == 1 and r["last_batch"]["failed"] == 2
    assert r["usage"]["input_tokens"] == 110 and s["corpus"]["batch"] is None


def test_a_cancelled_batch_returns_unprocessed_papers_to_pending():
    from fastapi.testclient import TestClient
    import app as A
    L.anthropic_batch_create = lambda cfg, reqs: "msgbatch_2"
    L.anthropic_batch_cancel = lambda cfg, bid: None
    L.anthropic_batch_status = lambda cfg, bid: {"status": "ended", "processing": 0, "succeeded": 0, "errored": 0,
                                                 "canceled": 1, "expired": 0}
    L.anthropic_batch_results = lambda cfg, bid: {"d1": {"type": "canceled", "error": "canceled"}}
    client = TestClient(A.app)
    sid, s = _batch_session(client, A, ["text"])
    client.post("/api/corpus/batch/start", json={"session_id": sid, "llm_config": CFG})
    assert client.post("/api/corpus/batch/cancel", json={"session_id": sid, "llm_config": CFG}).json()["batch"]["canceling"]
    r = client.post("/api/corpus/batch/check", json={"session_id": sid, "llm_config": CFG}).json()
    assert r["docs"][0]["status"] == "pending" and r["batch"] is None


def test_a_second_copy_of_a_paper_is_marked_as_a_possible_duplicate():
    # DECISIONS 157: by the text (preprint and published version) or by the card's title; only a warning
    from fastapi.testclient import TestClient
    import app as A
    import random
    rnd = random.Random(1)
    words = lambda n: " ".join(rnd.choice(["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
                                           "iota", "kappa", "lambda", "omicron", "sigma", "omega"]) + str(rnd.randint(0, 99))
                                for _ in range(n))
    paper = words(3000)
    preprint = "Preprint. Under review. " + paper[: int(len(paper) * 0.8)] + " " + words(300)
    client = TestClient(A.app)
    sid, s = _batch_session(client, A, [paper, words(3000), preprint, words(3000), words(3000)])
    docs = s["corpus"]["docs"]
    docs[3]["card"] = {"title": "A Task by Data Type Taxonomy", "concepts": []}
    docs[4]["card"] = {"title": "A task by data-type taxonomy", "concepts": []}
    pairs = C.mark_duplicates(sid, s["corpus"])
    assert [(p["doc"], p["duplicate_of"]) for p in pairs] == [("d3", "d1"), ("d5", "d4")]
    assert "text is the same" in docs[2]["duplicate_of"]["why"] and docs[4]["duplicate_of"]["why"] == "same title"
    assert "duplicate_of" not in docs[0] and "duplicate_of" not in docs[1]
    docs[4]["card"]["title"] = "Something else entirely"                 # marks are recomputed, not kept
    assert len(C.mark_duplicates(sid, s["corpus"])) == 1 and "duplicate_of" not in docs[4]
    A.build_inventory = lambda session, cfg: {"concepts": [], "doc_ids": []}
    r = client.post("/api/corpus/inventory", json={"session_id": sid, "llm_config": CFG}).json()
    assert r["inventory"]["duplicates"][0]["doc"] == "d3" and r["docs"][2]["duplicate_of"]["id"] == "d1"


def test_two_batch_starts_at_the_same_time_create_only_one_paid_batch():
    # DECISIONS 166 (code review): both requests saw "no batch" before either had stored its own; one paid batch
    # was lost from the project
    import threading, time
    from fastapi.testclient import TestClient
    import app as A
    created = []
    def create(cfg, reqs):
        created.append(1)
        time.sleep(0.3)                                       # the provider takes a moment
        return f"msgbatch_{len(created)}"
    L.anthropic_batch_create = create
    client = TestClient(A.app)
    sid, s = _batch_session(client, A, ["a text", "b text"])
    codes = []
    def start():
        codes.append(client.post("/api/corpus/batch/start", json={"session_id": sid, "llm_config": CFG}).status_code)
    threads = [threading.Thread(target=start) for _ in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert sorted(codes) == [200, 409] and len(created) == 1 and s["corpus"]["batch"]["id"] == "msgbatch_1"


def test_batch_starts_of_different_projects_do_not_wait_for_each_other():
    # DECISIONS 167 (second review): the lock was process-wide and held across the call to the provider
    import threading, time
    from fastapi.testclient import TestClient
    import app as A
    created = []
    def create(cfg, reqs):
        created.append(time.time())
        time.sleep(0.4)
        return f"msgbatch_{len(created)}"
    L.anthropic_batch_create = create
    client = TestClient(A.app)
    sids = [_batch_session(client, A, ["a text"])[0] for _ in range(2)]
    codes = []
    threads = [threading.Thread(target=lambda sid=sid: codes.append(client.post(
        "/api/corpus/batch/start", json={"session_id": sid, "llm_config": CFG}).status_code)) for sid in sids]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert codes == [200, 200] and abs(created[0] - created[1]) < 0.3      # both at once, not one after the other


def test_batch_check_and_cancel_refuse_other_providers():
    # DECISIONS 168 (code review 2026-11-11): with an empty key field the server's KI:connect key would go to Anthropic
    from fastapi.testclient import TestClient
    import app as A
    client = TestClient(A.app)
    sid, s = _batch_session(client, A, ["a text"])
    s["corpus"]["batch"] = {"id": "msgbatch_x", "doc_ids": [], "counts": None, "canceling": False}
    other = {**CFG, "provider": "rwthgpt", "api_key": ""}
    for path in ("/api/corpus/batch/check", "/api/corpus/batch/cancel"):
        r = client.post(path, json={"session_id": sid, "llm_config": other})
        assert r.status_code == 400 and "Anthropic" in r.text


def _two_stage_session():
    card = lambda *terms: {"status": "done", "card": {"concepts": [
        {"term": t, "synonyms": [], "definition": f"{t} as defined here"} for t in terms]}}
    return {"momo": {"use_case": "test"}, "corpus": {"docs": [
        {"id": "d1", "name": "p1", **card("task", "goal", "aim", "chart")},
        {"id": "d2", "name": "p2", **card("task", "goal")}, {"id": "d3", "name": "p3", **card("aim", "task")}]}}


def _ids(messages):
    import re
    return dict((label, cid) for cid, label in re.findall(r"^(c\d+) \| ([^|(]+?)[ |(]", messages[-1]["content"], re.M))


def _fake_two_stage(fail_detail_of=None, truncate=()):
    """Answers by pass: the first merges goal and aim and puts task and goal into one theme, the second gives a
    conflict on task and a definition for goal. `truncate` names the passes cut off at the output limit."""
    calls = []
    def fake(cfg, messages, effort="high"):
        sys_prompt, ids = messages[0]["content"], _ids(messages)
        stage = "names" if "FIRST pass" in sys_prompt else "detail" if "SECOND pass" in sys_prompt else "single"
        calls.append((stage, sorted(ids)))
        L._record_usage(100, 10)
        if stage in truncate:
            raise L.LLMTruncatedError(32000)
        if stage == "names":
            return json.dumps({"merges": [{"ids": [ids["goal"], ids["aim"]], "label": "goal"}],
                               "themes": [{"name": "Work", "description": "d", "concepts": [ids["task"], ids["goal"]]}]})
        if fail_detail_of and fail_detail_of in ids:
            raise RuntimeError("server down")
        out = {"merges": [], "conflicts": [], "definitions": []}
        if "task" in ids:
            out["conflicts"] = [{"concept": ids["task"], "issue": "i", "positions": [
                {"view": "a step", "docs": ["d1"]}, {"view": "a goal", "docs": ["d2", "d3"]}]}]
        if "goal" in ids:
            out["definitions"] = [{"concept": ids["goal"], "definition": "What a user wants."}]
        return json.dumps(out)
    return fake, calls


def _with(fake, **consts):
    old = {k: getattr(C, k) for k in consts}
    old_llm = L.call_llm
    for k, v in consts.items():
        setattr(C, k, v)
    L.call_llm = fake
    return old, old_llm


def _restore(old, old_llm):
    for k, v in old.items():
        setattr(C, k, v)
    L.call_llm = old_llm


def test_a_large_inventory_is_consolidated_in_two_passes():
    fake, calls = _fake_two_stage()
    old = _with(fake, INVENTORY_TWO_STAGE_MIN=0)
    try:
        inv = C.build_inventory(_two_stage_session(), CFG)
    finally:
        _restore(*old)
    by = {c["label"]: c for c in inv["concepts"]}
    assert inv["consolidated"] and inv["consolidation"]["mode"] == "two-stage" and not inv["warning"]
    assert [s for s, _ in calls] == ["names", "detail"]
    assert calls[1][1] == ["goal", "task"]                        # the second pass sees only multi-source concepts
    assert by["goal"]["papers"] == 3 and "aim" in by["goal"]["variants"] and "aim" not in by
    assert by["goal"]["definition"] == "What a user wants." and by["task"]["conflict"]
    assert [t["name"] for t in inv["themes"]] == ["Work"]
    label = {c["id"]: c["label"] for c in inv["concepts"]}
    assert [label[i] for i in inv["themes"][0]["concepts"]] == ["task", "goal"]      # the first pass's order


def test_a_failed_part_of_the_second_pass_keeps_the_rest_and_says_so():
    fake, calls = _fake_two_stage(fail_detail_of="task")
    old = _with(fake, INVENTORY_TWO_STAGE_MIN=0, INVENTORY_BATCH=1)
    try:
        inv = C.build_inventory(_two_stage_session(), CFG)
    finally:
        _restore(*old)
    by = {c["label"]: c for c in inv["concepts"]}
    assert inv["consolidated"] and inv["consolidation"]["parts"] == 2 and inv["consolidation"]["failed_parts"] == 1
    assert "1 of 2 parts failed" in inv["warning"] and "server down" in inv["warning"]
    assert by["goal"]["definition"] and not by["task"]["conflict"] and not inv["conflicts"]


def test_a_single_call_cut_off_at_the_limit_falls_back_to_two_passes():
    fake, calls = _fake_two_stage(truncate=("single",))
    old = _with(fake)
    try:
        inv = C.build_inventory(_two_stage_session(), CFG)
    finally:
        _restore(*old)
    assert [s for s, _ in calls] == ["single", "names", "detail"]
    assert inv["consolidated"] and "32000 tokens" in inv["consolidation"]["note"] and not inv["warning"]


def test_a_cut_off_first_pass_names_the_limit_in_the_warning():
    fake, calls = _fake_two_stage(truncate=("names",))
    old = _with(fake, INVENTORY_TWO_STAGE_MIN=0)
    try:
        inv = C.build_inventory(_two_stage_session(), CFG)
    finally:
        _restore(*old)
    assert not inv["consolidated"] and "output limit of 32000 tokens" in inv["warning"]
    assert "aim" in {c["label"] for c in inv["concepts"]}         # name grouping unchanged
