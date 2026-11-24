"""Verbindungen zwischen den Key Notions (DECISIONS 148): das Gesamtschema von MOMo, das die Module verbindet.

Rueckmeldung zu einer VA-Ontologie (2026-11-05): "die Key Concepts sind noch nicht miteinander verbunden". In VA
7a-7c verband eine Property oder Restriktion nur 1-2 der 45 Paare der zehn Key Notions direkt; die Kernrelationen
haben die obere Schicht als Domain und Range, und jedes Modul verbindet nur seine eigenen Klassen. Hier schlaegt ein
Aufruf in Schritt 7 wenige Verbindungen zwischen den Key Notions selbst vor, das Team gibt sie frei, die Generierung
legt sie als Properties zwischen den Klassen der Key Notions an (und als Restriktion, wo sie fuer jede Instanz
gelten), und die Module verbinden ihre Klassen ueber sie.
"""

from fastapi import HTTPException
from ontology_edits import humanize, IDENT

from project import _class_name, context_block, _cq_text, MOMO_METHOD, named_notions, _norm
from corpus import _inventory_parts, _plain
from vocabularies import _clip
from relations import approved_vocab, core_names, PLAN_LITERATURE_RELATIONS, _within

LINKS_PER_NOTION = (1, 2)          # Umfang des Vorschlags je Key Notion
LINKS_LIMIT_PER_NOTION = 3         # harte Grenze beim Speichern

NOTION_LINKS_SYS = (
    MOMO_METHOD + "\nYou design the KEY NOTION LINKS of a modular ontology before it is generated - in MOMo, the overall "
    "schema diagram that connects the modules: a small set of direct relations between the key notions themselves "
    "(each key notion becomes the main class of its module). Without them each module connects only its own classes "
    "and the key notions stand unconnected side by side. Propose about {lo} to {hi} links - one to two per key "
    "notion - so that every key notion is in at least one link.\n"
    "Rules:\n"
    "1. A link says how instances of one key notion relate to instances of another: subject key notion, relation, "
    "object key notion (two different key notions, exactly as named). Choose the links the use case, the competency "
    "questions{literature} need, in the direction a query follows most naturally.\n"
    "2. Name the relation by its specific meaning (lowerCamelCase verb phrase, such as performs, encodes, records) - "
    "never a catch-all such as isRelatedTo or hasAssociation, and never the name of a core relation itself.\n"
    "3. \"sub_property_of\": the approved core relation whose general meaning the link specialises (performs below a "
    "participation relation, encodes below a representation relation), or empty if none fits.\n"
    "4. \"every\": true only if EVERY instance of the subject has such a relation to some instance of the object - it "
    "becomes a class restriction; false where the relation is possible or typical.\n"
    "5. \"reading\": the link as one plain sentence. \"covers\": the competency questions it serves as \"CQ<number>\""
    "{covers}.\n"
    "6. Give each relation \"labels\" in every language listed under \"Label languages\" in the project conventions "
    "(lowercase verb phrases); English only if none are listed.\n"
    "7. Only links between two key notions; relations between more specific classes are the modules' work.\n"
    'Answer ONLY as JSON: {{"summary":"how the key notions are connected","links":[{{"subject":"KeyNotion",'
    '"name":"relationName","object":"KeyNotion","sub_property_of":"coreRelation or empty","every":false,'
    '"labels":{{"<language code>":"label"}},"description":"...","reading":"...","covers":["CQ1"]}}]}}')


def notion_classes(session) -> list:
    """Die Klassennamen der Key Notions, wie die Planung sie anlegt."""
    return [n for n in (_class_name(x["name"]) for x in named_notions((session.get("momo") or {}).get("key_notions")))
            if n]


def notion_modules(session) -> dict:
    """Klasse der Key Notion -> Name ihres Moduls (die Module heissen wie die Key Notions)."""
    return {_class_name(x["name"]): x["name"] for x in named_notions((session.get("momo") or {}).get("key_notions"))
            if _class_name(x["name"])}


