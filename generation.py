"""Generierung: Planung, Module, Zusammenfuehrung."""

import contextvars, re
from fastapi import HTTPException

import llm
from llm import usage_step
from project import (_class_name, decision_store, nth, declined_relations, relation_key, _cq_text, _ctx, find_pattern, label_languages, MOMO_METHOD, named_notions, _norm,
                     pattern_template_text, session_prefixes)
from corpus import _concept_definition, concept_key, doc_citation, _existing_terms, _inventory_parts, _plain, source_type
from vocabularies import (align_candidates, align_listing, class_candidates, known_prefixes, relevant_vocab_terms,
                          reuse_block, session_vocab)
from ontology_edits import apply_edits, restriction_label
from notion_links import add_notion_links, approved_links, links_block, notion_modules
from editing import OOPS_GUIDANCE
from definitions import apply_to_plan, decided_classes
from ontology_evaluation import _ancestors, central_ids, hierarchy_coverage, inverse_conflicts, _STOP
from upper import ensure_upper_layer, remove_unused_upper, upper_layer_of, use_upper_layer
from relations import (approved_vocab, check_core_relations, core_names, core_properties, core_relation_block,
                       CORE_MODULE, ensure_core_module)

# ── Generierung Modul fuer Modul (ein Weg fuer alle Projekte, DECISIONS 84) ────
# Ein einzelner Aufruf kann weder hunderte Begriffe samt Definitionen lesen noch hunderte Klassen schreiben
# (Ausgabelimit). Deshalb: 1. ein Planungsaufruf legt die Klassen jedes Moduls (= Key Notion) und deren Namen fest -
# mit Literatur aus den Begriffen des Inventars, ohne Literatur aus Use Case, Kompetenzfragen und Daten; ohne Key
# Notions schlaegt er auch die Module vor; 2. je Modul ein Aufruf mit nur dessen Material, parallel; 3. die Module
# werden deterministisch zusammengefuehrt. Die Klassennamen aller Module sind vorab bekannt, daher kann jedes Modul
# Klassen anderer Module als Domain/Range verwenden.
MODULE_WORKERS = 4
PLAN_LISTING_LIMIT = 150_000
MODULE_SOURCE_DEFS = 6
DATA_PROMPT_LIMIT = 20_000      # Zeichen der Datenvorschau in Plan- und Modul-Prompts

PLAN_SYS = (MOMO_METHOD + "\nYou plan the MODULES and CLASSES of a modular ontology. {modules}\n"
            "Rules:\n"
            "1. Select what belongs in the ontology given the use case, the project context, the competency "
            "questions and the data: {select}\n"
            "2. One class per notion: notions with the same meaning become ONE class{ids}.\n"
            "3. A notion that is better modeled as a property (a relation or an attribute) or as an individual (a "
            "single named thing) is not a class: list it under 'other' of its module, with how to model it.\n"
            "4. Class names UpperCamelCase, singular and specific, unique across the whole ontology. Give every "
            "class a one-sentence note on what it stands for.\n"
            "5. Size: {size}. Do not list helper classes that no notion names and the hierarchy does not need - the "
            "module step adds those.\n"
            "6. Every module gets classes; the module's key notion itself is one of them.\n"
            "7. A concept listed under 'Decided definitions' in the project context becomes exactly the class(es) "
            "named there, with those names - a split concept becomes all of its classes.\n"
            "8. Hierarchy: give every class its \"parent\" - the planned class (in any module) of which it is a kind, "
            "or null for a top class. Ask for each class whether it is a kind of something else the ontology needs. "
            "Where several classes are kinds of one broader notion the use case needs (kinds of places, of products, "
            "of events, of roles), plan that broader class as well and put them below it. A key notion may be below "
            "another class. A value set (such as colours or categories) can be one class with individuals instead of "
            "subclasses. Choose ONE of the two per distinction - subclasses or a value set, never both for the same "
            "distinction (e.g. not kinds of products by size AND a size value set). A class whose members are "
            "categories, types or grades OF something is not a kind of that thing: never place it below it (a "
            "category of products is not a product). No cycles.{upper}{literature}\n"
            'Answer ONLY as JSON: {{"ontology_name":"...","summary":"one paragraph","license":"license URI",{declined}'
            '"modules":[{{"name":"{module_name}","description":"one sentence",'
            '"classes":[{{"name":"ClassName","parent":"PlannedClass or null",{concepts}"note":"what it stands for"}}],'
            '"other":[{{{other}"as":"property|individual","hint":"how to model it"}}]}}]}}')

# Hierarchie aus der Literatur in der Planung (PLAN.md Phase 3d, DECISIONS 103): die Oberbegriffe und Taxonomien der
# Quellen gehen in den Plan, statt erst nach der Generierung von "Build hierarchy" nachgetragen zu werden.
LITERATURE_HIERARCHY_RULE = (
    " The listing gives each concept's broader terms as the sources state them (concept ids where the broader term is "
    "a concept of the inventory), and the taxonomies the sources use. Use them for \"parent\": a planned class whose "
    "concept the sources place below another planned concept gets that class as its parent; the categories of a "
    "taxonomy go below its root where both are planned. The sources sometimes say 'broader' loosely - for a part, a "
    "phase, a related topic: leave such a relation out and list it under \"hierarchy_declined\" with the reason "
    "(by planned class names where both are planned).")

# Jeder zentrale Begriff geplant oder begruendet ausgeschlossen (PLAN.md Phase 3e, DECISIONS 104): vorher holte "Add
# missing central concepts" sie nach der Generierung nach (VA-Projekt: rund 1 M Eingabe-Tokens).
CENTRAL_RULE = (" Every concept with 2 or more sources is CENTRAL and must be accounted for: in a class's "
                "\"concepts\", under \"other\", or under \"excluded\" with the reason (out of scope for the use case, "
                "specific to one paper's method, generic research vocabulary, or the same as another concept). A "
                "category of one of the literature's taxonomies, or a concept a competency question names, is not "
                "excluded for being narrow, specific or part of one framework: plan it as a subclass, or as an "
                "individual of the class for its taxonomy where the categories are fine-grained values.")

# Obere Schicht in der Planung (PLAN.md Phase 3b, DECISIONS 97): die obersten geplanten Klassen kommen unter die
# Klasse der Schicht, deren Art sie sind - vorher besorgte das die Aktion "Group root classes" nach der Generierung.
UPPER_RULE = (" The UPPER LAYER listed in the task groups all classes by the kind of thing they are: a class without a "
              "planned parent gets as \"parent\" the upper class it is a kind of (by its exact name); leave it null "
              "only if none fits. Do not plan the upper classes themselves.")

def _plan_system(inv, fixed_modules, upper=False) -> str:
    if inv:
        select = ("concepts of the concept inventory supported by several sources, the members of the themes, and "
                  "every concept the competency questions need. Leave out concepts that are out of scope, generic "
                  "research vocabulary, or a single paper's METHOD: what one paper uses or builds to study the domain "
                  "- its own system, algorithm, model, data structure or representation, dataset, metric or study "
                  "setup (e.g. the graph or database a paper builds, a vector or embedding it computes, its scoring "
                  "formula). Ask whether the use case needs the thing itself or only the paper that built it; the "
                  "list of sources says what each paper is about. Exclude such a concept under \"excluded\" "
                  "(\"specific to one paper's method\") even where a theme of the corpus groups it - unless the use "
                  "case is about such systems or methods. Judge each concept, not the paper: what a method paper "
                  "says ABOUT the domain - its rules, categories, characteristics and descriptors of the domain's "
                  "things - is domain knowledge and stays; only what the paper builds or computes is its method.")
        ids, size = " (list all their ids)", f"typically 8-40 classes per module, about {plan_target(inv)} classes in total"
        concepts, other = '"concepts":["c1","c7"],', '"concepts":["c9"],'
    else:
        # Ohne Literatur plante das Modell nur die Woerter der Fragen (Wein-Lauf 1: 6 Klassen, examples/wine/RUNS.md).
        select = ("the things the competency questions ask about and return, the key notions, and what the data "
                  "contain (tables, columns, entities). There is no literature, so also add the notions a domain "
                  "expert would expect for this use case although no question names them: kinds and subkinds, parts, "
                  "participants, places and times, and value sets (types, grades, categories) that the questions "
                  "compare or filter by. Things the questions name individually (a particular place, product, "
                  "category or person) are individuals of a planned class: list each under 'other' as an "
                  "individual. Leave out what the use case does not need.")
        ids, size, concepts, other = "", "typically 5-15 classes per module", "", '"term":"the notion",'
    modules = ("The modules are fixed: one per key notion; use their names exactly as given." if fixed_modules else
               "Divide the domain into 3-8 modules - the key notions in the sense of MOMo, each a coherent part of "
               "the domain (such as products, places or processes) - and name each with an UpperCamelCase noun.")
    return PLAN_SYS.format(modules=modules, select=select, ids=ids, size=size, concepts=concepts, other=other,
                           module_name="exact module name as given" if fixed_modules else "ModuleName",
                           upper=UPPER_RULE if upper else "",
                           literature=LITERATURE_HIERARCHY_RULE + CENTRAL_RULE if inv else "",
                           declined='"hierarchy_declined":[{"narrower":"Class or concept","broader":"Class or concept '
                                    'or taxonomy name","reason":"why it is not a kind of"}],'
                                    '"excluded":[{"concept":"c12","reason":"why it is not modelled"}],' if inv else "")

def _upper_names(session) -> list:
    return [x["name"] for x in upper_layer_of(session)] if use_upper_layer(session) else []

def _upper_lines(layer) -> str:
    return "\n".join(f"- {x['name']}" + (f" (below {x['parent']})" if x.get("parent") else "") + f": {x['definition']}"
                     for x in layer)

MODULE_SYS = ("You are an expert ontology engineer working according to the MOMo (Modular Ontology Modeling) "
              "methodology. You build ONE MODULE of a larger modular ontology. The module's classes have been planned: "
              "keep the planned class names EXACTLY; you may add a few classes the module's structure needs (e.g. from "
              "its design pattern) - but not classes for what a source uses to study the domain (its data "
              "structures, representations, algorithms or datasets, such as graphs, nodes, vectors or embeddings), "
              "unless the use case is about them. Keep a planned superclass (\"below: X\") as the class's parent, or put a class of "
              "your own between them. A class of categories, types or grades of X is never a subclass of X. Do not add "
              "a value set for a distinction the planned subclasses already make, or subclasses for one a planned "
              "value set makes. Where "
              "the project has a literature corpus, each planned class comes with the "
              "concept material from the sources: their definitions (with source ids such as d1a2b3c4d5) and terms of "
              "existing ontologies; otherwise with a note on what it stands for.\n"
              "- Write each class description from the sources' definitions; where they differ, follow the project "
              "context, otherwise the majority of sources. Without sources, write it from the note, the use case and "
              "the competency questions. A class with a DECIDED DEFINITION gets exactly that text "
              "as its description - the team decided it.\n"
              "- Set \"sources\" of a class to the ids of the sources its definition is based on, and \"see_also\" to "
              "the URIs of existing-ontology terms with the same meaning (only ids and URIs given to you).\n"
              "- Model the module's properties (object and datatype) so that the competency questions can be "
              "answered, and so that the data described below fit. An ObjectProperty may use a class of ANOTHER "
              "module (listed by name) as domain or range - never define those classes yourself.\n"
              "- Model the notions listed under 'other' as properties or individuals as hinted, and give the property "
              "or individual you create for one of them \"concepts\": the ids in brackets before it.\n"
              "- Use the class hierarchy (parent) for the broader/narrower relations the sources state.\n"
              "- Events and changes: where a competency question asks what an action or event changes, what someone "
              "does in it, how something changes over time, or how to trace a result back through the steps that "
              "led to it, model the event so that a query can return exactly that: who takes part and in which "
              "role, what it acts on, WHAT it changes - the state, content or value before and after, or what it "
              "adds, removes or alters - what it results in, and the ORDER of events, linking a result to the event "
              "that produced it. For each of these connections, first use a core relation with that meaning (e.g. "
              "one for states, changes, input and output, or temporal order): directly, or as \"sub_property_of\" "
              "of a more specific relation such as the state before and the state after. Create a relation of the "
              "module without such a parent only where no core relation has that meaning (for the order also a time "
              "stamp). Recording only that an event happened does not answer such a question.\n"
              "- Write the KEY RESTRICTIONS of the module's classes under \"restrictions\": what holds for EVERY "
              "instance of a class. some: every A has at least one p to a B; only: all p values of an A are B; min, "
              "max, exactly: a number n of p values that are B. Use a core relation or a property of this module; the "
              "class must lie within the property's domain and the value within its range. Where a core relation "
              "connects two classes of this module, a restriction states that pair - no new property is needed for "
              "it. Write some only where every instance has such a relation, not where it is merely typical; only "
              "and numbers only where the domain or a competency question requires them. When unsure, leave it "
              "out.\n"
              "- A DatatypeProperty's range is an OWL 2 datatype: xsd:string, rdf:langString, xsd:boolean, xsd:integer, "
              "xsd:nonNegativeInteger, xsd:decimal, xsd:double, xsd:dateTime or xsd:anyURI. xsd:date, xsd:gYear, "
              "xsd:duration and the other XML Schema types are not part of OWL 2 DL: write a year as xsd:integer and a "
              "date as xsd:dateTime.\n"
              "Naming: classes UpperCamelCase, singular and specific; properties lowerCamelCase, directional and "
              "verb-based. Give a property an inverse only where a competency question or the data need both "
              "directions - a query can follow a property backwards. Prefer SCOPED over global cardinality axioms. Document the "
              "module: documentation is a primary part of the ontology, not an afterthought.\n"
              + OOPS_GUIDANCE +
              'Give every class, property and individual a label for EACH language listed under "Label languages" '
              "in the project conventions, and write descriptions in the first of those languages.\n"
              "A PROJECT CONTEXT agreed by the team may follow: it overrides your defaults. Items marked [confirm] "
              "there are unconfirmed assumptions - follow them unless they contradict the use case.\n"
              'Answer ONLY as JSON: {"module":{"name":"...","key_notion":"...","documentation":"prose describing this module"},'
              '"classes":[{"name":"...","labels":{"<language code>":"label"},"description":"...","parent":null,'
              '"sources":["d..."],"see_also":["uri"]}],'
              '"properties":[{"name":"...","type":"ObjectProperty|DatatypeProperty","domain":"...","range":"...",'
              '"inverse_of":"name or null","sub_property_of":"name, prefix:term or null","labels":{"<language code>":"label"},"description":"...",'
              '"concepts":["c12"]}],'
              '"individuals":[{"name":"...","class":"...","labels":{"<language code>":"label"},"concepts":["c13"]}],'
              '"axioms":[{"type":"DisjointClasses|EquivalentClasses|SubClassOf","classes":["A","B"],"scoped":true|false,'
              '"natural_language":"plain English reading"}],'
              '"restrictions":[{"class":"A","property":"p","kind":"some|only|min|max|exactly","value":"B or xsd:...",'
              '"n":"number for min/max/exactly","natural_language":"plain English reading"}]}')

def _theme_of(inv) -> dict:
    return {cid: t["name"] for t in inv.get("themes") or [] for cid in t["concepts"]}

def plan_target(inv) -> int:
    themed = set(_theme_of(inv))
    relevant = len(central_ids(inv) | themed)
    return max(40, min(300, relevant))

def _concept_ids(inv) -> dict:
    """Begriffsschluessel (Label und Varianten) -> Begriffs-ID, um Oberbegriffe und Kategorien als IDs zu zeigen."""
    out = {}
    for c in inv["concepts"]:
        for v in [c["label"], *c.get("variants", [])]:
            out.setdefault(concept_key(v), c["id"])
    return out

def _broader_of(c, ids, limit=3) -> str:
    """Die Oberbegriffe, die die Quellen fuer einen Begriff nennen, die haeufigsten zuerst - als ID, wo sie selbst
    Begriffe des Inventars sind."""
    counts = {}
    for s in c.get("sources") or []:
        b = _plain(s.get("broader"), 60)
        if b:
            ref = ids.get(concept_key(b)) or f"'{b}'"
            if ref != c["id"]:
                counts[ref] = counts.get(ref, 0) + 1
    return ", ".join(r for r, _ in sorted(counts.items(), key=lambda x: -x[1])[:limit])

TAXONOMY_BLOCK_LIMIT = 25_000

def _taxonomy_block(inv) -> str:
    """Taxonomien der Quellen, deren Wurzel oder mindestens zwei Kategorien Begriffe des Inventars sind (wie bei
    "Build hierarchy"), mit den Kategorien als IDs - die meisten zugeordneten Kategorien zuerst."""
    ids, rows, seen = _concept_ids(inv), [], set()
    for t in inv.get("taxonomies") or []:
        name, cats = _plain(t.get("name"), 100), [_plain(x, 60) for x in t.get("categories") or []]
        root = ids.get(concept_key(name))
        mapped = [(x, ids.get(concept_key(x.split(":")[-1]))) for x in cats if x]
        hits = sum(1 for _, i in mapped if i)
        same = (root, frozenset(i for _, i in mapped if i))     # dieselbe Taxonomie aus einem anderen Paper
        if not name or concept_key(name) in seen or same in seen or not (hits >= 2 or (root and len(cats) >= 3)):
            continue
        seen.update({concept_key(name), same})
        rows.append((hits, f"- '{name}'" + (f" ({root})" if root else "") + ": " +
                     "; ".join(f"{x} ({i})" if i else x for x, i in mapped[:20])))
    out, size = [], 0
    for _, line in sorted(rows, key=lambda r: -r[0]):
        if size + len(line) > TAXONOMY_BLOCK_LIMIT:
            break
        out.append(line)
        size += len(line) + 1
    return "\n".join(out)

def _paper_ids(docs) -> dict:
    """Kurze Namen der Quellen fuer den Plan (p1, p2, ...) - die Dokument-IDs sind lang und sagen nichts."""
    return {d: f"p{i}" for i, d in enumerate(docs or {}, 1)}

def _sources_block(docs) -> str:
    """Wovon jede Quelle handelt (DECISIONS 140): ohne das sieht der Plan nicht, ob ein Begriff mit einer Quelle die
    Domaene beschreibt oder das, was ein Paper zu ihrer Untersuchung baut (Wein: WineGraph, aroma vector)."""
    pids, out = _paper_ids(docs), []
    for d, doc in (docs or {}).items():
        card = doc.get("card") or {}
        kind = card.get("contribution") if source_type(doc) == "paper" else source_type(doc)
        out.append(f"- {pids[d]} = {doc_citation(doc)}" + (f" ({kind})" if kind else "") +
                   (f": {_plain(card.get('scope'), 200)}" if card.get("scope") else ""))
    return "\n".join(out)

def _plan_listing(inv, docs) -> str:
    theme = _theme_of(inv)
    ids = _concept_ids(inv)
    pids = _paper_ids(docs)
    def build(def_limit):
        out = []
        for c in inv["concepts"]:
            line = f"{c['id']} | {c['label']} | {c['papers']}"
            only = {s["doc"] for s in c.get("sources") or []}
            if c["papers"] == 1 and len(only) == 1 and next(iter(only)) in pids:
                line += f" ({pids[next(iter(only))]})"
            if c["id"] in theme:
                line += f" | theme: {theme[c['id']]}"
            broader = _broader_of(c, ids)
            if broader:
                line += f" | broader: {broader}"
            if _existing_terms(c, docs):
                line += " | in existing ontology"
            if def_limit and (c["papers"] > 1 or c["id"] in theme):
                d = _concept_definition(c)
                if d:
                    line += f" | {d[:def_limit]}"
            out.append(line)
        return "\n".join(out)
    for limit in (200, 120, 60, 0):
        text = build(limit)
        if len(text) <= PLAN_LISTING_LIMIT:
            return text
    return text[:PLAN_LISTING_LIMIT] + "\n[... list truncated]"

def _use_case(session, use_case=None) -> str:
    return (use_case or (session.get("momo") or {}).get("use_case") or "(none)").strip()

def _data_block(session) -> str:
    """Die Datenvorschau (Tabellenprofile, RDF-Zusammenfassungen, Auszuege) - ohne Literatur oft das wichtigste
    Material neben den Kompetenzfragen."""
    data = (session.get("data_preview") or "").strip()
    if not data:
        return ""
    if len(data) > DATA_PROMPT_LIMIT:
        data = data[:DATA_PROMPT_LIMIT] + "\n[... data preview truncated]"
    return "\n\n**Data the ontology has to describe (profiles and excerpts of the uploaded files):**\n" + data

def build_plan_prompt(session, notions, context, use_case=None):
    inv, docs, _ = _inventory_parts(session)
    momo = session.get("momo") or {}
    cqs = "\n".join("- " + _cq_text(c) for c in momo.get("competency_questions") or [] if _cq_text(c)) or "(none)"
    mods = "\n".join(f"- {n['name']}" + (f": {n['description']}" if n.get("description") else "") for n in notions)
    task = ("**Use case:**\n" + _use_case(session, use_case) + _ctx(context) +
            "\n\n**Competency questions:**\n" + cqs +
            ("\n\n**Modules (key notions):**\n" + mods if notions else "") + _data_block(session))
    if inv:
        themes = "\n".join(f"- {t['name']}: {t['description']}" for t in inv.get("themes") or []) or "(none)"
        taxonomies = _taxonomy_block(inv)
        task += ("\n\n**Sources** (what each is about):\n" + _sources_block(docs) +
                 "\n\n**Themes of the corpus:**\n" + themes +
                 "\n\n**Concept inventory** (id | label | number of sources, with the source where it is one | theme | "
                 "broader terms | definition):\n" +
                 _plan_listing(inv, docs) +
                 ("\n\n**Taxonomies in the sources** (name (concept id of the root): categories (concept ids)):\n" +
                  taxonomies if taxonomies else ""))
    upper = use_upper_layer(session)
    if upper:
        task += ("\n\n**Upper layer** (exists in the ontology; the top classes go below these):\n" +
                 _upper_lines(upper_layer_of(session)))
    task += "\n\nPlan the classes of every module." if notions else "\n\nPlan the modules and their classes."
    return [{"role": "system", "content": _plan_system(inv, bool(notions), upper)},
            {"role": "user", "content": task}]

def clean_plan(result, notions, inv, upper_names=()) -> dict:
    """Nur bekannte Module (bei vorgegebenen Key Notions) und Begriffe; Klassennamen eindeutig ueber alle Module.
    Ohne Key Notions uebernimmt der Plan die Module, die das Modell vorschlaegt."""
    by_id = {c["id"]: c for c in inv["concepts"]} if inv else {}
    r = result if isinstance(result, dict) else {}
    proposed = [m for m in r.get("modules") or [] if isinstance(m, dict)]
    if not notions:   # Module aus dem Plan: Namen wie Key Notions, eindeutig
        notions, seen = [], set()
        for m in proposed:
            name = _class_name(m.get("name"))
            if name and _norm(name) not in seen:
                seen.add(_norm(name))
                notions.append({"name": name, "description": _plain(m.get("description"), 300)})
                m["name"] = name
    wanted = {_norm(n["name"]): n["name"] for n in notions}
    modules = {n["name"]: {"name": n["name"], "description": n.get("description", ""), "classes": [], "other": []}
               for n in notions}
    taken = set()
    for m in proposed:
        name = wanted.get(_norm(m.get("name")))
        if not name:
            continue
        for c in m.get("classes") or []:
            if not isinstance(c, dict):
                continue
            cname = _class_name(c.get("name"))
            if not cname or cname in taken:
                continue
            taken.add(cname)
            modules[name]["classes"].append({"name": cname, "note": _plain(c.get("note"), 300),
                                             "parent": _class_name(_one(c.get("parent"))) or None,
                                             "concepts": [i for i in _ids(c.get("concepts")) if i in by_id]})
        for o in m.get("other") or []:
            if not isinstance(o, dict):
                continue
            ids = [i for i in _ids(o.get("concepts")) if i in by_id]
            term = _plain(o.get("term"), 120)
            entry = {"concepts": ids, "term": term, "as": _plain(o.get("as"), 20), "hint": _plain(o.get("hint"), 200)}
            if ids or term:
                modules[name]["other"].append(entry)
    for n in notions:  # der Key Notion selbst gehoert in ihr Modul, auch wenn der Plan sie vergessen hat
        cname = _class_name(n["name"])
        if cname and cname not in taken:
            taken.add(cname)
            modules[n["name"]]["classes"].insert(0, {"name": cname, "note": n.get("description", ""), "parent": None,
                                                     "concepts": []})
    upper_renamed = _clean_planned_parents(modules.values(), upper_names)
    return {"ontology_name": _plain(r.get("ontology_name"), 120), "summary": _plain(r.get("summary"), 1000),
            "upper_renamed": upper_renamed,
            "license": _plain(r.get("license"), 200), "modules": list(modules.values()),
            "hierarchy_declined": [{"narrower": _plain(d.get("narrower"), 120), "broader": _plain(d.get("broader"), 120),
                                    "reason": _plain(d.get("reason"), 300)}
                                   for d in (r.get("hierarchy_declined") or [])[:200]
                                   if isinstance(d, dict) and d.get("narrower") and d.get("broader")],
            "excluded": {d["concept"]: _plain(d.get("reason"), 300) or "excluded by the plan"
                         for d in r.get("excluded") or [] if isinstance(d, dict) and isinstance(d.get("concept"), str)
                         and d.get("concept") in by_id}}

def _clean_planned_parents(modules, upper_names=()):
    """Die Oberklasse aus dem Plan (Wein-Lauf 4: ohne sie blieb die Hierarchie flach) gilt nur, wenn sie selbst
    geplant ist; ein Zyklus wird an der Klasse aufgebrochen, die ihn schliesst."""
    classes = [cl for m in modules for cl in m["classes"]]
    names = {cl["name"] for cl in classes} | set(upper_names)     # eine Klasse der oberen Schicht ist erlaubt
    for cl in classes:
        if cl.get("parent") not in names or cl.get("parent") == cl["name"]:
            cl["parent"] = None
    parent = {cl["name"]: cl["parent"] for cl in classes}
    for cl in classes:
        x, seen = parent[cl["name"]], set()
        while x and x != cl["name"] and x not in seen:
            seen.add(x)
            x = parent.get(x)
        if x == cl["name"]:
            cl["parent"] = parent[cl["name"]] = None
    return _rename_upper_collisions(classes, upper_names)

def _rename_upper_collisions(classes, upper_names) -> list:
    """Eine geplante Klasse mit dem Namen einer Klasse der oberen Schicht, die der Plan unter eine gewoehnliche Klasse
    stellt, meint etwas anderes (DECISIONS 159; VA dry4: "Process" als Szenario einer Evaluation, unter
    EvaluationScenario und damit unter Quality). Uebernaehme sie den Platz der oberen Klasse, waere Process wegen der
    Disjunktheit unerfuellbar und mit ihm jede Klasse darunter. Sie bekommt den Namen ihrer Oberklasse angehaengt."""
    upper = {_norm(n) for n in upper_names}
    taken = {_norm(cl["name"]) for cl in classes} | upper
    renamed = []
    for cl in classes:
        if _norm(cl["name"]) in upper and cl.get("parent") and _norm(cl["parent"]) not in upper:
            new, n = cl["name"] + cl["parent"], 2
            while _norm(new) in taken:
                new, n = f"{cl['name']}{cl['parent']}{n}", n + 1
            taken.add(_norm(new))
            renamed.append(f"{cl['name']} -> {new} (below {cl['parent']})")
            cl["name"] = new
    return renamed

# Optionale Schritte (Anbindungen, Nachtrag, Hierarchie, Kernrelationen) laufen bei diesen Fehlern ohne ihr Ergebnis
# weiter - auch bei einer abgeschnittenen Antwort, sonst ginge die bezahlte Generierung verloren (Review vor VA 4a-4c)
OPTIONAL_STEP_ERRORS = (HTTPException, ValueError, llm.LLMTruncatedError)

# ── Anbindung an Vokabulare nach der Planung (PLAN.md Phase 3c, DECISIONS 98, 101) ──────────────────────────────
# Wein-Lauf 11: sah der Plan die Terme eines Vokabulars, plante er sie als eigene Klassen nach (35 statt 11 Klassen,
# die meisten gleichnamige Kopien). Jetzt plant er ohne sie; danach sucht der Server zu jeder geplanten Klasse die
# aehnlichsten Terme (wie die Align-Aktion), und ein kleiner Aufruf entscheidet je Klasse: Unterklasse, gleiche
# Bedeutung, den Term statt der eigenen Klasse verwenden ('use_terms') - oder nichts.
LINK_SYS = ("You link the PLANNED classes of an ontology to classes of vocabularies the team loaded for reuse. For each "
            "planned class with candidate terms, decide by MEANING (the definitions, not the names):\n"
            "- \"subclass\": every instance of the planned class is an instance of the term - the usual case;\n"
            "- \"equivalent\": both have exactly the same instances - only if the term's definition says the same "
            "as the planned class, with the same scope. A broader term (a term for any kind of place, where the class "
            "means one kind of place) gives \"subclass\"; when in doubt, \"subclass\";\n"
            "- \"use\": the term replaces the planned class - only for vocabularies marked 'use terms directly', and "
            "only if the term means the SAME as the planned class (as for \"equivalent\"); the ontology then uses the "
            "term itself instead of an own class. A broader term never replaces a class (a task target is not just "
            "any entity): that is \"subclass\";\n"
            "- if no candidate fits, list the class under \"none\" with the reason - it is not asked again later.\n"
            "Use only the candidates given for that class.\n"
            'Answer ONLY as JSON: {"links":[{"class":"PlannedClass","term":"prefix:Name","as":"subclass|equivalent|use"}],'
            '"none":[{"class":"PlannedClass","reason":"why no candidate fits"}]}')