def build_notion_links_prompt(session) -> list:
    momo = session.get("momo") or {}
    notions = named_notions(momo.get("key_notions"))
    n = len(notions)
    lo, hi = max(1, LINKS_PER_NOTION[0] * n), max(2, LINKS_PER_NOTION[1] * n)
    inv, _, _ = _inventory_parts(session)
    lit = (inv or {}).get("relations") or []
    cqs = [_cq_text(c) for c in momo.get("competency_questions") or [] if _cq_text(c)]
    vocab = approved_vocab(session)
    system = NOTION_LINKS_SYS.format(
        lo=lo, hi=hi, literature=" and the relations the literature states" if lit else "",
        covers=" and the relations of the literature as \"subject - relation - object\"" if lit else "")
    lines = ["**Use case:**\n" + (momo.get("use_case") or "(none)"),
             "**Competency questions:**\n" + ("\n".join(f"CQ{i}. {q}" for i, q in enumerate(cqs, 1)) or "(none)"),
             "**Key notions** (class name: description):\n" + "\n".join(
                 f"- {_class_name(x['name'])}" + (f": {_clip(x.get('description'), 200)}" if x.get("description") else "")
                 for x in notions),
             "**Approved core relations** (for \"sub_property_of\"):\n" + ("\n".join(
                 f"- {r['name']}: {r.get('domain') or '(any)'} -> {r.get('range') or '(any)'}" +
                 (f": {_clip(r.get('description'), 120)}" if r.get("description") else "") for r in vocab)
                 or "(none - leave sub_property_of empty)")]
    if lit:
        shown = lit[:PLAN_LITERATURE_RELATIONS]
        lines.append(f"**Relations stated in the literature** ({len(shown)} of {len(lit)}, most sources first):\n" +
                     "\n".join(f"- {r['subject']} - {r['relation']} - {r['object']} ({len(r.get('docs') or [])})"
                               for r in shown))
    return [{"role": "system", "content": system},
            {"role": "user", "content": context_block(session) + "\n\n" + "\n\n".join(lines)}]


def clean_notion_links(links, session) -> list:
    """Prueft die vorgeschlagenen oder vom Team bearbeiteten Verbindungen. Fehler -> HTTP 400 mit Grund."""
    notions = notion_classes(session)
    if len(notions) < 2:
        raise HTTPException(status_code=400, detail="Links need at least two key notions")
    if not isinstance(links, list) or not links:
        raise HTTPException(status_code=400, detail="Add at least one link")
    if len(links) > LINKS_LIMIT_PER_NOTION * len(notions):
        raise HTTPException(status_code=400, detail=f"At most {LINKS_LIMIT_PER_NOTION * len(notions)} links "
                                                    f"({LINKS_LIMIT_PER_NOTION} per key notion)")
    core = core_names(approved_vocab(session))
    out, seen = [], set()
    for x in links:
        x = x if isinstance(x, dict) else {}
        subj, obj, name = (str(x.get(k) or "").strip() for k in ("subject", "object", "name"))
        for side, v in (("subject", subj), ("object", obj)):
            if v not in notions:
                raise HTTPException(status_code=400, detail=f"{name or 'A link'}: the {side} {v or '(empty)'} is not a "
                                                            f"key notion ({', '.join(notions)})")
        if subj == obj:
            raise HTTPException(status_code=400, detail=f"{name}: a link connects two different key notions")
        if not IDENT.match(name):
            raise HTTPException(status_code=400, detail=f"Invalid relation name {name!r}")
        if name in core:
            raise HTTPException(status_code=400, detail=f"{name} is a core relation - name the link by its specific "
                                                        "meaning and put it below the core relation")
        if _norm(name) in {_norm(n) for n in notions}:
            raise HTTPException(status_code=400, detail=f"{name} is already the name of a key notion")
        if _norm(name) in seen:
            raise HTTPException(status_code=400, detail=f"The relation name {name} appears twice")
        seen.add(_norm(name))
        sup = str(x.get("sub_property_of") or "").strip()
        if sup and sup not in core:
            raise HTTPException(status_code=400, detail=f"{name}: {sup} is not an approved core relation")
        labels = x.get("labels") if isinstance(x.get("labels"), dict) else {}
        labels = {str(k).strip().lower(): _plain(v, 80) for k, v in labels.items() if isinstance(v, str) and v.strip()}
        covers = [_plain(c, 120) for c in x.get("covers") or [] if isinstance(c, str) and c.strip()]
        out.append({"subject": subj, "name": name, "object": obj, "sub_property_of": sup,
                    "every": x.get("every") is True, "labels": labels,
                    "description": _plain(x.get("description"), 500), "reading": _plain(x.get("reading"), 300),
                    "covers": covers[:20]})
    return out