def _decisions(session) -> dict:
    return {s.get("prefix"): s.get("decision") or "align" for s in session.get("suggested_standards") or []
            if isinstance(s, dict)}

def link_candidates(session, plan) -> dict:
    """Je geplanter Klasse die aehnlichsten Klassen-Terme der geladenen Vokabulare (ohne 'reference only') - ueber
    ihren Namen und die Labels und Varianten ihrer Inventar-Begriffe (DECISIONS 105)."""
    decisions = _decisions(session)
    vocabs = {p: v for p, v in (session.get("vocabularies") or {}).items() if decisions.get(p) != "reference"}
    by_id = _inventory_parts(session)[2] or {}
    out = {}
    for m in plan["modules"] if vocabs else []:
        for cl in m["classes"]:
            labels = [x for i in cl.get("concepts") or [] if i in by_id
                      for x in [by_id[i]["label"], *(by_id[i].get("variants") or [])]]
            found = class_candidates(vocabs, cl["name"], labels)
            if found:
                out[cl["name"]] = found
    return out

def build_link_prompt(session, plan, cands) -> list:
    decisions = _decisions(session)
    vocabs = "\n".join(f"- {p}: {v.get('name')} - " + ("use terms directly" if decisions.get(p) == "use_terms" else "align")
                       for p, v in (session.get("vocabularies") or {}).items() if decisions.get(p) != "reference")
    lines = []
    for m in plan["modules"]:
        for cl in m["classes"]:
            if cl["name"] not in cands:
                continue
            lines.append(f"- {cl['name']} (module {m['name']})" + (f": {cl['note']}" if cl.get("note") else ""))
            lines += [f"    candidate {ref}" + (f' \"{t["label"]}\"' if t.get("label") else "") +
                      (f": {_plain(t.get('definition'), 160)}" if t.get("definition") else "") for _, ref, t in cands[cl["name"]]]
    task = ("**Use case:**\n" + _use_case(session) + "\n\n**Loaded vocabularies:**\n" + vocabs +
            "\n\n**Planned classes and candidate terms:**\n" + "\n".join(lines))
    return [{"role": "system", "content": LINK_SYS}, {"role": "user", "content": task}]

def apply_links(session, plan, result, cands) -> dict:
    """Uebernimmt die Entscheidungen: nur Kandidaten der Klasse; 'use' nur bei 'use_terms', nur fuer einen Term mit
    gleichem Namen oder Label wie die Klasse oder einer ihrer Begriffe (VA-Lauf 2: TaskTarget -> prov:Entity ersetzt;
    sonst 'subclass') und nicht fuer die Klasse einer Key Notion oder eine entschiedene Klasse (die bleiben eigene
    Klassen - dann gilt 'equivalent')."""
    decisions = _decisions(session)
    keep = {_class_name(m["name"]) for m in plan["modules"]} | set(decided_classes(session))
    dropped, replaced = [], {}
    for x in (result or {}).get("links") or []:
        if not isinstance(x, dict):
            continue
        name, ref, kind = _class_name(x.get("class")), str(x.get("term") or "").strip(), str(x.get("as") or "").strip()
        if ref not in {r for _, r, _ in cands.get(name, [])}:
            dropped.append(f"{name} -> {ref}: not a candidate of this class")
            continue
        if kind not in ("subclass", "equivalent", "use"):
            dropped.append(f"{name} -> {ref}: unknown kind of link {kind!r}")
            continue
        if kind == "use" and decisions.get(ref.split(":", 1)[0]) != "use_terms":
            dropped.append(f"{name} -> {ref}: the team chose 'align' for {ref.split(':', 1)[0]}, so it stays an own class")
            kind = "subclass"
        elif kind == "use" and max(s for s, r, _ in cands[name] if r == ref) < 3:   # 3: gleicher Name oder Label
            dropped.append(f"{name} -> {ref}: a term replaces a class only under the same name or label, so it stays "
                           "an own class below the term")
            kind = "subclass"
        elif kind == "use" and name in keep:
            kind = "equivalent"          # Key Notion oder entschiedene Klasse: bleibt, mit gleicher Bedeutung
        for m in plan["modules"]:
            for cl in list(m["classes"]):
                if cl["name"] != name:
                    continue
                if kind == "use":
                    m["classes"].remove(cl)
                    m["other"].append({"concepts": cl.get("concepts") or [], "term": cl["name"], "as": "term",
                                       "ref": ref, "hint": cl.get("note") or ""})
                    replaced[name] = ref
                else:
                    cl["link"], cl["link_as"] = ref, kind
    for m in plan["modules"]:           # Unterklassen einer ersetzten Klasse haengen nun unter dem Term
        for cl in m["classes"]:
            if cl.get("parent") in replaced:
                cl["parent"] = replaced[cl["parent"]]
    plan["reuse_dropped"] = dropped
    plan["reuse_candidates"] = len(cands)
    # Klassen mit Kandidaten, aber ohne Anbindung: als Entscheidung der Align-Aktion merken (Wein-Lauf 12), mit Grund
    linked = {cl["name"] for m in plan["modules"] for cl in m["classes"] if cl.get("link")} | set(replaced)
    reasons = {_class_name(x.get("class")): _plain(x.get("reason"), 300) for x in (result or {}).get("none") or []
               if isinstance(x, dict)}
    plan["link_declined"] = {name: reasons.get(name) or "no candidate fits (decided when linking the plan)"
                             for name in cands if name not in linked}
    return plan

# Nach den Modulen (DECISIONS 105): VA-Lauf 1 hatte 6 statt 13 Anbindungen. Die Anbindung nach der Planung sieht nur
# geplante Klassen - nicht die obere Schicht (Agent -> prov:Agent), nicht die Klassen, die ein Modul selbst anlegt,
# und keine Properties (used, wasDerivedFrom ohne prov:used, prov:wasDerivedFrom). Ein zweiter kleiner Aufruf legt
# diese mit ihren Kandidaten vor (wie die Align-Aktion, aber ohne die Ontologie-Liste); der Server prueft wie dort,
# dass Domain und Range einer Property innerhalb derer des Vokabular-Terms liegen.
LINK_AFTER_BATCH = 40
LINK_AFTER_SYS = (
    "You link the classes and properties of a newly generated ontology to terms of vocabularies the team loaded for "
    "reuse. For each own term with candidate terms, decide by MEANING (the descriptions and definitions, not the "
    "names):\n"
    "- class \"subclass\": every instance of the own class is an instance of the term - the usual case;\n"
    "- class \"equivalent\": both have exactly the same instances - only if the term's definition says the same as "
    "the own class, with the same scope; when in doubt, \"subclass\";\n"
    "- property \"subproperty\": every statement made with the own property also holds with the term. Its domain and "
    "range must lie within the term's (shown as domain -> range; '(any)' lies within nothing narrower) - otherwise "
    "the link would retype what the property connects;\n"
    "- if no candidate fits, list the own term under \"none\" with the reason - it is not asked again later.\n"
    "Use only the candidates given for that term.\n"
    'Answer ONLY as JSON: {"links":[{"item":"OwnTerm","term":"prefix:Name","as":"subclass|equivalent|subproperty"}],'
    '"none":[{"item":"OwnTerm","reason":"why no candidate fits"}]}')

def link_after_modules(session, llm_config, onto) -> tuple:
    """Bindet Klassen und Properties an, die die Anbindung nach der Planung nicht sehen konnte. Liefert (onto, report);
    wovon das Modell sagt, dass nichts passt, wird eine Entscheidung der Align-Aktion."""
    decisions = _decisions(session)
    cands = []
    for c in align_candidates({**session, "ontology": onto}):
        c["candidates"] = [t for t in c["candidates"] if decisions.get(t["ref"].split(":", 1)[0]) != "reference"]
        if c["candidates"]:
            cands.append(c)
    report = {"candidates": len(cands), "links": [], "rejected": [], "declined": [], "errors": []}
    if not cands:
        return onto, report
    vocabs = "\n".join(f"- {p}: {v.get('name')}" for p, v in (session.get("vocabularies") or {}).items()
                       if decisions.get(p) != "reference")
    by = {c["name"]: c for c in cands}
    store = decision_store(session, "align")
    for i in range(0, len(cands), LINK_AFTER_BATCH):
        part = cands[i:i + LINK_AFTER_BATCH]
        task = ("**Use case:**\n" + _use_case(session) + "\n\n**Loaded vocabularies:**\n" + vocabs +
                "\n\n**Own terms and candidate terms:**\n" + align_listing(part))
        try:
            with usage_step("Vocabulary links (after the modules)"):
                result = llm.call_llm_json(llm_config, [{"role": "system", "content": LINK_AFTER_SYS},
                                                        {"role": "user", "content": task}])
        except OPTIONAL_STEP_ERRORS as ex:   # ohne diese Anbindungen weiter; die Align-Aktion kann sie nachholen
            report["errors"].append(str(getattr(ex, "detail", ex))[:200])
            continue
        ops, shown, linked = [], [], set()
        names = {c["name"] for c in part}
        for x in (result or {}).get("links") or []:
            if not isinstance(x, dict):
                continue
            # eine Liste als "item" brach den Schritt ab (DECISIONS 168): ihr erster Name
            name, ref, kind = _one(x.get("item")), str(x.get("term") or "").strip(), str(x.get("as") or "").strip()
            c = by.get(name) if name in names else None
            if not c or ref not in {t["ref"] for t in c["candidates"]}:
                report["rejected"].append(f"{name} -> {ref}: not a candidate of this term")
            elif c["kind"] == "class" and kind in ("subclass", "equivalent"):
                same = kind == "equivalent"
                ops.append({"op": "add_axiom", "type": "EquivalentClasses" if same else "SubClassOf",
                            "classes": [name, ref], "module": c.get("module"), "scoped": False,
                            "natural_language": f"{name} means the same as {ref}." if same else f"Every {name} is a {ref}."})
                shown.append(f"{name} {'=' if same else '->'} {ref}")
            elif c["kind"] != "class" and kind == "subproperty":
                ops.append({"op": "update_property", "name": name, "sub_property_of": ref})
                shown.append(f"{name} < {ref}")
            else:
                report["rejected"].append(f"{name} -> {ref}: \"{kind}\" does not fit a {c['kind']}")
                continue
            linked.add(name)
        onto, applied = apply_edits(onto, ops, label_languages(session)[0], known_prefixes(session),
                                    session_vocab(session))
        failed = {id(r["op"]) for r in applied["rejected"]}
        report["links"] += [s for op, s in zip(ops, shown) if id(op) not in failed]
        report["rejected"] += [f"{s}: {r['reason']}" for op, s in zip(ops, shown) for r in applied["rejected"]
                               if r["op"] is op]
        reasons = {_one(x.get("item")): _plain(x.get("reason"), 300) for x in (result or {}).get("none") or []
                   if isinstance(x, dict)}
        for c in part:                   # weder angebunden noch abgelehnt: kein Kandidat passt
            if c["name"] not in linked:
                store[c["name"]] = {"item": c["name"],
                                    "reason": reasons.get(c["name"]) or "no candidate fits (decided after the modules)"}
                report["declined"].append(c["name"])
    return onto, report

# Hierarchie nach den Modulen (DECISIONS 111): die Literatur nennt Oberbegriffe, die die erzeugten Klassen nicht
# umsetzen - in fuenf VA-Laeufen 49-77 je Lauf, die meisten von Lauf zu Lauf andere, ohne Grund. Ein kurzer Aufruf
# entscheidet je Beziehung: auch eine Art davon (Oberklasse bzw. zusaetzliches SubClassOf) oder begruendet nicht.
HIERARCHY_AFTER_BATCH = 60
HIERARCHY_AFTER_SYS = (
    "The sources of an ontology's literature state broader/narrower relations between terms that are now both classes "
    "of the generated ontology, but the class hierarchy does not realize them. Decide for each relation by the "
    "classes' MEANING (their descriptions and current superclasses):\n"
    "- \"kind_of\": every instance of the narrower class is an instance of the broader one. The broader class becomes "
    "its superclass, or an additional one if it already has another - only if both hold; a class that is a different "
    "thing than its current superclass suggests (a task vs. a technique of the same name) is not a kind of both;\n"
    "- \"decline\": the sources use \"broader\" loosely - a part of it, related to it, a step or a result of it, the "
    "same word in another sense, or a category of it rather than a kind - with the reason; it is not asked again.\n"
    'Answer ONLY as JSON: {"relations":[{"item":1,"decision":"kind_of|decline","reason":"one sentence"}]}')

def hierarchy_after_modules(session, llm_config, onto) -> tuple:
    """Legt die nicht umgesetzten Oberbegriffe der Literatur zur Entscheidung vor. Liefert (onto, report)."""
    report = {"relations": 0, "realized": [], "declined": 0, "rejected": [], "errors": []}
    inv = _inventory_parts(session)[0]
    if not inv:
        return onto, report
    store = decision_store(session, "hierarchy")
    todo = hierarchy_coverage(onto, inv, concept_key, session.get("gap_decisions"),
                              declined_relations(session))["unrealized"]
    report["relations"] = len(todo)
    by = {c["name"]: c for c in onto["classes"]}
    def line(name):
        c = by.get(name) or {}
        return f"   {name}" + (f" (below {c['parent']})" if c.get("parent") else "") + \
            (f": {_plain(c.get('description'), 160)}" if c.get("description") else "")
    for i in range(0, len(todo), HIERARCHY_AFTER_BATCH):
        part = todo[i:i + HIERARCHY_AFTER_BATCH]
        items = "\n".join(f"{k}. {u['narrower']} is a kind of {u['broader']}? ({u['support']} source"
                          f"{'s' if u['support'] != 1 else ''})\n{line(u['narrower'])}\n{line(u['broader'])}"
                          for k, u in enumerate(part, 1))
        try:
            with usage_step("Hierarchy (after the modules)"):
                result = llm.call_llm_json(llm_config, [{"role": "system", "content": HIERARCHY_AFTER_SYS},
                                                        {"role": "user", "content": "**Use case:**\n" + _use_case(session) +
                                                         "\n\n**Relations:**\n" + items}])
        except OPTIONAL_STEP_ERRORS as ex:   # ohne diese Oberklassen weiter; "Build hierarchy" kann sie nachholen
            report["errors"].append(str(getattr(ex, "detail", ex))[:200])
            continue
        ops, wanted, new_parent, accepted = [], [], {}, []   # in diesem Paket gesetzte Oberklassen und Kanten
        for x in (result or {}).get("relations") or []:
            try:
                u = nth(part, x.get("item"))
            except (TypeError, ValueError, IndexError, AttributeError):
                continue
            if u is None:
                continue
            n, b = u["narrower"], u["broader"]
            if x.get("decision") == "decline":
                store[relation_key(n, b)] = {"item": f"{n} is a kind of {b}",
                                            "reason": _plain(x.get("reason"), 300) or "declined after the modules"}
                report["declined"] += 1
            elif x.get("decision") == "kind_of":
                conflict = _disjoint_conflict(onto, n, b, accepted)
                if (by.get(n) or {}).get("layer") == "upper":
                    conflict = "an upper-layer class stays at the top"
                if conflict:
                    report["rejected"].append(f"{n} -> {b}: {conflict}")
                    continue
                parent = new_parent.get(n) or (by.get(n) or {}).get("parent")
                if not parent or (by.get(parent) or {}).get("layer") == "upper":   # nur die obere Schicht darueber
                    ops.append({"op": "update_class", "name": n, "parent": b})
                    new_parent[n] = b
                else:
                    ops.append({"op": "add_axiom", "type": "SubClassOf", "classes": [n, b], "module": by[n].get("module"),
                                "scoped": False, "natural_language": f"Every {n} is a {b}."})
                wanted.append(f"{n} -> {b}")
                accepted.append((n, b))
        onto, applied = apply_edits(onto, ops, label_languages(session)[0], known_prefixes(session),
                                    session_vocab(session))
        failed = {id(r["op"]): r["reason"] for r in applied["rejected"]}
        report["realized"] += [w for op, w in zip(ops, wanted) if id(op) not in failed]
        report["rejected"] += [f"{w}: {failed[id(op)]}" for op, w in zip(ops, wanted) if id(op) in failed]
        by = {c["name"]: c for c in onto["classes"]}
    return onto, report

def _disjoint_conflict(onto, narrower, broader, pending=()) -> str:
    """Wuerde narrower unter broader mit einer Disjunktheit kollidieren - fuer narrower oder eine seiner Unterklassen,
    zusammen mit den Kanten, die dieses Paket schon angenommen hat (pending)? Dann waere eine Klasse unerfuellbar
    (Code-Review 2026-10-29: vorher nur gegen den Stand vor dem Paket und nur fuer narrower selbst)."""
    edge = lambda n, b: {"type": "SubClassOf", "classes": [n, b]}
    disjoint = [set(a.get("classes") or []) for a in onto.get("axioms") or [] if a.get("type") == "DisjointClasses"]
    def clashes(axioms):
        anc = _ancestors({**onto, "axioms": axioms})
        found = set()
        for c in [narrower, *(x for x, a in anc.items() if narrower in a)]:
            mine = anc.get(c, set()) | {c}
            for d in disjoint:
                hit = sorted(d & mine)
                if len(hit) >= 2:
                    found.add((c, hit[0], hit[1]))
        return found
    base = list(onto.get("axioms") or []) + [edge(n, b) for n, b in pending]
    new = clashes(base + [edge(narrower, broader)]) - clashes(base)
    return "" if not new else "{1} and {2} are disjoint".format(*sorted(new)[0])

# Kernrelationen nach den Modulen (DECISIONS 112): in VA 3a-3c hingen 44-58 Relationen der Module unter keiner der
# 41 Kernrelationen (hasTaskInput nicht unter usesAsInput, hasModelOutput nicht unter produces) - jedes Modul sieht
# alle Kernrelationen und setzt selten eine darueber. Ein kurzer Aufruf entscheidet je Relation mit passenden
# Kandidaten (Domain und Range darin), wie die Aktion "Consolidate properties".
CORE_AFTER_BATCH = 40
CORE_AFTER_SYS = (
    "You place the relations (object properties) of a newly generated modular ontology below the CORE RELATIONS the "
    "team approved for the whole ontology. For each relation with candidate core relations decide by MEANING:\n"
    "- \"below\": every statement made with the relation is also a statement of the core relation - a more specific "
    "way of the same connection (such as a task's input below a general \"uses as input\"); name that core "
    "relation;\n"
    "- \"none\": the relation is a connection of its own kind (to a value set, a role, a time) or no candidate shares "
    "its meaning - with the reason; it is not asked again.\n"
    "Fitting domain and range are not enough; the meaning decides. Use only the candidates given for a relation.\n"
    'Answer ONLY as JSON: {"relations":[{"item":1,"decision":"below|none","core":"coreRelation",'
    '"reason":"one sentence"}]}')

def core_after_modules(session, llm_config, onto, vocab) -> tuple:
    """Legt die Relationen der Module ohne Kernrelation darueber mit ihren Kandidaten vor. Liefert (onto, report)."""
    report = {"relations": 0, "placed": [], "declined": 0, "rejected": [], "errors": []}
    store = decision_store(session, "properties")
    props = {p["name"]: p for p in onto["properties"]}
    core = [p for p in onto["properties"] if p.get("module") == CORE_MODULE and p.get("type") == "ObjectProperty"]
    anc = _ancestors(onto)
    within = lambda cls, outer: not outer or cls == outer or (cls and outer in anc.get(cls, ()))
    todo = []
    for name in check_core_relations(onto, vocab)["without_core"]:
        p = props[name]
        if name in store:
            continue
        cands = [c["name"] for c in core if within(p.get("domain"), c.get("domain")) and
                 within(p.get("range"), c.get("range"))]
        cands.sort(key=lambda n: (not props[n].get("domain") and not props[n].get("range"), n))   # spezifische zuerst
        if cands:
            todo.append((p, cands))
    report["relations"] = len(todo)
    if not todo:
        return onto, report
    core_lines = "\n".join(f"- {c['name']}: {c.get('domain') or '(any)'} -> {c.get('range') or '(any)'}" +
                           (f": {_plain(c.get('description'), 120)}" if c.get("description") else "") for c in core)
    for i in range(0, len(todo), CORE_AFTER_BATCH):
        part = todo[i:i + CORE_AFTER_BATCH]
        items = "\n".join(f"{k}. {p['name']} (module {p.get('module')}): {p.get('domain') or '(any)'} -> "
                          f"{p.get('range') or '(any)'}" +
                          (f": {_plain(p.get('description'), 140)}" if p.get("description") else "") +
                          f"\n   candidates: {', '.join(cands)}" for k, (p, cands) in enumerate(part, 1))
        try:
            with usage_step("Core relations (after the modules)"):
                result = llm.call_llm_json(llm_config, [{"role": "system", "content": CORE_AFTER_SYS},
                                                        {"role": "user", "content": "**Core relations:**\n" + core_lines +
                                                         "\n\n**Relations of the modules:**\n" + items}])
        except OPTIONAL_STEP_ERRORS as ex:   # ohne diese Zuordnungen weiter; "Consolidate properties" kann es
            report["errors"].append(str(getattr(ex, "detail", ex))[:200])
            continue
        ops, shown = [], []
        for x in (result or {}).get("relations") or []:
            try:
                p, cands = nth(part, x.get("item")) or (None, None)
            except (TypeError, ValueError, IndexError, AttributeError):
                continue
            if p is None:
                continue
            if x.get("decision") == "none":
                store[p["name"]] = {"item": p["name"],
                                    "reason": _plain(x.get("reason"), 300) or "no core relation fits (after the modules)"}
                report["declined"] += 1
            elif x.get("decision") == "below":
                if x.get("core") not in cands:
                    report["rejected"].append(f"{p['name']} < {x.get('core')}: not a candidate of this relation")
                    continue
                ops.append({"op": "update_property", "name": p["name"], "sub_property_of": x["core"]})
                shown.append(f"{p['name']} < {x['core']}")
        onto, applied = apply_edits(onto, ops, label_languages(session)[0], known_prefixes(session),
                                    session_vocab(session))
        failed = {id(r["op"]): r["reason"] for r in applied["rejected"]}
        report["placed"] += [s for op, s in zip(ops, shown) if id(op) not in failed]
        report["rejected"] += [f"{s}: {failed[id(op)]}" for op, s in zip(ops, shown) if id(op) in failed]
    return onto, report

PLAN_COMPLETE_BATCH = 60
PLAN_COMPLETE_SYS = (
    "A plan for a modular ontology leaves some CENTRAL concepts of the literature unassigned. "
    "Account for each one: add it to a planned class of the same meaning, plan a new class for it (with its module "
    "and the planned class it is a kind of), model it as a property or an individual of a module, or exclude it with "
    "the reason (out of scope for the use case, specific to one paper's method, generic research vocabulary, or the "
    "same as another concept). Use only the module and class names given; new class names UpperCamelCase.\n"
    "Concepts marked REVIEW were excluded by the plan, for the reason given. Check that reason: place the concept, or "
    "list it under \"excluded\" again with a reason that holds for a central concept of the literature. Where the "
    "mark says the concept is a category of one of the literature's taxonomies or named by a competency question, "
    "being narrow, specific or part of one framework is no reason to leave it out: place a taxonomy's category as a "
    "subclass, or - where the categories are fine-grained values - as an individual of the class that stands for the "
    "taxonomy. Exclude such a concept only if it is out of scope for the use case or the same as another concept, and "
    "say which.\n"
    'Answer ONLY as JSON: {"assign":[{"concept":"c12","module":"Module","class":"ClassName","new":true,'
    '"parent":"PlannedClass or null"},{"concept":"c13","module":"Module","as":"property|individual","hint":"how"}],'
    '"excluded":[{"concept":"c14","reason":"..."}]}')

def _protected(session, inv) -> dict:
    """Begriffe, die der Plan nicht als 'zu speziell' ausschliessen soll (DECISIONS 110): Kategorien einer Taxonomie
    der Literatur und Begriffe, die eine Kompetenzfrage nennt. id -> warum."""
    cats = {}
    for t in inv.get("taxonomies") or []:
        for cat in t.get("categories") or []:
            cats.setdefault(concept_key(str(cat).split(":")[-1]), t.get("name") or "a taxonomy")
    cqs = [_cq_text(c).lower() for c in (session.get("momo") or {}).get("competency_questions") or []]
    def named(label, q):
        label = label.strip().lower()
        return len(label) >= 4 and label not in _STOP and re.search(r"\b" + re.escape(label) + r"(s|es)?\b", q)
    out = {}
    for c in inv["concepts"]:
        names = [c["label"], *c.get("variants", [])]
        tax = next((cats[concept_key(v)] for v in names if concept_key(v) in cats), None)
        if tax:
            out[c["id"]] = f'a category of the literature\'s taxonomy "{tax}"'
            continue
        n = next((n for n, q in enumerate(cqs, 1) if any(named(v, q) for v in names)), None)
        if n:
            out[c["id"]] = f"named in competency question {n}"
    return out

# eine Begruendung des Ausschlusses, die eine geplante Klasse nennt, ist eine Zuordnung (VA 5a: "accounted for as
# ObjectiveUncertainty in the Uncertainty module"); "covered by the Uncertainty module" nennt ein Modul, keine Klasse
_AS_CLASS = re.compile(r"\b(?i:accounted for|modell?ed|represented|covered|captured|included)\s+(?i:as|by)\s+"
                       r"(?i:the\s+)?(?i:class\s+)?`?([A-Z][A-Za-z0-9]*)`?(?!\w|\s+module)"
                       r"|\b(?i:same as)\s+(?i:the\s+)?(?i:class\s+)?`?([A-Z][A-Za-z0-9]*)`?(?!\w|\s+module)")

_NEGATED = re.compile(r"\b(?:not|never|no longer|neither|nor|cannot|can't|isn't|aren't|wasn't|won't)\b(?:\s+\w+){0,4}\s*$",
                      re.IGNORECASE)

def _named_class(reason, classes):
    """Die geplante Klasse, als die eine Begruendung den Begriff schon fuehrt, sonst None."""
    text = str(reason or "")
    for m in _AS_CLASS.finditer(text):
        name = m.group(1) or m.group(2)
        # "not modelled as X", "is never represented by X", "cannot be captured as X": keine Zuordnung (DECISIONS 166)
        if _NEGATED.search(text[max(0, m.start() - 40):m.start()]):
            continue
        if name in classes:
            return name
    return None

def _accounted(plan) -> set:
    ids = {i for m in plan["modules"] for cl in m["classes"] for i in cl.get("concepts") or []}
    ids |= {i for m in plan["modules"] for o in m["other"] for i in o.get("concepts") or []}
    return ids | set(plan.get("excluded") or {})

def _place_concepts(plan, result, wanted, by_id, classes, upper, default_reason) -> tuple:
    """Uebernimmt die Antwort eines Nachtrags zum Plan (Nachtrag zentraler Begriffe, DECISIONS 104; zu kleiner Plan,
    DECISIONS 147): Ausschluesse mit Grund, Zuordnungen zu einer geplanten oder neuen Klasse, als Property oder
    Individuum. Nur Begriffe aus `wanted`, die noch keinen Platz haben. Liefert (zugeordnet, ausgeschlossen,
    neue Klassen)."""
    modules = {m["name"]: m for m in plan["modules"]}
    assigned = excluded = new = 0
    for x in (result or {}).get("excluded") or []:
        if isinstance(x, dict) and isinstance(x.get("concept"), str) and x["concept"] in wanted \
                and x["concept"] not in _accounted(plan):
            plan["excluded"][x["concept"]] = _plain(x.get("reason"), 300) or default_reason
            excluded += 1
    for x in (result or {}).get("assign") or []:
        cid = x.get("concept") if isinstance(x, dict) and isinstance(x.get("concept"), str) else None
        mod = modules.get(_one(x.get("module"))) if cid in wanted else None   # eine Liste: ihr erster Name (168)
        if not mod or cid in _accounted(plan):
            continue
        assigned += 1
        if x.get("as") in ("property", "individual"):
            mod["other"].append({"concepts": [cid], "term": "", "as": x["as"], "hint": _plain(x.get("hint"), 200)})
            continue
        name = _class_name(x.get("class")) or _class_name(by_id[cid]["label"])
        if name in classes:                       # derselbe Begriff wie eine geplante Klasse
            classes[name][1].setdefault("concepts", []).append(cid)
            continue
        parent = _class_name(_one(x.get("parent"))) or None
        parent = parent if parent in classes or parent in upper else None
        # ein Name der oberen Schicht unter einer gewoehnlichen Klasse meint etwas anderes - wie im Plan (DECISIONS
        # 159), sonst nahm die neue Klasse den Platz der oberen ein und wurde unerfuellbar (DECISIONS 168)
        if parent and parent not in upper and _norm(name) in {_norm(u) for u in upper}:
            new_name, n = name + parent, 2
            while new_name in classes or _norm(new_name) in {_norm(u) for u in upper}:
                new_name, n = f"{name}{parent}{n}", n + 1
            plan.setdefault("upper_renamed", []).append(f"{name} -> {new_name} (below {parent})")
            name = new_name
        cl = {"name": name, "note": _concept_definition(by_id[cid])[:300], "concepts": [cid], "parent": parent}
        mod["classes"].append(cl)
        classes[name] = (mod, cl)
        new += 1
    return assigned, excluded, new