def approved_links(session) -> list:
    v = session.get("notion_links") or {}
    return v.get("links") or [] if v.get("status") == "approved" else []


def unlinked_notions(links, notions) -> list:
    used = {x["subject"] for x in links} | {x["object"] for x in links}
    return [n for n in notions if n not in used]


def links_block(links, notion_name) -> str:
    """Die Verbindungen einer Key Notion fuer den Prompt ihres Moduls."""
    cls = _class_name(notion_name)
    mine = [x for x in links if cls in (x["subject"], x["object"])]
    if not mine:
        return ""
    return ("\n\n**Key notion links** (approved by the team; they connect the key notions and exist already - never "
            "define them yourself):\n" + "\n".join(
                f"- {x['subject']} {x['name']} {x['object']}" + (f" (below {x['sub_property_of']})" if x["sub_property_of"] else "")
                + (f": {x['reading']}" if x.get("reading") else "") for x in mine) +
            "\nConnect this module's classes to the other key notions through these relations, or through more specific "
            "properties below them, where the competency questions need it.")


def add_notion_links(onto, links, vocab, langs, notion_modules) -> tuple:
    """Die freigegebenen Verbindungen als Properties zwischen den Klassen der Key Notions, mit der Kernrelation als
    Oberproperty (wenn Domain und Range darin liegen). Wo eine Verbindung fuer jede Instanz gilt, eine Restriktion
    "some" - als Edit-Operation zurueckgegeben, die die Generierung wie die Restriktionen der Module anwendet.
    notion_modules: Klassenname der Key Notion -> Name ihres Moduls. Liefert (onto, Bericht, Restriktionen)."""
    rep = {"links": len(links), "added": [], "restrictions": 0, "existing": [], "missing": [], "below_core_dropped": []}
    restrictions = []
    if not links:
        return onto, rep, restrictions
    langs = list(langs) or ["en"]
    classes = {c["name"] for c in onto.get("classes") or []}
    parents = {c["name"]: c.get("parent") for c in onto.get("classes") or []}
    props = {p["name"]: p for p in onto.get("properties") or []}
    core = {r["name"]: r for r in vocab}
    for x in links:
        label = f"{x['subject']} {x['name']} {x['object']}"
        if x["subject"] not in classes or x["object"] not in classes:
            rep["missing"].append(label)
            continue
        if x["name"] in props:          # ein Modul hat sie trotz der Anweisung selbst angelegt: die bleibt
            rep["existing"].append(label)
        else:
            sup = x["sub_property_of"] or None
            c = core.get(sup) if sup else None
            if sup and not (c and _within(x["subject"], c.get("domain"), parents) and _within(x["object"], c.get("range"), parents)):
                rep["below_core_dropped"].append(f"{label} (not within {sup}'s domain and range)")
                sup = None
            labels = {langs[0]: humanize(x["name"]).lower(), **{l: v for l, v in (x.get("labels") or {}).items() if l in langs}}
            p = {"name": x["name"], "type": "ObjectProperty", "domain": x["subject"], "range": x["object"],
                 "sub_property_of": sup, "inverse_of": None, "characteristics": [], "labels": labels,
                 "description": x.get("description") or x.get("reading") or "",
                 "module": notion_modules.get(x["subject"], x["subject"]), "notion_link": True}
            onto.setdefault("properties", []).append(p)
            props[p["name"]] = p
            rep["added"].append(label)
        if x.get("every"):
            restrictions.append({
                "class": x["subject"], "property": x["name"], "kind": "some", "value": x["object"], "n": None,
                "module": notion_modules.get(x["subject"], x["subject"]),
                "natural_language": x.get("reading") or f"Every {humanize(x['subject']).lower()} {humanize(x['name']).lower()} "
                                                        f"some {humanize(x['object']).lower()}."})
    return onto, rep, restrictions