def complete_plan(session, llm_config, plan, inv) -> dict:
    """Prueft, ob der Plan jeden zentralen Begriff zuordnet oder begruendet ausschliesst; die fehlenden gehen in
    einem Nachtrag (in Paketen) an das Modell. Was danach noch fehlt, wird berichtet. Begriffe, die das Team oder
    "Add missing central concepts" schon ausgelassen haben, gelten als ausgeschlossen."""
    by_id = {c["id"]: c for c in inv["concepts"]}
    cids = central_ids(inv)                 # DECISIONS 160: in einem kleinen Korpus auch die Begriffe der Themen
    central = [c for c in inv["concepts"] if c["id"] in cids]
    plan.setdefault("excluded", {})
    gap = session.get("gap_decisions") or {}
    classes = {cl["name"]: (m, cl) for m in plan["modules"] for cl in m["classes"]}
    accounted_as = []
    for cid, reason in list(plan["excluded"].items()):
        name = _named_class(reason, classes) if cid in by_id else None
        if name:
            classes[name][1].setdefault("concepts", []).append(cid)
            del plan["excluded"][cid]
            accounted_as.append(by_id[cid]["label"])
    earlier = 0
    for c in central:
        reason = next((gap[concept_key(v)] for v in [c["label"], *c.get("variants", [])] if concept_key(v) in gap), None)
        if reason and c["id"] not in _accounted(plan):
            plan["excluded"][c["id"]] = reason
            earlier += 1
    # jeder Ausschluss des Plans geht noch einmal an den Nachtrag (DECISIONS 110, 131): ein einzelner Aufruf schloss
    # bei gleicher Eingabe 16 bis 51 zentrale Begriffe aus (VA 4a-5c). Kategorien einer Taxonomie und Begriffe einer
    # Kompetenzfrage sind dabei geschuetzt; was der Nachtrag nicht unterbringt, bleibt mit dem Grund des Plans aus
    protected = _protected(session, inv)
    # nur zentrale: ein Begriff einer Quelle, den der Plan ausschliesst (DECISIONS 140: die Methode eines Papers), bleibt aus
    review = {cid: (plan["excluded"].pop(cid), protected.get(cid)) for cid in list(plan["excluded"])
              if cid in by_id and cid in cids and not any(
                  concept_key(v) in gap for v in [by_id[cid]["label"], *by_id[cid].get("variants", [])])}
    by_plan = len([c for c in central if c["id"] in _accounted(plan)]) - earlier
    assigned = excluded = 0
    missing = [c for c in central if c["id"] not in _accounted(plan)]
    upper = set(_upper_names(session))
    ids = _concept_ids(inv)
    errors = []
    for i in range(0, len(missing), PLAN_COMPLETE_BATCH):
        part = missing[i:i + PLAN_COMPLETE_BATCH]
        listing = "\n".join(f"{c['id']} | {c['label']} | {c['papers']} sources" +
                            (f" | broader: {_broader_of(c, ids)}" if _broader_of(c, ids) else "") +
                            (f" | {_concept_definition(c)[:200]}" if _concept_definition(c) else "") +
                            (f' | REVIEW: excluded by the plan ("{review[c["id"]][0]}")' +
                             (f" although {review[c['id']][1]}" if review[c["id"]][1] else "")
                             if c["id"] in review else "") for c in part)
        task = ("**Use case:**\n" + _use_case(session) + "\n\n**Planned modules and classes:**\n" +
                "\n".join(f"- {m['name']}: " + ", ".join(cl["name"] for cl in m["classes"]) for m in plan["modules"]) +
                ("\n\n**Upper layer:** " + ", ".join(sorted(upper)) if upper else "") +
                "\n\n**Central concepts without a place in the plan** (id | label | sources | broader | definition):\n" +
                listing)
        try:
            with usage_step("Plan completion"):
                result = llm.call_llm_json(llm_config, [{"role": "system", "content": PLAN_COMPLETE_SYS},
                                                        {"role": "user", "content": task}])
        except OPTIONAL_STEP_ERRORS as ex:   # ohne Nachtrag weiter; "Add missing central concepts" kann ihn nachholen
            errors.append(str(getattr(ex, "detail", ex))[:200])
            continue
        a, e, _new = _place_concepts(plan, result, {c["id"] for c in part}, by_id, classes, upper,
                                     "excluded when completing the plan")
        assigned, excluded = assigned + a, excluded + e
    for cid, (reason, _why) in review.items():   # nicht untergebracht: der Grund des Plans gilt weiter
        if cid not in _accounted(plan):
            plan["excluded"][cid] = reason
    open_ = [by_id[c["id"]]["label"] for c in central if c["id"] not in _accounted(plan)]
    plan["central_report"] = {"central": len(central), "by_plan": by_plan, "earlier_decisions": earlier,
                              "completion_assigned": assigned, "completion_excluded": excluded,
                              "excluded": sorted(by_id[i]["label"] for i in plan["excluded"] if i in by_id),
                              "unassigned": open_[:80], "unassigned_count": len(open_), "errors": errors,
                              "reviewed": len(review),
                              "reviewed_protected": sum(1 for x in review.values() if x[1]),
                              "review_kept": sorted(by_id[i]["label"] for i in review if i in plan["excluded"]),
                              "accounted_as": sorted(accounted_as)}
    return plan

# Ein zu kleiner Plan (DECISIONS 147): die offenen Modelle planten fuer den Wein 19-60 Klassen bei einem Ziel von
# etwa 82, gpt-6-sol 58-67. Unter dem Anteil fragt ein Nachtrag die noch ungenutzten Begriffe der Themen ab.
PLAN_GROW_SHARE = 0.6
PLAN_GROW_BATCH = 80
PLAN_GROW_SYS = (
    "A plan for a modular ontology has far fewer classes than its concept inventory supports. Below are the concepts "
    "of the inventory's themes that the plan has not used yet. For each one the use case needs: add it to a planned "
    "class of the same meaning, plan a new class for it (with its module and the planned class it is a kind of), or "
    "model it as a property or an individual of a module. Exclude the others with the reason (out of scope for the use "
    "case, specific to one paper's method - what one paper builds or computes, not what it says about the domain -, "
    "generic research vocabulary, or the same as another concept). Do not exclude a concept only to keep the plan "
    "small. Concepts marked REVIEW were excluded by the plan for the reason given: check that reason - place the "
    "concept, or list it under \"excluded\" again with a reason that holds. A concept a competency question names, or "
    "a category of one of the literature's taxonomies, is not excluded for being narrow or specific. Use only the "
    "module and class names given; new class names UpperCamelCase.\n"
    'Answer ONLY as JSON: {"assign":[{"concept":"c12","module":"Module","class":"ClassName","new":true,'
    '"parent":"PlannedClass or null"},{"concept":"c13","module":"Module","as":"property|individual","hint":"how"}],'
    '"excluded":[{"concept":"c14","reason":"..."}]}')

# Gruende, mit denen der Plan die Methode eines Papers ausschliesst - frei formuliert: "specific to one paper's
# method", "the graph the paper builds", "a particular graph resource used by one paper" (Wein, Runde 7)
_METHOD_REASON = re.compile(r"\bmethod|\b(?:one|a single|a|the)\s+paper\b|\bpaper'?s\b|\bp\d+'s\b", re.I)

def _planned(plan) -> int:
    return sum(len(m["classes"]) for m in plan["modules"])

def grow_plan(session, llm_config, plan, inv) -> dict:
    """Hat der Plan weniger als PLAN_GROW_SHARE des Ziels (plan_target), gehen die Begriffe der Themen und die
    zentralen, die er nicht nutzt, in Paketen an einen Nachtrag (DECISIONS 147) - auch die, die er selbst
    ausgeschlossen hat, mit seinem Grund zur Pruefung: der Plan laesst Begriffe selten offen, er schliesst sie aus
    (DeepSeek V4.1, Wein: 40 ausgeschlossen, darunter Vintage, das zwei Kompetenzfragen nennen). Zentrale Begriffe hat
    schon der Nachtrag des Plans geprueft (DECISIONS 131). Was nicht untergebracht wird, bleibt mit dem Grund des
    Plans aus. Sonst kein Aufruf. Das Ergebnis steht in plan["size_report"]."""
    target, before = plan_target(inv), _planned(plan)
    rep = {"target": target, "planned": before, "asked": False, "candidates": 0, "reviewed": 0, "added_classes": 0,
           "assigned": 0, "excluded": 0, "after": before, "errors": []}
    plan["size_report"] = rep
    if before >= PLAN_GROW_SHARE * target:
        return plan
    _, docs, by_id = _inventory_parts(session)
    theme = _theme_of(inv)
    gap = session.get("gap_decisions") or {}
    decided = lambda c: any(concept_key(v) in gap for v in [c["label"], *c.get("variants", [])])
    cids = central_ids(inv)
    relevant = lambda c: c["id"] in cids or c["id"] in theme
    # was der Plan als Methode eines Papers ausschloss, bleibt aus (DECISIONS 140): angeboten, brachte der Nachtrag
    # FlavorGraph und HeterogeneousNetwork zurueck (Wein 7-dsv41r-a). Die Modelle nennen den Grund aber auch falsch
    # (Astringent, elimination rules "specific to one paper's method"): was eine Kompetenzfrage oder eine Taxonomie
    # nennt, wird trotzdem noch einmal angeboten
    protected = _protected(session, inv)
    review = {cid: plan["excluded"].pop(cid) for cid in list(plan.get("excluded") or {})
              if cid in by_id and cid not in cids and relevant(by_id[cid]) and not decided(by_id[cid])
              and (cid in protected or not _METHOD_REASON.search(plan["excluded"][cid]))}
    open_ = [c for c in inv["concepts"] if relevant(c) and c["id"] not in _accounted(plan) and not decided(c)]
    open_.sort(key=lambda c: (theme.get(c["id"], "~"), -c["papers"]))
    rep.update(asked=bool(open_), candidates=len(open_), reviewed=len(review))
    classes = {cl["name"]: (m, cl) for m in plan["modules"] for cl in m["classes"]}
    upper = set(_upper_names(session))
    ids, pids = _concept_ids(inv), _paper_ids(docs)
    for i in range(0, len(open_), PLAN_GROW_BATCH):
        part = open_[i:i + PLAN_GROW_BATCH]
        def line(c):
            src = {s["doc"] for s in c.get("sources") or []}
            return (f"{c['id']} | {c['label']} | {c['papers']}" +
                    (f" ({pids[next(iter(src))]})" if c["papers"] == 1 and len(src) == 1 and next(iter(src)) in pids else "") +
                    (f" | theme: {theme[c['id']]}" if c["id"] in theme else "") +
                    (f" | broader: {_broader_of(c, ids)}" if _broader_of(c, ids) else "") +
                    (f" | {_concept_definition(c)[:200]}" if _concept_definition(c) else "") +
                    (f' | REVIEW: excluded by the plan ("{review[c["id"]]}")' +
                     (f" although {protected[c['id']]}" if c["id"] in protected else "") if c["id"] in review else ""))
        task = ("**Use case:**\n" + _use_case(session) +
                f"\n\n**The plan has {_planned(plan)} classes; the inventory supports about {target}.**" +
                "\n\n**Planned modules and classes:**\n" +
                "\n".join(f"- {m['name']}: " + ", ".join(cl["name"] for cl in m["classes"]) for m in plan["modules"]) +
                ("\n\n**Upper layer:** " + ", ".join(sorted(upper)) if upper else "") +
                "\n\n**Sources** (what each is about):\n" + _sources_block(docs) +
                "\n\n**Concepts not used by the plan** (id | label | sources | theme | broader | definition):\n" +
                "\n".join(line(c) for c in part))
        try:
            with usage_step("Plan size"):
                result = llm.call_llm_json(llm_config, [{"role": "system", "content": PLAN_GROW_SYS},
                                                        {"role": "user", "content": task}])
        except OPTIONAL_STEP_ERRORS as ex:      # ohne Nachtrag weiter: der Plan bleibt, wie er ist
            rep["errors"].append(str(getattr(ex, "detail", ex))[:200])
            continue
        a, e, new = _place_concepts(plan, result, {c["id"] for c in part}, by_id, classes, upper,
                                    "excluded when the plan was too small")
        rep["assigned"] += a
        rep["excluded"] += e
        rep["added_classes"] += new
    for cid, reason in review.items():          # nicht untergebracht: der Grund des Plans gilt weiter
        if cid not in _accounted(plan):
            plan["excluded"][cid] = reason
    rep["review_placed"] = sum(1 for cid in review if cid not in plan["excluded"])
    rep["after"] = _planned(plan)
    return plan

def _apply_planned_links(plan, onto) -> dict:
    """Die Anbindungen aus der Planung als SubClassOf- oder EquivalentClasses-Axiome (wie die Align-Aktion), sofern
    das Modul sie nicht schon gesetzt hat; dazu die Terme, die statt eigener Klassen verwendet werden."""
    by = {c["name"]: c for c in onto["classes"]}
    have = {tuple(a["classes"]) for a in onto["axioms"]
            if a.get("type") in ("SubClassOf", "EquivalentClasses") and len(a.get("classes") or []) == 2}
    links = []
    for m in plan["modules"]:
        for cl in m["classes"]:
            ref, c = cl.get("link"), by.get(cl["name"])
            if not ref or not c:
                continue
            same = cl.get("link_as") == "equivalent"
            if (c.get("parent") != ref or same) and (cl["name"], ref) not in have:
                onto["axioms"].append({"type": "EquivalentClasses" if same else "SubClassOf", "classes": [cl["name"], ref],
                                       "module": c.get("module"), "scoped": False,
                                       "natural_language": f"{cl['name']} means the same as {ref}." if same
                                       else f"Every {cl['name']} is a {ref}."})
            links.append(f"{cl['name']} {'=' if same else '->'} {ref}")
    terms = [f"{o.get('term') or ', '.join(o.get('concepts') or [])} -> {o['ref']}"
             for m in plan["modules"] for o in m["other"] if o.get("ref")]
    return {"links": links, "terms": terms, "dropped": plan.get("reuse_dropped") or [],
            "candidates": plan.get("reuse_candidates", 0), "error": plan.get("reuse_error"),
            "declined": sorted(plan.get("link_declined") or {})}

def _apply_planned_parents(plan, onto) -> dict:
    """Nach dem Zusammenfuehren: hat ein Modul die geplante Oberklasse weggelassen, wird sie gesetzt. Eine andere
    Oberklasse des Moduls bleibt (es darf eine eigene Klasse dazwischen setzen); liegt die geplante dann nicht
    darueber, wird das berichtet."""
    by = {c["name"]: c for c in onto["classes"]}
    def ancestors(name):
        seen = []
        while name and name not in seen:
            seen.append(name)
            name = (by.get(name) or {}).get("parent")
        return seen
    planned, filled, differ = 0, [], []
    for m in plan["modules"]:
        for cl in m["classes"]:
            c, p = by.get(cl["name"]), cl.get("parent")
            if not c or not p or (p not in by and ":" not in p):
                continue
            planned += 1
            if not c.get("parent") or (c["parent"] not in by and ":" not in c["parent"]):
                if cl["name"] not in ancestors(p):          # kein Zyklus durch die Oberklassen der Module
                    c["parent"] = p
                    filled.append(cl["name"])
            elif p not in ancestors(c["parent"]):
                differ.append(f"{cl['name']} below {c['parent']} instead of {p}")
    return {"planned": planned, "set_from_plan": filled, "differ": differ}

def build_module_prompt(session, notion, plan, standards, context, use_case=None):
    inv, docs, by_id = _inventory_parts(session)
    docs, by_id = docs or {}, by_id or {}
    momo = session.get("momo") or {}
    mod = next(m for m in plan["modules"] if m["name"] == notion["name"])
    used_docs, blocks = [], []
    decided = decided_classes(session)
    def cite(doc_id):
        if doc_id not in used_docs:
            used_docs.append(doc_id)
        return doc_id
    for cl in mod["classes"]:
        lines = [f"### {cl['name']}"]
        if cl["name"] in decided:
            concept, definition, names = decided[cl["name"]]
            lines.append(f"- DECIDED DEFINITION (by the team - use it word for word as the description): {definition}")
            if len(names) > 1:
                lines.append(f"  (the team split the concept '{concept}' into the classes {', '.join(names)})")
        for cid in cl["concepts"]:
            c = by_id[cid]
            disagree = (" - sources disagree; the team decided" if cl["name"] in decided else " - SOURCES DISAGREE") \
                if c.get("conflict") else ""
            lines.append(f"- concept '{c['label']}'" + (f" (also: {', '.join(c['variants'][:5])})" if c["variants"] else "") +
                         f", {c['papers']} source(s)" + disagree)
            if c.get("definition"):
                lines.append(f"  consolidated: {c['definition']}")
            for s in [s for s in c["sources"] if s.get("definition")][:MODULE_SOURCE_DEFS]:
                broader = f" [broader: {s['broader']}]" if s.get("broader") else ""
                lines.append(f"  {cite(s['doc'])}: {s['definition'][:300]}{broader}")
            for d, s in _existing_terms(c, docs):
                lines.append(f"  existing term: {d['card'].get('title') or d['name']} <{s['uri']}>")
        if cl.get("parent"):
            lines.append(f"- below: {cl['parent']} (" + ("upper layer class" if cl["parent"] in _upper_names(session)
                                                          else "planned superclass") + ")")
        if cl.get("link"):
            lines.append(f"- linked to: {cl['link']} (" + ("same meaning" if cl.get("link_as") == "equivalent" else
                                                            "a kind of it") + "; the merge adds the link)")
        if cl.get("note"):
            lines.append(f"- planned as: {cl['note']}")
        elif not cl["concepts"]:
            lines.append("- (no material - model it from the key notion, the use case and the competency questions)")
        blocks.append("\n".join(lines))
    others = []
    for o in mod["other"]:
        labels = ", ".join([by_id[i]["label"] for i in o["concepts"]] + ([o["term"]] if o.get("term") else []))
        defs = "; ".join(_concept_definition(by_id[i])[:160] for i in o["concepts"] if _concept_definition(by_id[i]))
        ids = f"[{', '.join(o['concepts'])}] " if o["concepts"] else ""   # die Property traegt sie (DECISIONS 136)
        others.append(f"- {ids}{labels} -> " + (f"use the vocabulary term {o['ref']} directly (no own class), as parent, "
                                           "domain or range" if o.get("ref") else f"as {o['as'] or 'property'}") +
                      (f" ({o['hint']})" if o["hint"] else "") + (f": {defs}" if defs else ""))
    ids = {i for cl in mod["classes"] for i in cl["concepts"]} | {i for o in mod["other"] for i in o["concepts"]}
    rels = [r for r in (inv or {}).get("relations") or [] if r.get("subject_id") in ids or r.get("object_id") in ids][:40]
    other_classes = "\n".join(f"- {m['name']}: " + ", ".join(c["name"] for c in m["classes"])
                              for m in plan["modules"] if m["name"] != notion["name"]) or "(none)"
    pattern = next((p for p in momo.get("patterns") or [] if isinstance(p, dict) and p.get("notion") == notion["name"]
                    and p.get("pattern") and p.get("selected", True) is not False), None)
    pat_text = ""
    if pattern and find_pattern(pattern["pattern"]):
        pat_text = (f"\n\n**Design pattern to use as the module's template:** {pattern['pattern']}"
                    + (f"\n  keep: {pattern['keep']}" if pattern.get("keep") else "")
                    + (f"\n  change: {pattern['change']}" if pattern.get("change") else "")
                    + "\n" + pattern_template_text(find_pattern(pattern["pattern"])))
    std = ("\n\n**Standards to reuse:**\n" + "".join(f"- {s['name']} ({s.get('url', '')}): {s.get('reuse_hint', '')}\n"
                                                    for s in standards)) if standards else ""
    legend = "\n".join(f"- {d} = {doc_citation(docs[d])}" for d in used_docs if d in docs)
    cqs = "\n".join("- " + _cq_text(c) for c in momo.get("competency_questions") or [] if _cq_text(c)) or "(none)"
    task = (f"**Ontology:** {plan['ontology_name'] or 'see use case'}\n**Use case:**\n{_use_case(session, use_case)}"
            + _ctx(context) + f"\n\n**Competency questions of the whole ontology:**\n{cqs}"
            + f"\n\n**THIS module:** {notion['name']}" + (f" - {notion['description']}" if notion.get("description") else "")
            + pat_text + std
            + reuse_block(relevant_vocab_terms(session, [cl["name"] for cl in mod["classes"]] +
                                               [by_id[cid]["label"] for cl in mod["classes"] for cid in cl["concepts"]
                                                if cid in by_id] +
                                               [cl["note"] for cl in mod["classes"] if cl.get("note")]))
            + _data_block(session)
            + "\n\n**Planned classes of this module" + (", with the material from the sources" if inv else "") + ":**\n"
            + "\n\n".join(blocks)
            + ("\n\n**Notions to model as properties or individuals:**\n" + "\n".join(others) if others else "")
            + ("\n\n**Relations the sources state:**\n" + "\n".join(f"- {r['subject']} {r['relation']} {r['object']}"
                                                                for r in rels) if rels else "")
            + core_relation_block(approved_vocab(session))
            + links_block(approved_links(session), notion["name"])    # DECISIONS 148
            + (("\n\n**Upper layer** (exists in the ontology; never define these classes): " +
                ", ".join(_upper_names(session)) + ". A class you add that has no superclass in this module gets "
                "the upper class it is a kind of as its parent.") if use_upper_layer(session) else "")
            + f"\n\n**Classes of the OTHER modules (use them by their bare class name as domain/range, do not define them):**\n{other_classes}"
            + (f"\n\n**Sources:**\n{legend}" if legend else "")
            + "\n\nBuild this module.")
    return [{"role": "system", "content": MODULE_SYS}, {"role": "user", "content": task}]

def _fallback_class(cl, mod_name, by_id, lang="en") -> dict:
    """Klasse aus dem Plan, falls ihr Modul nicht erzeugt werden konnte oder sie dort fehlt."""
    concepts = [by_id[i] for i in cl["concepts"] if i in by_id]
    desc = next((_concept_definition(c) for c in concepts if _concept_definition(c)), "") or cl.get("note", "")
    docs = list(dict.fromkeys(s["doc"] for c in concepts for s in c["sources"]))
    label = concepts[0]["label"] if concepts else re.sub(r"(?<=[a-z])(?=[A-Z])", " ", cl["name"])
    return {"name": cl["name"], "labels": {lang: label}, "description": desc, "parent": None, "module": mod_name,
            "sources": docs, "see_also": []}

def _link_concepts(x, by_id):
    """Die Begriffe, fuer die ein Modul eine Property oder ein Individuum angelegt hat, wie bei Klassen als
    inventory_concepts (DECISIONS 136): sonst fand die Evaluation hasTaskStability nicht als "stability of the task"."""
    ids = [i for i in _ids(x.pop("concepts", None)) if i in by_id]
    if ids:
        x["inventory_concepts"] = list(dict.fromkeys(by_id[i]["label"] for i in ids))

def _one(v):
    """Ein Name aus der Antwort des Modells: eine Liste (mehrere Oberklassen, eine Vereinigung als Domain) gibt ihren
    ersten Namen - vorher brach die Generierung mit einem TypeError ab (Code-Review 2026-10-29)."""
    if isinstance(v, list):
        v = next((x for x in v if isinstance(x, str) and x.strip()), None)
    return v if isinstance(v, str) else None

def _list(v) -> list:
    """Eine Liste aus der Antwort des Modells; ein einzelner Wert wird zu einer Liste, alles andere zu keiner."""
    return v if isinstance(v, list) else [v] if isinstance(v, str) else []

def _ids(v) -> list:
    """Begriffs-IDs aus der Antwort, auch aus verschachtelten Listen (gruppierte Begriffe)."""
    out = []
    for x in v if isinstance(v, list) else [v]:
        out += _ids(x) if isinstance(x, list) else [x] if isinstance(x, str) else []
    return out

# ein Name (eigener oder mit Prefix) - was ein Modul sonst als Klasse schreibt ("(any)", "isPartOf some X"), macht
# den Turtle-Export unlesbar (VA-Laeufe 2 und 3b)
NAME_RE = re.compile(r"[A-Za-z_][\w.-]*(:[A-Za-z_][\w.-]*)?")

def merge_modules(plan, results, notions, session) -> tuple:
    """Fuehrt die Module zusammen: Namen eindeutig, fehlende geplante Klassen ergaenzt, Verweise auf nicht
    deklarierte Klassen als knappe Platzhalterklassen deklariert. Quellen-IDs werden zu Zitaten."""
    inv, docs, by_id = _inventory_parts(session)
    docs, by_id = docs or {}, by_id or {}
    momo = session.get("momo") or {}
    patterns = {p.get("notion"): p.get("pattern") for p in momo.get("patterns") or []
                if isinstance(p, dict) and p.get("pattern") and p.get("selected", True) is not False}
    allowed_uris = {s["uri"] for c in (inv or {}).get("concepts") or [] for s in c["sources"] if s.get("uri")}
    onto = {"modules": [], "classes": [], "properties": [], "individuals": [], "axioms": []}
    # Kernrelationen (DECISIONS 89): vom Team freigegeben, gelten fuer alle Module; ein Modul definiert sie nicht neu
    vocab = approved_vocab(session)
    core, core_skipped = core_names(vocab), []
    renames = {}             # Klassennamen, die _class_name geaendert hat (Code-Review 2026-10-29)
    restrictions = []        # Klassenrestriktionen der Module (Phase 5), geprueft, wenn alle Namen feststehen
    class_names, prop_names, ind_names = set(), set(core), set()
    report = {"modules": len(plan["modules"]), "planned_classes": sum(len(m["classes"]) for m in plan["modules"]),
              "fallback_classes": 0, "placeholder_classes": [], "module_errors": [], "inventory": bool(inv),
              "invalid_axioms": []}
    # welche Inventar-Begriffe der Plan einer Klasse zugeordnet hat - als Begriffe (nicht IDs) gespeichert, damit die
    # Evaluation die Abdeckung auch nach einem Neuaufbau des Inventars (neue IDs) berechnen kann
    planned_concepts = {cl["name"]: [by_id[i]["label"] for i in cl["concepts"] if i in by_id]
                        for m in plan["modules"] for cl in m["classes"]}
    for m in plan["modules"]:
        res = results.get(m["name"])
        notion = next(n for n in notions if n["name"] == m["name"])
        if isinstance(res, Exception) or not isinstance(res, dict):
            report["module_errors"].append({"module": m["name"], "error": f"{type(res).__name__}: {str(res)[:200]}"})
            res = {}
        info = res.get("module") if isinstance(res.get("module"), dict) else {}
        onto["modules"].append({"name": m["name"], "key_notion": notion["name"], "pattern": patterns.get(m["name"]),
                                "documentation": _plain(info.get("documentation")) or notion.get("description", "")})
        for c in res.get("classes") or []:
            if not isinstance(c, dict) or not _class_name(c.get("name")):
                continue
            if _class_name(c["name"]) != c["name"]:   # Wine_Region -> WineRegion: Verweise darauf spaeter nachziehen
                renames[str(c["name"])] = _class_name(c["name"])
            c["name"] = _class_name(c["name"])
            c["parent"] = _one(c.get("parent"))
            if c["name"] in class_names:
                continue
            c["module"] = m["name"]
            # nur Zeichenketten: eine Liste in einer Liste brach die Zusammenfuehrung ab (DECISIONS 168)
            c["sources"] = [s for s in _list(c.get("sources")) if isinstance(s, str) and s in docs]
            c["see_also"] = [u for u in _list(c.get("see_also")) if isinstance(u, str) and u in allowed_uris]
            if planned_concepts.get(c["name"]):
                c["inventory_concepts"] = planned_concepts[c["name"]]
            class_names.add(c["name"])
            onto["classes"].append(c)
        for cl in m["classes"]:
            if cl["name"] not in class_names:
                class_names.add(cl["name"])
                fallback = _fallback_class(cl, m["name"], by_id, label_languages(session)[0])
                if planned_concepts.get(cl["name"]):
                    fallback["inventory_concepts"] = planned_concepts[cl["name"]]
                onto["classes"].append(fallback)
                report["fallback_classes"] += 1
        for p in res.get("properties") or []:
            if isinstance(p, dict):   # eine Liste als Name, Inverse oder Oberproperty: ihr erster Name (DECISIONS 168)
                for key in ("name", "inverse_of", "sub_property_of"):
                    if key in p:
                        p[key] = _one(p[key])
            if isinstance(p, dict) and p.get("name") and (p["name"] in core or p.get("inverse_of") in core):
                core_skipped.append(f"{p['name']} ({m['name']})")     # eine eigene Fassung einer Kernrelation
                continue
            if isinstance(p, dict) and p.get("name") and p["name"] not in prop_names:
                p["module"] = m["name"]
                _link_concepts(p, by_id)
                for side in ("domain", "range"):    # "(any)" aus der Kernrelationen-Liste kopiert (VA-Lauf 2): = keine
                    p[side] = _one(p.get(side))
                    if isinstance(p.get(side), str) and not NAME_RE.fullmatch(p[side].strip()) or p.get(side) == "any":
                        p[side] = None
                prop_names.add(p["name"])
                onto["properties"].append(p)
        for i in res.get("individuals") or []:
            if isinstance(i, dict) and isinstance(i.get("name"), str) and i["name"] and i["name"] not in ind_names:
                i["class"] = _one(i.get("class"))
                _link_concepts(i, by_id)
                ind_names.add(i["name"])
                onto["individuals"].append(i)
        for a in res.get("axioms") or []:
            if isinstance(a, dict):
                classes = a.get("classes") or []
                # eine Restriktion als Klassenname ("isPartOf some X"): kann das Format noch nicht (PLAN.md Phase 5);
                # weniger als zwei verschiedene Klassen ist kein gueltiges OWL - HermiT lehnte die ganze Ontologie ab
                # (Wein 7-dsv41-a: DisjointClasses(RedWine, RedWine), DECISIONS 146)
                if not all(isinstance(c, str) and NAME_RE.fullmatch(c.strip()) for c in classes) or \
                        len({c.strip() for c in classes if isinstance(c, str)}) < 2 or \
                        (a.get("type") == "SubClassOf" and len(classes) != 2):
                    report["invalid_axioms"].append(f"{a.get('type')}({', '.join(map(str, classes))}) in {m['name']}")
                    continue
                a["module"] = m["name"]
                onto["axioms"].append(a)
        for r in res.get("restrictions") or []:
            if isinstance(r, dict):
                restrictions.append({**{k: _one(r.get(k)) for k in ("class", "property", "value")},
                                     "kind": r.get("kind"), "n": r.get("n"), "module": m["name"],
                                     "natural_language": _plain(r.get("natural_language"), 400)})
    if renames:      # ein Modul schrieb einen Klassennamen anders, als er gilt - sonst entstuende ein Platzhalter
        fix = lambda v: renames.get(v, v) if isinstance(v, str) else v
        for c in onto["classes"]:
            c["parent"] = fix(c.get("parent"))
        for p in onto["properties"]:
            p["domain"], p["range"] = fix(p.get("domain")), fix(p.get("range"))
        for i in onto["individuals"]:
            i["class"] = fix(i.get("class"))
        for a in onto["axioms"]:
            a["classes"] = [fix(x) for x in a.get("classes") or []]
        for r in restrictions:
            r["class"], r["value"] = fix(r.get("class")), fix(r.get("value"))
    upper = None
    if use_upper_layer(session):
        upper = ensure_upper_layer(onto, label_languages(session), upper_layer_of(session))
        class_names |= {c["name"] for c in onto["classes"] if c.get("layer") == "upper"}
    report["hierarchy"] = _apply_planned_parents(plan, onto)
    # SubClassOf-Axiome, die nur die Hierarchie (parent) wiederholen, blaehen die Axiomzahl auf (Wein-Lauf 2)
    parent = {c["name"]: c.get("parent") for c in onto["classes"]}
    kept = [a for a in onto["axioms"] if not (a.get("type") == "SubClassOf" and len(a.get("classes") or []) == 2
                                              and parent.get(a["classes"][0]) == a["classes"][1])]
    report["redundant_axioms"] = len(onto["axioms"]) - len(kept)
    onto["axioms"] = kept
    # ein SubClassOf-Axiom, das eine Klasse zusaetzlich unter eine zu ihrer Oberklasse disjunkte Klasse stellt, macht
    # sie unerfuellbar (Wein 7-luna-2: Vintage unter Process, als Axiom unter InformationObject) - es entfaellt, die
    # Hierarchie des Plans gilt (DECISIONS 142)
    report["disjoint_axioms"] = []
    for a in [a for a in kept if a.get("type") == "SubClassOf" and len(a.get("classes") or []) == 2]:
        rest = [x for x in onto["axioms"] if x is not a]
        conflict = _disjoint_conflict({**onto, "axioms": rest}, *a["classes"])
        if conflict:
            onto["axioms"] = rest
            report["disjoint_axioms"].append(f"{a['classes'][0]} below {a['classes'][1]} ({conflict})")
    report["reuse"] = _apply_planned_links(plan, onto)
    widened = []
    if vocab:
        props, widened = core_properties(vocab, class_names, label_languages(session))
        onto["properties"] = props + onto["properties"]
        ensure_core_module(onto)
    # eine Ober- oder Inverse-Property, die weder ein Modul noch die Kernrelationen deklarieren, oder eine andere Art
    # (VA 8-dsv41-dry: hasInteractionIntent unter "support", die Kernrelation heisst "supports"): HermiT lehnte die
    # ganze Ontologie ab - der Verweis entfaellt, wie bei den Edit-Operationen (DECISIONS 149)
    kinds = {p["name"]: p.get("type") or "ObjectProperty" for p in onto["properties"]}
    # die Verbindungen der Key Notions entstehen erst weiter unten; eine Modul-Property darunter (oder ihre Inverse)
    # ist kein Verweis ins Leere - der Modul-Prompt bittet darum (DECISIONS 166; VA 8-dsv41r-a und -c)
    links = approved_links(session)
    link_names = {x["name"] for x in links} - set(kinds)
    kinds.update({n: "ObjectProperty" for n in link_names})
    report["dangling_property_refs"] = []
    for p in onto["properties"]:
        for key, word in (("sub_property_of", "below"), ("inverse_of", "inverse of")):
            ref = p.get(key)
            if not ref or (isinstance(ref, str) and (":" in ref or ref == p["name"])):
                continue      # Vokabularbegriffe prueft der Export; sich selbst schreibt er nicht
            want = "ObjectProperty" if key == "inverse_of" else (p.get("type") or "ObjectProperty")
            if not isinstance(ref, str) or kinds.get(ref) != want:
                p[key] = None
                found = kinds.get(ref) if isinstance(ref, str) else None
                why = f"{'an' if found[0] in 'AEIOU' else 'a'} {found}" if found else "not declared"
                report["dangling_property_refs"].append(f"{p['name']} {word} {ref} ({why})")
    # eine Property mit zwei Inversen macht diese gleichwertig (Wein-Lauf 5): die zweite Erklaerung entfaellt
    by_prop = {p["name"]: p for p in onto["properties"]}
    report["inverse_conflicts"] = []
    for name, target, keep in inverse_conflicts(onto["properties"]):
        by_prop[name]["inverse_of"] = None
        report["inverse_conflicts"].append(f"{name} (declared inverse of {target}, which has {keep})")
    # Verweise auf Klassen, die kein Modul deklariert hat (ohne Prefix und kein xsd-Datentyp)
    def needs_stub(ref):
        return isinstance(ref, str) and ref and ":" not in ref and ref not in class_names and \
            re.match(r"^[A-Za-z_][\w-]*$", ref)
    refs = [(c.get("parent"), c["module"]) for c in onto["classes"]]
    refs += [(p.get(k), p["module"]) for p in onto["properties"] if p.get("type") == "ObjectProperty"
             for k in ("domain", "range")]
    refs += [(p.get("domain"), p["module"]) for p in onto["properties"] if p.get("type") != "ObjectProperty"]
    refs += [(i.get("class"), None) for i in onto["individuals"]]
    for ref, mod in refs:
        if needs_stub(ref):
            class_names.add(ref)
            onto["classes"].append({"name": ref, "labels": {label_languages(session)[0]: re.sub(r"(?<=[a-z])(?=[A-Z])", " ", ref)},
                                    "description": "Referenced by the module " + (mod or "") +
                                                   "; not yet specified.", "parent": None, "module": mod})
            report["placeholder_classes"].append(ref)
    if upper:   # leere obere Klassen wieder entfernen, wie die Aktion "Group root classes" (DECISIONS 69)
        removed = remove_unused_upper(onto, upper["created"])
        layer = {c["name"] for c in onto["classes"] if c.get("layer") == "upper"}
        names, anc = {c["name"] for c in onto["classes"]}, _ancestors(onto)
        # ausserhalb: ohne eigene Oberklasse und ohne Weg zur oberen Schicht - auch nicht ueber einen Vokabularbegriff
        # (User unter prov:Person mit prov:Person SubClassOf Agent liegt innerhalb, DECISIONS 132)
        report["upper_layer"] = {
            "used": sorted(layer), "removed": removed, "reused": upper["reused"],
            "renamed": plan.get("upper_renamed") or [],      # DECISIONS 159
            "outside": sorted(c["name"] for c in onto["classes"] if c["name"] not in layer
                              and c.get("parent") not in names and not (anc.get(c["name"], set()) & layer))}
    for c in onto["classes"]:
        c["sources"] = [doc_citation(docs[s]) for s in dict.fromkeys(c.get("sources") or []) if s in docs]
    # die Verbindungen zwischen den Key Notions, vom Team freigegeben (DECISIONS 148) - vor den Restriktionen der
    # Module: die Module kennen sie aus ihrem Prompt und verwenden sie darin; danach angelegt, wurden diese
    # Restriktionen als "unknown property" abgelehnt (Compliance-Demo 2026-11-06, DECISIONS 150)
    every = []
    if links:
        onto, report["notion_links"], every = add_notion_links(onto, links, vocab, label_languages(session),
                                                               notion_modules(session))
    # eine Verbindung, die nicht angelegt werden konnte (Key Notion fehlt): Verweise darauf entfallen wie oben
    declared = {p["name"] for p in onto["properties"]}
    for p in onto["properties"]:
        for key, word in (("sub_property_of", "below"), ("inverse_of", "inverse of")):
            if p.get(key) in link_names and p[key] not in declared:
                report["dangling_property_refs"].append(f"{p['name']} {word} {p[key]} (a key notion link that was not created)")
                p[key] = None
    if restrictions:   # wie Edit-Operationen: Namen, Domain und Range, Zahlen - was nicht passt, steht im Bericht
        onto, rep = apply_edits(onto, [{"op": "add_restriction", **r} for r in restrictions],
                                label_languages(session)[0], known_prefixes(session), session_vocab(session))
        report["restrictions"] = {"written": len(restrictions), "added": len(rep["applied"]),
                                  "rejected": [x["reason"] for x in rep["rejected"]][:40]}
    if every:   # "gilt fuer jede Instanz": Restriktionen wie die der Module, danach mit dem Reasoner geprueft
        onto, rep = apply_edits(onto, [{"op": "add_restriction", **r} for r in every],
                                label_languages(session)[0], known_prefixes(session), session_vocab(session))
        report["notion_links"]["restrictions"] = len(rep["applied"])
        report["notion_links"]["restrictions_rejected"] = [x["reason"] for x in rep["rejected"]][:20]
        report.setdefault("restrictions", {"written": 0, "added": 0, "rejected": []})
    report["classes"] = len(onto["classes"])
    report["properties"] = len(onto["properties"])
    if vocab:
        report["core_relations"] = {**check_core_relations(onto, vocab), "skipped": core_skipped, "widened": widened}
    return onto, report

MISSING_STEP = "Missing central concepts (after the modules)"

def missing_after_modules(session, llm_config, onto, plan) -> tuple:
    """Zentrale Begriffe, die nach den Modulen fehlen, obwohl der Plan sie nicht ausgeschlossen hat (DECISIONS 136;
    VA 6a-6c: 3-8 je Lauf, z.B. chunking, feedback loop, scope of the task): derselbe Schritt wie die Aktion "Add
    missing central concepts", in Paketen und nur, wenn etwas fehlt. Was das Modell bewusst nicht modelliert, gilt
    als entschieden, wie bei der Aktion."""
    from improvements import GAP_CONCEPT_INTRO, GAP_CONCEPTS_PER_BATCH, _gap_concept_text, link_new_classes
    from editing import edit_ontology
    from ontology_evaluation import ConceptIndex
    inv, docs, _ = _inventory_parts(session)
    gap = session.get("gap_decisions") or {}
    excluded = set(plan.get("excluded") or {})
    idx = ConceptIndex(onto, concept_key)
    cids = central_ids(inv)
    todo = [c for c in inv["concepts"] if c["id"] in cids and c["id"] not in excluded
            and not idx.class_of(c) and not idx.other_of(c)
            and not any(concept_key(v) in gap for v in [c["label"], *c.get("variants", [])])]
    report = {"missing": [c["label"] for c in todo], "added": [], "declined": 0, "errors": []}
    for i in range(0, len(todo), GAP_CONCEPTS_PER_BATCH):
        part = todo[i:i + GAP_CONCEPTS_PER_BATCH]
        texts = "\n".join(_gap_concept_text(c, docs or {}, idx) for c in part)
        before = onto
        try:
            onto, edit = edit_ontology(session, llm_config, onto, GAP_CONCEPT_INTRO + texts, MISSING_STEP, focus_text=texts)
        except OPTIONAL_STEP_ERRORS as ex:     # ohne den Schritt weiter; die Aktion in Schritt 9 kann ihn nachholen
            report["errors"].append(str(getattr(ex, "detail", ex))[:200])
            continue
        link_new_classes(before, onto, [c["label"] for c in part], inv)
        store = session.setdefault("gap_decisions", {})
        for s in edit.get("skipped") or []:
            if concept_key(s.get("item")):
                store[concept_key(s["item"])] = s.get("reason") or "not modeled"
                report["declined"] += 1
    after = ConceptIndex(onto, concept_key)
    report["added"] = [c["label"] for c in todo if after.class_of(c) or after.other_of(c)]
    return onto, report

INCONSISTENT = "(the ontology is inconsistent)"

def _unsatisfiable(session, onto, errors=None):
    """Unerfuellbare Klassen laut HermiT (INCONSISTENT, wenn die Ontologie widerspruechlich ist), oder None, wenn der
    Reasoner nicht laeuft - dann steht sein Fehler, falls er einen meldet, in errors."""
    from ontology_evaluation import reasoner_check
    from ontology_io import ontology_to_turtle
    from vocabularies import turtle_for_reasoning
    turtle = ontology_to_turtle(onto, session.get("_standards", []), session_prefixes(session, onto))
    r = reasoner_check(turtle_for_reasoning(session, turtle))
    o = r.get("ontology") or {}
    if not r.get("available") or o.get("error"):
        if errors is not None:
            errors.append(str(o.get("error") or r.get("reason") or "")[:300])
        return None
    return {INCONSISTENT} if o.get("consistent") is False else set(o.get("unsatisfiable") or [])

RESTRICTION_SEARCH_RUNS = 24   # hoechstens so viele Reasoner-Laeufe fuer die Suche (DECISIONS 161)
RESTRICTION_CHUNKS = 8         # in so viele Pakete wird zuerst geteilt

def _consistent_restrictions(session, onto, base) -> tuple:
    """Macht die Ontologie erst mit den Restriktionen widerspruechlich, werden die verantwortlichen gesucht
    (DECISIONS 161): paketweise dazu, was mit den bisher behaltenen widerspruchsfrei bleibt, bleibt; ein Paket, das den
    Widerspruch bringt, wird halbiert, bis die einzelne Restriktion gefunden ist. Nach RESTRICTION_SEARCH_RUNS Laeufen
    bleibt der ungepruefte Rest weg. Gibt (behalten, entfernt, Laeufe, ungeprueft) zurueck."""
    restrictions = list(onto["restrictions"])
    size = max(1, -(-len(restrictions) // RESTRICTION_CHUNKS))
    todo = [restrictions[i:i + size] for i in range(0, len(restrictions), size)]
    kept, dropped, untested, runs = [], [], [], 0
    while todo:
        chunk = todo.pop(0)
        if runs >= RESTRICTION_SEARCH_RUNS:
            untested += chunk
            continue
        runs += 1
        found = _unsatisfiable(session, {**onto, "restrictions": kept + chunk})
        if found is None:       # ein gescheiterter Lauf sagt nichts ueber das Paket: halbiert neu versuchen, eine
            if len(chunk) == 1:  # einzelne Restriktion bleibt ungeprueft (DECISIONS 166, 167) - nie ein ganzes
                untested += chunk  # Paket wegen einer einzigen Zeitueberschreitung
            else:
                todo[:0] = [chunk[:len(chunk) // 2], chunk[len(chunk) // 2:]]
            continue
        if INCONSISTENT not in found - base:
            kept += chunk
        elif len(chunk) == 1:
            dropped += chunk
        else:
            todo[:0] = [chunk[:len(chunk) // 2], chunk[len(chunk) // 2:]]
    return kept, dropped + untested, runs, untested

def drop_unsatisfiable_restrictions(session, onto) -> tuple:
    """Die Restriktionen der Module gegen den Reasoner (DECISIONS 125): macht eine Klassen unerfuellbar, die es ohne
    die Restriktionen nicht sind, werden die Restriktionen dieser Klassen, ihrer Oberklassen und auf sie entfernt und
    berichtet - ohne weiteren Modellaufruf. Hoechstens zwei Runden; was dann noch bleibt, meldet der Bericht."""
    errors = []
    found = _unsatisfiable(session, onto, errors)
    if found is None:                   # kein Java, oder der Reasoner lehnt die Ontologie ab: sein Grund im Bericht
        return onto, {"checked": False, "removed": [], "error": errors[0] if errors else ""}
    if not found:
        return onto, {"checked": True, "removed": []}
    base = _unsatisfiable(session, {**onto, "restrictions": []}, errors)
    if base is None:    # ohne Vergleich gilt jede unerfuellbare Klasse als neu - nichts entfernen (DECISIONS 166)
        return onto, {"checked": False, "removed": [], "still_unsatisfiable": sorted(found),
                      "error": "the reasoner run without the restrictions failed: " + (errors[0] if errors else "")}
    removed, search = [], None
    for _ in range(2):
        new = found - base
        if not new:
            break
        if INCONSISTENT in new:     # die verursachenden Restriktionen suchen, statt alle zu entfernen (DECISIONS 161)
            _, drop, runs, untested = _consistent_restrictions(session, onto, base)
            search = {"runs": runs, "untested": [restriction_label(r) for r in untested]}
        else:
            anc = _ancestors(onto)
            hit = set(new) | {a for n in new for a in anc.get(n, ())}
            drop = [r for r in onto["restrictions"] if r.get("class") in hit or r.get("value") in new]
        if not drop:
            break
        removed += drop
        onto["restrictions"] = [r for r in onto["restrictions"] if not any(r is d for d in drop)]
        found = _unsatisfiable(session, onto, errors)
        if found is None:   # ein gescheiterter Lauf heisst nicht "nichts mehr unerfuellbar" (DECISIONS 166)
            break
    out = {"checked": found is not None, "removed": [restriction_label(r) for r in removed],
           "still_unsatisfiable": sorted(found - base) if found is not None else []}
    if found is None:
        out["error"] = "the reasoner run after the removal failed: " + (errors[-1] if errors else "")
    if search:
        out["search"] = search
    return onto, out

def reasoner_repairs(session, onto, report) -> dict:
    """Die beiden Reparaturen mit dem Reasoner, in dieser Reihenfolge (DECISIONS 158): erst unerfuellbare Klassen aus
    Axiomen und Anbindungen, OHNE die Restriktionen (DECISIONS 147), dann die Restriktionen (DECISIONS 125). Umgekehrt
    machten die Restriktionen eine schon unerfuellbare Klasse inkonsistent, und die Pruefung entfernte alle
    Restriktionen fuer einen Fehler, den eine Anbindung verursacht hatte (VA dry3: 67 von 67)."""
    restrictions = onto.get("restrictions") or []
    onto, report["unsatisfiable"] = repair_unsatisfiable(session, {**onto, "restrictions": []})
    onto = {**onto, "restrictions": restrictions}
    if restrictions:                    # was Klassen unerfuellbar macht, wird entfernt und berichtet
        onto, report.setdefault("restrictions", {})["reasoner"] = drop_unsatisfiable_restrictions(session, onto)
    return onto

UNSAT_REPAIR_RUNS = 12          # hoechstens so viele Reasoner-Laeufe fuer die Suche nach dem verursachenden Axiom

def _axiom_label(a) -> str:
    return f"{a.get('type')}({', '.join(map(str, a.get('classes') or []))})"

def repair_unsatisfiable(session, onto) -> tuple:
    """Klassen, die nach der Generierung unerfuellbar sind, auch ohne Restriktionen (DECISIONS 147; Wein runde 7:
    "every Wine is a FoodOn red wine" machte WhiteWine und RoseWine unerfuellbar, eine Gleichsetzung mit FoodOn
    Meal). Die Axiome, die eine solche Klasse oder ihre Oberklassen nennen, werden einzeln probeweise entfernt -
    Anbindungen an Vokabulare zuerst, dann Unterklassen-, Gleichsetzungs- und Disjunktheits-Axiome der Module; die
    der oberen Schicht bleiben. Macht das Entfernen Klassen erfuellbar, ohne neue unerfuellbar zu machen, bleibt das
    Axiom weg. Hoechstens UNSAT_REPAIR_RUNS Reasoner-Laeufe; was bleibt, steht im Bericht."""
    own = {c["name"] for c in onto.get("classes") or []}
    errors = []
    found = _unsatisfiable(session, onto, errors)
    if found is None:
        return onto, {"checked": False, "error": errors[0] if errors else "", "unsatisfiable": [], "removed": [],
                      "still_unsatisfiable": []}
    # widerspruechlich: meist Individuen einer unerfuellbaren Klasse (DeepSeek V4.1, Wein: Individuen von Meal,
    # Country, WineRegion, WineGrape) - dann nennt der Reasoner keine Klasse. Die Ursache wird an den Klassen allein
    # gesucht (ohne Individuen), danach mit ihnen noch einmal geprueft
    inconsistent = INCONSISTENT in found
    probe = (lambda o: {**o, "individuals": []}) if inconsistent else (lambda o: o)
    if inconsistent:
        found = _unsatisfiable(session, probe(onto))
        if found is None or INCONSISTENT in found:
            return onto, {"checked": True, "inconsistent": True, "still_inconsistent": True, "unsatisfiable": [],
                          "removed": [], "still_unsatisfiable": []}
    unsat = found & own
    rep = {"checked": True, "inconsistent": inconsistent, "unsatisfiable": sorted(unsat), "removed": [],
           "still_unsatisfiable": sorted(unsat)}
    if not unsat:
        rep["still_inconsistent"] = inconsistent
        return onto, rep
    anc = _ancestors(onto)
    touched = set(unsat) | {a for n in unsat for a in anc.get(n, ())}
    # "a kind of" vor "same meaning": ein falsches SubClassOf gibt einer Klasse eine unerwartete Oberklasse (Wein
    # 7-dsv41-b: Wine unter FoodOn red wine); zuerst probiert, entfernte es sonst die richtige Gleichsetzung RedWine
    order = {"SubClassOf": 1, "EquivalentClasses": 2, "DisjointClasses": 3}
    cands = [a for a in onto.get("axioms") or [] if a.get("type") in order and a.get("module") != "UpperLayer"
             and touched & set(a.get("classes") or [])]
    cands.sort(key=lambda a: (0 if any(":" in str(c) for c in a.get("classes") or []) else 1, order[a["type"]]))
    runs = 0
    for a in cands:
        if not unsat or runs >= UNSAT_REPAIR_RUNS:
            break
        trial = {**onto, "axioms": [x for x in onto["axioms"] if x is not a]}
        runs += 1
        after = _unsatisfiable(session, probe(trial))
        if after is None or INCONSISTENT in after:
            continue
        after &= own
        if after < unsat:               # weniger unerfuellbar und nichts Neues
            onto, unsat = trial, after
            rep["removed"].append(_axiom_label(a))
    rep.update(still_unsatisfiable=sorted(unsat), reasoner_runs=runs + 1)
    if inconsistent:                    # mit den Individuen noch einmal
        final = _unsatisfiable(session, onto)
        rep["still_inconsistent"] = final is None or INCONSISTENT in final
        rep["reasoner_runs"] += 1
    return onto, rep

def generate_modular(session, llm_config, standards, context, use_case=None) -> tuple:
    """Plan -> Module (parallel) -> Zusammenfuehrung. Liefert (onto, report). use_case: die Beschreibung aus dem
    Generierungsschritt (mit den zusaetzlichen Anforderungen), sonst der gespeicherte Use Case."""
    import concurrent.futures
    momo = session.get("momo") or {}
    notions = named_notions(momo.get("key_notions"))
    inv, _, _ = _inventory_parts(session)
    with usage_step("Module plan"):
        plan = clean_plan(llm.call_llm_json(llm_config, build_plan_prompt(session, notions, context, use_case)),
                          notions, inv, _upper_names(session))
    if not plan["modules"]:
        raise HTTPException(status_code=502, detail="The plan contains no modules - the model's answer was empty or "
                                                    "not in the expected format. Generate again.")
    proposed = not notions
    if proposed:      # die Module hat der Plan vorgeschlagen
        notions = [{"name": m["name"], "description": m["description"]} for m in plan["modules"]]
    decided = apply_to_plan(plan, session)   # die entschiedenen Definitionen legen Klassen fest (DECISIONS 83)
    if inv:
        complete_plan(session, llm_config, plan, inv)   # jeder zentrale Begriff geplant oder begruendet ausgeschlossen
        grow_plan(session, llm_config, plan, inv)       # ein viel zu kleiner Plan bekommt einen Nachtrag (DECISIONS 147)
    cands = link_candidates(session, plan)    # Anbindung an geladene Vokabulare (DECISIONS 101)
    if cands:
        with usage_step("Vocabulary links"):
            try:
                result = llm.call_llm_json(llm_config, build_link_prompt(session, plan, cands))
            except OPTIONAL_STEP_ERRORS as ex:   # ohne Anbindungen weiter; die Align-Aktion kann sie nachholen
                result, plan["reuse_error"] = {}, str(getattr(ex, "detail", ex))[:300]
        apply_links(session, plan, result, cands)
        if plan.get("reuse_error"):          # kein Ergebnis ist keine Ablehnung: nichts als Entscheidung merken
            plan["link_declined"] = {}
    def run(notion):
        with usage_step("Module: " + notion["name"]):
            return llm.call_llm_json(llm_config, build_module_prompt(session, notion, plan, standards, context,
                                                                     use_case))
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MODULE_WORKERS) as pool:
        # copy_context: die Threads sollen ihren Verbrauch in das Log dieser Anfrage schreiben
        futures = {pool.submit(contextvars.copy_context().run, run, n): n["name"] for n in notions}
        for f in concurrent.futures.as_completed(futures):
            try:
                results[futures[f]] = f.result()
            except Exception as ex:
                results[futures[f]] = ex
    if all(isinstance(r, Exception) for r in results.values()):
        first = next(iter(results.values()))
        if isinstance(first, HTTPException):
            raise first
        raise HTTPException(status_code=500, detail=f"No module could be generated: {type(first).__name__}: {first}")
    onto, report = merge_modules(plan, results, notions, session)     # mit den Key-Notion-Links (DECISIONS 148, 150)
    store = decision_store(session, "align")       # "keine Anbindung" gilt auch fuer die Align-Aktion (DECISIONS 102)
    for name, reason in (plan.get("link_declined") or {}).items():
        store[name] = {"item": name, "reason": reason}
    if session.get("vocabularies"):     # obere Schicht, Klassen der Module, Properties (DECISIONS 105)
        onto, report["reuse"]["after_modules"] = link_after_modules(session, llm_config, onto)
    # vom Plan abgelehnte Oberbegriffe: "Build hierarchy" fragt sie nicht noch einmal (DECISIONS 103) - mit dem
    # Schluessel der Aktion ("A is a kind of B", normalisiert)
    store = decision_store(session, "hierarchy")
    for d in plan.get("hierarchy_declined") or []:
        item = f"{d['narrower']} is a kind of {d['broader']}"
        store[_norm(item)] = {"item": item, "reason": d["reason"]}
    report["hierarchy"]["declined"] = len(plan.get("hierarchy_declined") or [])
    if inv:                             # Oberbegriffe der Literatur, die die Module nicht umsetzen (DECISIONS 111)
        onto, report["hierarchy"]["after_modules"] = hierarchy_after_modules(session, llm_config, onto)
    vocab = approved_vocab(session)
    if vocab and report.get("core_relations"):   # Relationen der Module unter die Kernrelationen (DECISIONS 112)
        onto, after = core_after_modules(session, llm_config, onto, vocab)
        report["core_relations"].update(check_core_relations(onto, vocab), after_modules=after)
    if inv:     # zentrale Begriffe, die nach den Modulen noch fehlen (DECISIONS 136)
        onto, report["central_after_modules"] = missing_after_modules(session, llm_config, onto, plan)
    onto = reasoner_repairs(session, onto, report)
    if inv:     # ausgeschlossene zentrale Begriffe: die Aktion "Add missing central concepts" fragt nicht noch einmal
        by_id = {c["id"]: c for c in inv["concepts"]}
        gap = session.setdefault("gap_decisions", {})
        for cid, reason in (plan.get("excluded") or {}).items():
            gap[concept_key(by_id[cid]["label"])] = reason
        report["central"] = plan.get("central_report")
        report["plan_size"] = plan.get("size_report")
    report["decided_plan"] = decided
    report["modules_proposed"] = proposed
    slug = re.sub(r"[^a-z0-9]+", "-", (plan["ontology_name"] or "ontology").lower()).strip("-") or "ontology"
    onto.update({"namespace": f"https://example.org/{slug}#", "ontology_name": plan["ontology_name"] or "Ontology",
                 "license": plan["license"], "summary": plan["summary"]})
    return onto, report
