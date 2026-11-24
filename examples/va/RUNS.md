# Measurement runs of the visual analytics (VA) project

The VA project is the case study of the full workflow: 54 papers, a concept inventory of 1,395 concepts (264 central,
i.e. with two or more sources), 329 taxonomies, ten key notions, ten competency questions, PROV-O, SKOS, Data Cube and
DCAT loaded as vocabularies ("use terms directly"). The project data are not in the repository (`data/` is ignored);
the runs are recorded here. Targets: [PLAN.md](../../PLAN.md), phase 3, "Success (measurement run)".

## Run 1 - 2026-10-28, gpt-6-sol, commit ce0ad1c (phase 3 complete: DECISIONS 89-104)

**Setup.** The baseline is the project "Visualization Analytics Core Ontology" (`c7323784`) after generation and all
repair actions (iteration 6, evaluated 2026-10-16), the version PLAN.md's table describes. It was exported and imported
as "VA measurement run 1 (phase 3)" (`b151f9fe`); in the copy, the repairs' decisions (29 declined concepts, 89
hierarchy relations, 3 upper-layer, 40 link and 49 property decisions) and the core vocabulary derived from the old
ontology were removed, so the run does not inherit knowledge from the repairs. Then: core relations proposed from the
literature in step 7 and approved unchanged (41 relations), regenerated, CQ tests, evaluation with hold-out questions.
**No repair action was run.**

**Generation report:** 10 modules, 219 planned classes (218 with a planned superclass) -> 234 classes and 122
properties; **central concepts: 264 - 259 placed by the plan, 5 added by the completion call, 47 excluded with a
reason, none left open**; 12 broader/narrower relations of the literature declined by the plan; upper layer: Process,
Agent, InformationObject, Specification, Quality used, PhysicalObject removed, no top class outside; vocabulary links:
8 planned classes with candidates, 1 link (`UncertaintyAwareDataset -> dcat:Dataset`), 1 term used instead of a class
(`Dataset -> dcat:Dataset`), 6 declined; core relations: 17 module properties below them, 42 without one, no
violation.

| | Baseline (after all repairs) | Run 1 (no repair) | Target (PLAN.md) | |
|---|---|---|---|---|
| **Input tokens** | ~2.8 M for generation and repairs (3.66 M for the whole project) | **~271k** for the whole run, incl. CQ and hold-out tests | well below 1 M | met (-90 %) |
| Top-level relations | 112 | **82** | about 70 or fewer | close |
| Root classes | 7 | **5** (4 upper classes + 1) | about 10 or fewer | met |
| Links to reused vocabularies | 13 (PROV-O) | **6** (PROV-O, DCAT) | at least as many | **not met** |
| Central concepts as a class | 76.5 % (202) | **78.0 %** (206); represented 98.9 %, 43 deliberately excluded, 3 missing | at least as good, without "Add missing concepts" | met |
| Broader/narrower relations realized | 99 of 153 (64.7 %) | 90 of 139 (**64.7 %**) | at least as good, without "Build hierarchy" | same share |
| Competency questions full | 10 / 10; **8 / 10 (2 partial) with the current test** | 8 / 10 (2 partial) | at least as good | met |
| Hold-out questions full | 7 / 10; **5 / 10 (4 partial, 1 none) with the current test** | 3 / 10 (6 partial, 1 none) | at least as good | 2 fewer, see below |

Further figures:

| | Baseline | Run 1 |
|---|---|---|
| Classes / object / datatype properties / individuals / axioms | 345 / 301 / 14 / 5 / 45 | 234 / 108 / 14 / 9 / 16 |
| Relations / with a superproperty | 187 / 77 | 100 / 18 |
| Hierarchy depth (max / mean) | 6 / 3.29 | 7 / 3.06 |
| Sibling groups with disjointness | 16 of 54 | 5 of 34 |
| Properties without domain or range | 23 | 0 |
| Classes linked to the inventory / untraceable | 68.4 % / 0.9 % | **90.6 %** / 0.4 % |
| Reasoner | consistent | consistent, also with the sample data |
| What the repairs would still offer | - | Align: 20 classes with candidates; Build hierarchy: 49 relations; Add missing: 3 concepts; Group root classes: none |

Tokens per step: core-relation proposal ~7k; plan 38.6k / 13.5k; completion 1.3k / 0.6k; vocabulary links 0.9k / 0.8k;
ten modules 116k / 45k (8-14k input each); CQ tests 53.9k / 6.7k; hold-out tests 53.8k / 4.6k.

### Findings

1. **The cost target is met by far**: about 271k input tokens for proposal, generation, CQ and hold-out tests, against
   about 2.8 M for generation and repairs before. The plan prompt with broader terms, taxonomies and the central-concept
   rule costs 38.6k tokens; the completion and link calls together 2k.
2. **Coverage without repairs is at least as good as with them**: every central concept placed or excluded with a
   reason (none open), 78.0 % as classes against 76.5 %, 90.6 % of the classes linked to inventory concepts against
   68.4 %; the literature's hierarchy realized to the same share (64.7 %) without "Build hierarchy".
3. **Vocabulary links fall short**: 6 against 13. The link step found candidates for only 8 of 219 planned classes -
   it matches the planned class *name*, while the align action matched classes with their labels after generation.
   Modules created properties named like PROV-O terms (`used`, `generatedBy`, `wasDerivedFrom`) without linking them,
   since the link step only links classes. "Align" would still offer 20 classes.
4. **The CQ results are not comparable as they stand**: the baseline was tested on 2026-10-16, before the CQ test
   learned to report partial answers (DECISIONS 91, 95, 96), and it had reused and extended its sample data and
   queries over six iterations. The run's partial results come from the authors' "leaves out" statements, several of
   which ask more than the question does ("whether the returned agent is an Infovis system") - the over-reporting seen
   in the wine runs. A fair comparison needs the baseline tested again with the current test - done below.
5. **Leaner, with fewer axioms**: 234 instead of 345 classes, 108 instead of 301 object properties, no property
   without domain or range; but 16 instead of 45 axioms, and disjointness in 5 instead of 16 sibling groups.
6. **Core relations are broad**: 30 of 41 relate "any" to "any"; top-level relations 82, not yet the ~70 aimed at.

### Baseline retested with the current CQ test

A copy of the baseline export ("VA baseline CQ retest", `292f8fe0`) was evaluated from scratch on 2026-10-28 with
gpt-6-sol: new sample data and queries for the competency and hold-out questions, the CQ test of DECISIONS 91-96. The
ontology was not changed; all other figures are the baseline's.

| Question | Baseline, current test | Run 1 |
|---|---|---|
| Competency questions | 8 full, 2 partial | 8 full, 2 partial |
| - filtering, selection, zooming in coordinated views | partial (before/after contents of the views) | partial (resulting extent, level of detail) |
| - evaluating a design, validation | partial (adequacy criteria, outcome) | full |
| - mapping attributes to marks and channels | full | partial (the sample data had no position mapping) |
| Hold-out questions | 5 full, 4 partial, 1 none | 3 full, 6 partial, 1 none |
| - techniques supporting an analytic goal | full | partial: "whether depicting the task's target data makes the representation suitable" |
| - intents an Infovis system supports | full | partial: "whether the returned agent is an Infovis system and whether it offers, rather than merely uses, the technique" |
| - information-seeking problems per data type; inherent uncertainty; tracking items; composition operators | partial | partial |
| - components of a Vega-Lite unit specification | none | none |

**Result.** With the same test the baseline drops from 10 to 8 full competency questions and from 7 to 5 full hold-out
questions: most of the earlier gap was the measurement. The competency questions are now even (8 / 2 / 0 each, with
one different question partial on each side - one of them caused by the sample data, not the ontology). On the
hold-out questions run 1 is two behind, and both differences are "leaves out" statements about judgements (whether a
representation is *suitable*, whether a system *is* an Infovis system) of the kind DECISIONS 91 meant to exclude; the
baseline's run of the test happened not to make them. Every test is a single run of a non-deterministic model, so a
difference of one or two questions is within the noise; the hold-out question no version answers (Vega-Lite) needs a
concept neither ontology has.

### Follow-ups (proposed)

- Link step: match planned classes also by their concepts' labels and variants and the planned note; link
  properties too (subPropertyOf a vocabulary property, e.g. PROV-O's `used`, `wasGeneratedBy`). **Done: DECISIONS
  105, measured in run 2.**
- CQ test: "leaves out" statements that only doubt a judgement or a type the query already asks for still count as
  partial (both hold-out differences above); the rule of DECISIONS 91 needs a sharper wording or a check.
- Disjointness: ask the modules for DisjointClasses among sibling classes that cannot share instances (OOPS! P10).

## Run 2 - 2026-10-28, gpt-6-sol, commit 0700ee0 (vocabulary links, DECISIONS 105)

**Setup.** As run 1: a new copy of the same baseline export ("VA measurement run 2 (vocabulary links)", `cdf6597c`),
the repairs' decisions removed. Run 1's approved core relations (41) were copied into it unchanged, so that the
generation differs from run 1 only by the code. Regenerated, CQ tests, evaluation with hold-out questions; no repair.
**One manual fix:** two module properties had the range "(any)", copied from the listing of the core relations, and
the Turtle export wrote `:(any)` - the CQ test could not parse it (the generation's syntax-fix call, 9.9k tokens,
did not repair it either). The two ranges were cleared in the project file, which is what the merge does since the
fix in DECISIONS 105 ("Fixed with 105").

**Links to vocabularies.** After planning: candidates for 20 planned classes (run 1: 8) - the labels and variants of
the concepts find more - but no link: 18 declined, mostly with reasons about DCAT's narrower meaning ("a collection of
data items need not meet DCAT's publication, curation, and access requirements"), and 2 classes replaced by a term:
`TaskTarget -> prov:Entity`, `AnnotationActivity -> prov:Activity`. After the modules: 25 terms with candidates, 7
linked (`Agent`, `EntityWithProvenance`, `ProvenanceActivity` as subclasses of `prov:Agent`, `prov:Entity`,
`prov:Activity`; `attributedTo`, `generatedBy`, `used`, `wasDerivedFrom` as subproperties of their PROV-O
counterparts), 18 declined, none refused. The modules linked 3 more classes to `prov:Person` themselves.

| | Baseline | Run 1 | Run 2 |
|---|---|---|---|
| Input tokens of the run (generation, CQ, hold-out) | ~2.8 M (with repairs) | 264k (+7k core proposal) | 264k (incl. 2.6k for the new link call and 9.9k syntax fix) |
| **Links to reused vocabularies** | 13 (PROV-O) | 6 (PROV-O, DCAT) | **11** (PROV-O): 6 class links, 4 subproperties, 1 domain `prov:Activity` |
| Top-level relations | 112 | 82 | 87 |
| Root classes | 7 | 5 | 4 |
| Central concepts as a class | 76.5 % | 78.0 % (43 decided, 3 missing) | **68.9 %** (65 decided, 2 missing); represented 99.2 % |
| Broader/narrower relations realized | 64.7 % (99/153) | 64.7 % (90/139) | **51.3 %** (61/119) |
| Competency questions full / partial / none | 8 / 2 / 0 (current test) | 8 / 2 / 0 | 6 / 4 / 0 |
| Hold-out questions full / partial / none | 5 / 4 / 1 (current test) | 3 / 6 / 1 | 2 / 6 / 2 |
| Classes / object / datatype properties / axioms | 345 / 301 / 14 / 45 | 234 / 108 / 14 / 16 | 212 / 108 / 10 / 20 |
| Planned classes / central concepts excluded by the plan | - | 219 / 47 | 194 / 70 |
| Reasoner | consistent | consistent | consistent, also with the sample data |
| What "Align" would still offer | - | 20 | 0 |

### Findings

1. **The link step works**: 11 links instead of 6, at 2.6k tokens; together with the baseline's 13 - which needed the
   align repair - within reach. Nothing is left for "Align": everything with a candidate is linked or declined with a
   reason. The model declines DCAT for general data and dataset classes, as the careful rules of DECISIONS 102 ask.
2. **"Use the term" replaced classes by broader terms**: `TaskTarget` and `AnnotationActivity` disappeared in favour of
   `prov:Entity` and `prov:Activity`. The rule for `use` (DECISIONS 101) says the term replaces the class, but not
   that it must mean the same; a broader term should give a subclass.
3. **The run differs from run 1 far more than the code change explains.** The plan prompt was the same (the link step
   runs after it), yet the plan has 194 instead of 219 classes and excluded 70 instead of 47 central concepts -
   among them domain concepts from the literature's uncertainty taxonomy ("Usage Uncertainty", "Ignorance",
   "Incomplete Knowledge", "Nonrepresentative Sampling") and "overplotting", "sensitivity analysis methods". Central
   concepts as classes fall from 78.0 % to 68.9 %, the realized hierarchy from 64.7 % to 51.3 %, and the competency
   questions from 8 to 6 full. A single generation is not a measurement: the model's variance between two runs of the
   same plan prompt is larger than most effects measured so far.
4. **An invalid range broke the export**: the generation's own syntax check sent the Turtle to the model, which could
   not fix `:(any)` - now prevented in the merge (DECISIONS 105).

### Follow-ups (proposed)

- `use` only for a term with the same meaning; a broader term gives `subclass` (prompt rule in the link call).
  **Done: DECISIONS 106** (with a server check: same name or label).
- Measure with three generations per configuration (PLAN.md phase 6 plans "evaluate 3x"; it is needed now): mean and
  spread of central coverage, hierarchy, links and CQ results, so that a change is judged against the variance.
- Exclusions of central concepts: the plan rule allows "out of scope or specific to one paper"; concepts that belong
  to a taxonomy of the literature, or that the competency questions name, should not be excluded without a stronger
  reason - or the exclusions should be reviewed by the completion call.

## Runs 3a-3c - 2026-10-28, gpt-6-sol, commit b84cbab (three generations of one configuration)

**Setup.** Three new copies of the baseline export with the same reset as runs 1 and 2 and run 1's 41 approved core
relations, generated one after the other with the same code (DECISIONS 105, 106); then CQ tests and evaluation with
hold-out questions; no repair. Compared with `tools/compare_runs.py`. Two incidents:
- **3b** first stopped at the provider's token rate limit (429) right after 3a's tests; generated again a few minutes
  later. One module wrote a restriction as a class name (`SubClassOf(UsefulAI, "isPartOf some HumanCenteredAI")`),
  which broke the Turtle export; the generation's syntax-fix call tried twice (23.7k tokens) and could not repair it.
  The merge now leaves such axioms out (DECISIONS 105, "Fixed with 105"); in 3b the axiom was removed by hand in the
  project file before the CQ tests.
- **3c** ran with that merge fix (not yet committed then); it left out one axiom of the same kind
  (`SubClassOf(CompoundTask, "hasConstituentTask some Task")`), and no syntax fix was needed.
- In 3a the CQ tests ran twice (the input tokens include about 55k for the second run).

| | 3a | 3b | 3c | mean | sd |
|---|---|---|---|---|---|
| Planned classes | 224 | 198 | 231 | 217.7 | 17.4 |
| Central concepts excluded (plan + completion) | 42 | 68 | 24 | 44.7 | 22.1 |
| Vocabulary links after planning / after the modules | 2 / 6 | 1 / 6 | 0 / 7 | 1.0 / 6.3 | |
| Classes / object properties / axioms | 239 / 108 / 23 | 222 / 115 / 29 | 261 / 120 / 24 | 240.7 / 114.3 / 25.3 | |
| Root classes | 4 | 4 | 4 | 4.0 | 0.0 |
| Top-level relations | 85 | 91 | 99 | 91.7 | 7.0 |
| Links to reused vocabularies | 9 | 9 | 8 | 8.7 | 0.6 |
| Sibling groups with disjointness | 9 | 8 | 9 | 8.7 | 0.6 |
| Central concepts as a class (%) | 80.7 | 68.9 | 80.7 | 76.8 | 6.8 |
| Broader/narrower relations realized (%) | 48.0 | 55.3 | 64.5 | 55.9 | 8.3 |
| Classes linked to the inventory (%) | 92.5 | 90.1 | 85.4 | 89.3 | 3.6 |
| Competency questions full / partial / none | 8 / 2 / 0 | 4 / 6 / 0 | 2 / 8 / 0 | 4.7 full | 3.1 |
| Hold-out questions full / partial / none | 4 / 6 / 0 | 4 / 6 / 0 | 5 / 4 / 1 | 4.3 full | 0.6 |
| Input tokens of the run (k) | 325 (CQ twice) | 284 (syntax fix 24k) | 277 | 295 | 26 |

**Against the targets (PLAN.md phase 3), as mean over 3a-3c; in brackets the mean over all five runs where the code
changes since run 1 cannot matter (they act after the plan):**

| | Baseline | Target | Mean (sd) | |
|---|---|---|---|---|
| Input tokens | ~2.8 M | well below 1 M | ~280k per run | met |
| Top-level relations | 112 | about 70 | 91.7 (7.0) | not met |
| Root classes | 7 | about 10 or fewer | 4.0 | met |
| Links to reused vocabularies | 13 | at least as many | 8.7 (0.6) | not met (run 1: 6) |
| Central concepts as a class | 76.5 % | at least as good | 76.8 % (6.8) [75.4 %] | met on average, with a large spread |
| Broader/narrower relations realized | 64.7 % | at least as good | 55.9 % (8.3) [56.8 %] | not met |
| Competency questions full (current test) | 8 | at least as good | 4.7 (3.1); **8.3 (0.6) with the check** (below) | not met at first - see finding 3; met with the check |
| Hold-out questions full (current test) | 5 | at least as good | 4.3 (0.6) | close |

### Findings

1. **Generations of one configuration differ a lot.** The same plan prompt gives 198-231 planned classes and excludes
   24-68 central concepts; central concepts as classes vary between 68.9 % and 80.7 %, the realized hierarchy between
   48 % and 65 %. Single runs (runs 1 and 2) cannot show the effect of a change smaller than this spread.
2. **Stable:** root classes (4), links to vocabularies (8-9, the link calls decide alike), represented central
   concepts (98-100 %), consistency; token use ~280k per run.
3. **The CQ results vary mostly through the test, not the ontology**: full answers 8, 4 and 2. Most partial and failed
   results in 3b and 3c judge something the question does not ask: "whether the insight is sufficiently justified to
   be accepted as knowledge", "how much they help an audience understand", "not that the recorded interaction caused
   the insight", "the kinds are available from the asserted types rather than as separate answer values". The rule of
   DECISIONS 91 (a "leaves out" is missing information, not a judgement) does not hold the model.
4. **Two structural shortfalls remain**: the literature's hierarchy (56 % against 65 %) and the top-level relations
   (92 against 112 before and ~70 aimed at - more than run 1's 82; 30 of the 41 core relations relate "any" to "any",
   and modules add relations below few of them).
5. **Restrictions appear unasked**: two of three generations wrote "r some C" as a class - the modules want to say
   things the format cannot express yet (PLAN.md phase 5).

### Follow-ups (proposed)

- CQ test: make the "leaves out" rule hold - e.g. a second check per partial result ("is this information the
  question asks for, or a judgement about it?"), or the level decided by a separate short call with only question,
  answer rows and the stated gap; then test 3a-3c again to separate test noise from ontology differences.
- Exclusions of central concepts (24-68 per run): stricter rule as proposed after run 2.
- Hierarchy: look at which broader/narrower relations the plans realize in one run and not in another.

### 3a-3c tested again with the check of partial answers (DECISIONS 107)

The three ontologies unchanged; "Evaluate from scratch" (new sample data and queries for the competency and hold-out
questions), now with the separate check of partial answers. 3b twice: in the first evaluation its hold-out test failed
(the model's JSON answer was broken, `JSONDecodeError`), in the second the check of its hold-out answers hit the
provider's quota (429) - as designed they stayed partial and the report says so; so 3b's hold-out result is unchecked.

| | 3a | 3b | 3c | mean | sd |
|---|---|---|---|---|---|
| Competency questions full - first test (run 3) | 8 | 4 | 2 | 4.7 | 3.1 |
| **Competency questions full - with the check** | **8** | **8 / 9** (two tests) | **8** | **8.3** | 0.6 |
| ... of them made full by the check | 1 | 0 / 1 | 3 | | |
| ... full without the check (fresh test alone) | 7 | 8 / 8 | 5 | | |
| Hold-out questions full - first test | 4 | 4 | 5 | 4.3 | 0.6 |
| Hold-out questions full - with the check | 3 | (failed / 1 unchecked) | 5 (2 by the check) | | |
| Input tokens of the check calls | 2.0k | 0.8k / 0.8k | 2.5k | | |

**Findings.**
1. **The competency-question result is stable now: 8, 8-9 and 8 full** where the first test gave 8, 4 and 2 - on the
   same ontologies. All three reach the baseline's 8 (current test); the target "at least as good" is met.
2. **Two sources of test noise.** The fresh test alone already gives 7, 8 and 5 instead of 8, 4 and 2: queries and
   sample data written anew differ from test to test. The check removes the second source, gaps that judge instead
   of asking (made full: "the question asks how the concepts relate, not whether an insight was accepted or
   sufficiently justified", "... not whether they actually improved audience understanding"). The gaps it keeps name
   what the question asks ("the question asks about axes as well as legends, but the rows give only a legend").
3. **The hold-out questions remain hard to measure**: 3 and 5 full in 3a and 3c; in 3b one failure through broken
   JSON and one unchecked result through the quota. Several unchecked 3b gaps are judgements again ("whether users
   can actually perform each intended task"). Queries whose chain of joins finds no sample data still fail now and
   then ("No result on the sample data").
4. The baseline's hold-out figure (5) was measured without the check; a fair comparison needs it retested too.

### Follow-ups (proposed)

- Robustness of model calls: wait and retry when the provider's rate limit is reached; one retry when the answer is
  no valid JSON - both cost a run's test or a whole generation today.
- A query without a result on its own sample data: one correction round (query and sample data back to the model).
- Exclusions of central concepts, hierarchy and top-level relations: as above.

All four built: DECISIONS 108 (rate limits, broken JSON), 109 (correction of empty queries), 110 (exclusions of
taxonomy categories and concepts of the questions reviewed), 111 (hierarchy after the modules), 112 (core relations
after the modules); also 113 (an unreachable OOPS! service fails fast).

## The hierarchy measure with declined relations (DECISIONS 111), recomputed for the runs so far

Since DECISIONS 111 the evaluation also counts broader/narrower relations that were declined with a reason (by the
plan, by "Build hierarchy" or after the modules). Recomputed from the project files of the earlier runs (no model
call; the realized counts match their stored evaluations):

| | Relations | Realized | Declined with a reason | Neither | Realized | Realized or declined |
|---|---|---|---|---|---|---|
| Baseline (after repairs) | 153 | 99 | 44 | 9 | 64.7 % | **93.5 %** |
| Run 1 | 139 | 90 | 5 | 44 | 64.7 % | 68.3 % |
| Run 2 | 119 | 61 | 8 | 49 | 51.3 % | 58.0 % |
| 3a | 148 | 71 | 10 | 67 | 48.0 % | 54.7 % |
| 3b | 123 | 68 | 10 | 45 | 55.3 % | 63.4 % |
| 3c | 155 | 100 | 8 | 46 | 64.5 % | 69.7 % |

The baseline's "Build hierarchy" repair decided almost every relation: it realized 99 and declined 44, leaving 9
open. The runs without repair leave 44-67 relations neither realized nor decided. This - not the realized share,
which the baseline reaches in runs 1 and 3c - is the gap the hierarchy step after the modules (DECISIONS 111) is
meant to close; runs 4a-4c measure it.

Before runs 4a-4c the changes since 3a-3c (DECISIONS 108-113) were reviewed; four defects were fixed (notes under
DECISIONS 108-111): two broader terms of one class in one call overwrote each other, an upper-layer class could be
put below a domain class, one correction with invalid Turtle discarded the sample data of all others, and errors
that only mention a "limit" (or a quota for the day) were waited for in vain.

## Runs 4a-4c - 2026-10-29, gpt-6-sol, commit 166e028 (steps 1-4 and the code-review fixes)

**Setup.** As 3a-3c: three new copies of the baseline export with the same reset and run 1's 41 approved core
relations, generated one after the other, then CQ tests and evaluation with hold-out questions; no repair. The code
differs from 3a-3c by DECISIONS 107-113 (check of partial answers, robust model calls, correction of empty queries,
review of excluded taxonomy categories, hierarchy and core relations after the modules, OOPS! fail-fast) and the
review fixes (DECISIONS 117). No errors: no failed step, no invalid axiom, no placeholder class; the JSON repair and the
correction of an empty query were each used once (4c), and the corrected question then passed.

| | 3a-3c (mean, sd) | **4a** | **4b** | **4c** | **4a-4c (mean, sd)** |
|---|---|---|---|---|---|
| Planned classes | 217.7 (17.4) | 252 | 238 | 251 | 247.0 (7.8) |
| Central concepts excluded | 44.7 (22.1) | 11 | 9 | 16 | **12.0 (3.6)** |
| ... exclusions reviewed / kept (DECISIONS 110) | - | 7 / 1 | 7 / 0 | 15 / 0 | |
| Classes / object properties / axioms | 240.7 / 114.3 / 25.3 | 278 / 139 / 26 | 268 / 132 / 23 | 283 / 145 / 40 | 276.3 / 138.7 / 29.7 |
| Root classes | 4.0 | 4 | 4 | 4 | 4.0 |
| Top-level relations | 91.7 (7.0) | 75 | 91 | 100 | 88.7 (12.7) |
| ... relations placed below a core relation after the modules / kept | - | 28 / 36 | 16 / 51 | 15 / 61 | |
| Links to reused vocabularies | 8.7 (0.6) | 8 | 5 | 14 | 9.0 (4.6) |
| Sibling groups with disjointness | 8.7 | 13 | 6 | 10 | 9.7 |
| Central concepts as a class (%) | 76.8 (6.8) | 85.2 | 80.7 | 81.8 | **82.6 (2.3)** |
| Broader/narrower relations realized (%) | 55.9 (8.3) | 56.0 | 54.7 | 60.1 | 56.9 (2.8) |
| ... realized or declined with a reason (%) | 54.7-69.7 | 98.8 | 98.0 | 98.7 | **98.5** |
| ... after the modules: offered / added / declined / refused | - | 66 / 0 / 66 / 0 | 61 / 1 / 58 / 2 | 52 / 1 / 49 / 2 | |
| Competency questions full (with the check) | 8.3 (0.6) | 9 | 9 | 10 | **9.3 (0.6)** |
| Hold-out questions full | 4.0 (two runs) | 6 | 4 | 3 | 4.3 (1.5) |
| Input tokens of the run (k) | ~280-295 | 314 | 308 | 318 | 313 (5) |

The new steps cost about 20k input tokens per run: core relations after the modules 11-13k, hierarchy after the
modules 4-5k, the checks and corrections of the tests 1-3k.

**Against the targets (PLAN.md phase 3; baseline after all repairs):**

| | Baseline | Target | 4a-4c | |
|---|---|---|---|---|
| Input tokens | ~2.8 M | well below 1 M | ~313k per run | met |
| Root classes | 7 | about 10 or fewer | 4 | met |
| Central concepts as a class | 76.5 % | at least as good | 82.6 % (sd 2.3) | **met, now clearly** |
| Competency questions full (current test) | 8 | at least as good | 9.3 | **met** |
| Broader/narrower relations | 64.7 % realized, 93.5 % realized or declined | at least as good | 56.9 % realized, 98.5 % realized or declined | decided: met; realized: not met |
| Hold-out questions full | 5 (without the check) | at least as good | 4.3 | close |
| Links to reused vocabularies | 13 | at least as many | 9.0 (4c: 14) | not met |
| Top-level relations | 112 | about 70 | 88.7 (4a: 75) | not met |

### Findings

1. **The measurement is stable now.** The spread fell for every figure the steps aimed at: planned classes sd 17.4 ->
   7.8, excluded central concepts 22.1 -> 3.6, central concepts as classes 6.8 -> 2.3 points, realized hierarchy
   8.3 -> 2.8 points, competency questions 0.6. Differences between configurations of a few points can now be seen.
2. **Reviewing the exclusions works (DECISIONS 110):** 12 instead of 45 central concepts excluded, and central
   concepts as classes 82.6 % against 76.8 % - higher than the baseline after "Add missing central concepts". The plan
   itself excluded far fewer (the rule), and the review placed what remained in all but one case.
3. **The hierarchy step decides, but adds almost nothing (DECISIONS 111):** of 52-66 relations it added 0-1 and
   declined the rest, with sound reasons - the sources' "broader" terms are mostly single-source and loose ("Goal is a
   kind of Axis", "Interaction is a kind of Visualization"). So the literature's hierarchy is now decided almost
   completely (98.5 % against 93.5 % for the baseline after "Build hierarchy"), while the realized share stays at
   57 %. The baseline's higher realized share probably includes such loose relations adopted by the repair; the
   "realized" target compares against that and should give way to "realized or declined".
4. **Core relations after the modules (DECISIONS 112) help little:** they placed 15-28 relations, but the modules
   produce more relations than before (139 against 114 object properties), so top-level relations stay at 89 on
   average, with a wide spread (75-100). The model keeps 36-61 relations as "their own kind of connection".
5. **Links stay below the baseline** (9 against 13), varying with the plan (4c linked five role classes to prov:Role).
6. **The disjointness check of the hierarchy step works:** it refused two superclasses that would have put an
   interaction under both Process and InformationObject (4b and 4c).

### Follow-ups (proposed)

- **Done (DECISIONS 118):** the baseline's realized relations compared with 4a-4c - of its 99, 56-63 do not exist in
  a run at all (a class is missing or named differently); of those that do, the runs realize 30-36, decline 5-8 and
  leave 0-2 open; each run realizes 49-64 that the baseline does not have. Seven of the ten declined ones follow one
  modelling choice: the plan separates an executed interaction (brushing, panning, semantic zooming as something a user
  does) from the interaction technique that specifies it, and does not put the one below the other - a point for the
  expert review. The target is now "realized or declined".
- (was:) Replace the hierarchy target "realized at least as good" by "realized or declined at least as good" (PLAN.md), and
  look at the baseline's realized relations that the runs decline - if they are loose, the baseline's 64.7 % is not a
  goal.
- **Done (DECISIONS 119):** the relations kept without a core relation are mostly kept for good reasons; across 4a-4c
  they point to information objects (92), qualities (25), agents (13) and processes (10), and no core relation has
  Quality as range. 20 of the 41 core relations were below no relation in any run. The step-7 proposal now asks for
  general relations to upper-layer classes ("has quality") and keeps narrow ones in the modules; step 7 shows after
  a generation which core relations are unused and where the rest point.
- (was:) Top-level relations: find out why the model keeps relations like `hasTaskInput` as their own kind - the candidates
  are many (about 30 per relation) and most core relations relate "any" to "any"; fewer, more specific core relations
  or a closer look at the reasons kept.
- The remaining review findings (DECISIONS 117), first the Turtle editor (T1) and the plural handling of the concept key
  (T11, then all runs evaluated again).
  **Done:** the Turtle editor (DECISIONS 120) and the concept key (DECISIONS 121) - recomputed for the baseline and
  runs 1-4c, the new key changes none of the coverage and hierarchy figures, so no run had to be evaluated again.


## Runs 5a-5c - 2026-10-30/31, gpt-6-sol, commits d1d1719 / 2e25b08 (phase 5 and 6: class restrictions, Evaluate 3x)

**Setup.** As 4a-4c: three new copies of the baseline export with the same reset, generated one after the other,
then **Evaluate 3x** (three independent tests of the competency and hold-out questions, DECISIONS 124); no repair.
Unlike 4a-4c, the copies did not use run 1's 41 core relations but a vocabulary of 39 proposed with the new step-7
prompt (DECISIONS 119: general relations to the upper layer, "has quality") - 17 relations new, 19 gone, most domains
and ranges now upper-layer classes. (Corrected on 2026-10-31; the first version of this record said "the 41 approved
core relations".) New since 4a-4c: the core-relation proposal for the upper layer (DECISIONS 119), the
review fixes (120-122) and class restrictions written by the modules and checked by the reasoner (125). 5a was
generated on d1d1719 (12:32 CET), 5b on 2e25b08 (15:08 CET), 5c on 2026-10-31 (21:27 CET, same generation code). No
failed step. The daily limit of 100 sol calls set the pace: one run with Evaluate 3x takes 32-34 calls.

| | 4a-4c (mean, sd) | **5a** | **5b** | **5c** | **5a-5c (mean, sd)** |
|---|---|---|---|---|---|
| Planned classes | 247.0 (7.8) | 227 | 242 | 238 | 235.7 (7.8) |
| Central concepts excluded | 12.0 (3.6) | 26 | 21 | 17 | **21.3 (4.5)** |
| ... exclusions reviewed / kept | | 25 / 0 | 19 / 0 | 14 / 0 | |
| Classes / object properties / axioms | 276.3 / 138.7 / 29.7 | 264 / 115 / 28 | 272 / 126 / 29 | 269 / 130 / 27 | 268.3 / 123.7 / 28.0 |
| Root classes | 4.0 | 5 | 4 | 8 | 5.7 (2.1) |
| Top-level relations | 88.7 (12.7) | 67 | 75 | 89 | **77.0 (11.1)** |
| Links to reused vocabularies | 9.0 (4.6) | 9 | 10 | 15 | 11.3 (3.2) |
| Sibling groups with disjointness | 9.7 | 11 | 13 | 10 | 11.3 |
| Class restrictions (on classes) | - | 84 (72) | 84 (70) | 60 (55) | 76.0 |
| ... refused by the checks / removed by the reasoner | - | 1 / not checked | 1 / 0 | 2 / 0 | |
| Reasoner consistent | - | no (see below) | yes | yes | |
| Central concepts as a class (%) | 82.6 (2.3) | 75.0 | 80.3 | 79.5 | **78.3 (2.9)** |
| Central concepts represented (%) | | 98.5 | 98.9 | 98.1 | 98.5 (0.4) |
| Broader/narrower relations realized (%) | 56.9 (2.8) | 53.9 | 52.7 | 59.4 | 55.3 (3.6) |
| ... realized or declined with a reason (%) | 98.5 | 100.0 | 99.4 | 99.4 | **99.6** |
| Competency questions full, first test | 9.3 (0.6) | 9 | 8 | 9 | 8.7 (0.6) |
| Competency questions full, Evaluate 3x | - | 9, 6, 6 | 8, 8, 9 | 9, 8, 10 | **8.1** (runs 7.0, 8.3, 9.0) |
| ... spread within a run (sd) | - | 1.7 | 0.6 | 1.0 | 1.1 |
| Hold-out questions full, first test | 4.3 (1.5) | 5 | 4 | 4 | 4.3 (0.6) |
| Hold-out questions full, Evaluate 3x | - | 5, 4, 4 | 4, 4, 3 | 4, 5, 4 | **4.1** (sd within a run 0.6) |
| Model calls: generation / Evaluate 3x | | 18 / 15 | 18 / 16 | 17 / 15 | 17.7 / 15.3 |
| Input tokens: generation / Evaluate 3x (k) | ~313 incl. one test | 176 / 430 | 180 / 448 | 179 / 436 | 178 / 438 |

**5a and the reasoner.** HermiT refused 5a: the module wrote `hasPart min 2`, and `hasPart` is transitive - OWL 2 DL
allows no numbers on such a property. The reasoner check after the merge was therefore skipped ("not checked"). Fixed
in 2e25b08 (`restriction_issues`: no numbers on non-simple properties); without the three affected restrictions 5a is
consistent (checked offline). In 5c the new check refused exactly such a restriction (`CompoundTask SubClassOf hasPart
min 2 Task`); 5b and 5c are consistent, also with sample data, and the reasoner removed nothing.

### Findings

1. **One test is not enough, three are:** within one ontology the competency questions varied by up to three of ten
   between identical tests (5a: 9, 6, 6). Over the three generations the mean of the repeated tests is 8.1, the first
   test alone said 8.7. A difference between two configurations of one or two questions is within this noise; the
   hold-out questions vary less (sd 0.6).
2. **Class restrictions work from the first generation on:** 60-84 per run on 55-72 classes, almost all
   existential ("some"), each checked against domain and range; the checks refused one or two per run for good reasons
   (a class not below the property's domain, a number on a transitive property), and the reasoner had nothing to
   remove.
3. **Fewer top-level relations (DECISIONS 119):** 77 against 89, with 5a at 67 - near the target of about 70 for the
   first time - but the spread stays wide (67-89).
4. **More central concepts excluded:** 21 against 12. The plan assigned fewer (229-237 against 245-248), the completion
   placed more, and the review kept none of the exclusions. The excluded concepts are mostly about research itself -
   in all three runs `methodology`, `taxonomy`, `pitfall`, `problem-driven research`, `technique-driven research`,
   `reflection`, `VIS4ML` - but also `interaction primitive`, `information location` and `task by data type taxonomy`,
   which could be classes. Central concepts as classes fell to 78.3 % (82.6 %), represented or decided stays at 98.5 %.
5. **The hierarchy is decided almost completely** (99.6 % realized or declined), the realized share unchanged (55 %).
6. **Cost:** a generation now takes about 180k input tokens in 17-18 calls; Evaluate 3x costs about 2.5 times as much
   (430-450k, 15-16 calls).

### Class restrictions on a copy of the baseline (2026-10-30, eefcf277)

The repair tool "Add class restrictions" (DECISIONS 125) on a copy of the baseline after all repairs, to measure how
many of the class pairs the property consolidation gave up come back (`tools/lost_pairs.py`). Evaluate (single test),
add class restrictions (11 calls, 30 candidates each), evaluate again: 23 calls.

| | |
|---|---|
| Candidates (class pairs) | 301 |
| Restrictions written / declined with a reason | 55 (54 "some", 1 "min 2") on 46 classes / 245; 2 still offered |
| Lost class pairs of the consolidation (264) with a restriction again | 43 (16.3 %); 215 declined |
| Reasoner | consistent, also with sample data |
| Competency / hold-out questions full (after) | 10 / 7 (one test) |

The declined pairs mostly fail the "every A" test ("An attribute can exist without a recorded observation"), so the
tool restores a lost connection only where it holds for every member of the class. The question results before the
repair were overwritten by the second evaluation (follow-up below).

### Follow-ups (proposed)

- **Keep the previous evaluation** next to the latest, so a repair can be compared before and after (DECISIONS,
  open points).
- **Done (analysis below):** why the plan excludes more central concepts than in 4a-4c.
- **Done (DECISIONS 132):** root classes 8 in 5c - four of them were `User` and three roles below `prov:Person`,
  which the ontology puts below `Agent`; the count did not follow that link. Recomputed: 5c 4, run 1 4 (was 5), the
  rest unchanged; 5a keeps 5 (`CollaboratorRole` only below `dcat:Role`).

## Top-level relations per class (DECISIONS 130), recomputed for all runs

The absolute target "about 70" became "about 0.3 top-level relations per class or fewer". Recomputed from the stored
ontologies (no model calls):

| | Classes | Top-level relations | Per class | Target 0.3 |
|---|---|---|---|---|
| Raw generations before any consolidation | 229-326 | 268-272 | 0.83-1.17 | not met |
| Baseline after all repairs | 345 | 112 | 0.32 | close |
| Run 1 / 2 | 234 / 212 | 82 / 87 | 0.35 / 0.41 | not met |
| Runs 3a / 3b / 3c | 239 / 222 / 261 | 85 / 91 / 99 | 0.36 / 0.41 / 0.38 | not met |
| Runs 4a / 4b / 4c | 278 / 268 / 283 | 75 / 91 / 100 | 0.27 / 0.34 / 0.35 | 4a met |
| Runs 5a / 5b / 5c | 264 / 272 / 269 | 67 / 75 / 89 | 0.25 / 0.28 / 0.33 | 5a, 5b met |
| Wine runs 13 / 14 | 13 / 18 | 6 / 6 | 0.46 / 0.33 | below the minimum of 10 relations: not assessed |

The verdicts for VA hardly change (with "about 70", 5a met and 4a, 5b were close); the wine ontology is no longer
measured against a number meant for an ontology fifteen times its size.

## Why 5a-5c excluded more central concepts than 4a-4c (analysis, 2026-10-31, no model calls)

**The planning call got the same input in all six runs.** Inventory (1,395 concepts), use case, competency
questions, key notions, project context, upper layer and data are identical (compared by hash), the model was
gpt-6-sol via RWTHgpt in all runs, and the planning prompt did not change between 166e028 and 2e25b08. The core
vocabulary differs (see the setup of 5a-5c), but the planning prompt does not contain it. The new concept key
(DECISIONS 121) changes which concepts the review protects by one (611 -> 612, `aesthetics`).

**What differs is the model's answer.** Counted per run:

| | 4a | 4b | 4c | 5a | 5b | 5c |
|---|---|---|---|---|---|---|
| Central concepts the plan excluded | 16 | 16 | 31 | 51 | 40 | 31 |
| ... of them reviewed (taxonomy category or named in a question) | 7 | 7 | 15 | 25 | 19 | 14 |
| ... still excluded after the review | 1 | 0 | 0 | 0 | 0 | 0 |
| Not reviewed, so excluded as the plan said | 9 | 9 | 16 | 26 | 21 | 17 |
| Placed by the completion | 15 | 19 | 17 | 35 | 27 | 32 |

4c and 5c are equal (31); the means differ (21 against 41), but with three runs each the difference is not
significant (Welch's t about 2.6, 4 degrees of freedom, p about 0.06). **The likeliest explanation is the spread of
the planning call itself, not a change in the code**: for the same input it excluded between 16 and 51 central
concepts.

**Why the spread reaches the result:** the review (DECISIONS 110) only re-examines exclusions of protected concepts
(taxonomy categories, concepts named in a question) - and it placed all of them in 5a-5c. Every other exclusion
stands as the plan wrote it, after one call and without a second look. Two further observations:

- Most exclusions are about research itself, and leaving them out is defensible (`methodology`, `taxonomy`,
  `pitfall`, `problem-driven research`). 5a-5c added design-study frameworks and their terms (`nine stage framework`,
  `nested model`, `consideration space`, `proposal space`, `information location`, `stability of the task`) - "specific
  to one paper's method" is an allowed reason, but these have two or more sources each.
- Two of 5a's exclusions are bookkeeping errors: `objective uncertainty` and `uncertainty quantification` are
  "accounted for as ObjectiveUncertainty / UncertaintyQuantification in the Uncertainty module" - the plan put a
  modelled concept on the excluded list.

**Fixes (built, DECISIONS 131):**
1. Every exclusion of the plan goes through the completion step, not only the protected ones, so that each is
   decided twice and one noisy call no longer decides the count. The completion already batches 60 concepts per
   call; with 16-51 exclusions this adds no call in most runs.
2. An exclusion whose reason names a planned class ("accounted for as X") counts as an assignment to that class.

The next VA runs measure the effect (expected: a smaller spread of excluded central concepts). Note for comparisons:
`by_plan` no longer includes the plan's exclusions.

## Hold-out questions chosen by central concepts (DECISIONS 133) - a new series from here

The hold-out set of 5a-5c (and of all earlier runs) followed the order of the inventory: 415 of 416 literature
questions have one source, so "most sources first" decided nothing. It contained questions about single-paper details
(the Vega-Lite unit specification, multi-view composition operators) that failed in nearly every run. From DECISIONS
133 on, the set is chosen by the central concepts the questions name, spread over the themes, and stored with the
project. The 5c copy does not record which literature questions the suggestions of step 5 saw, so the first 40 of
the inventory stay excluded "to be safe", as before. (Corrected on 2026-10-31: the lists first written here were
computed without that exclusion and were not the sets tested; below are the sets as stored and tested.)

**Bridge (2026-10-31, 22:42 CET, commit 27d7468):** 5c evaluated once more with Evaluate 3x. In the review the
team removed two questions - one about specifying brushing, cross-filtering and the like, and one about which task
clarity and information location make a domain problem suitable for a design study - and the next candidates took
their place. The set tested, sharing no question with the old one:

1. Which actions can an analyst perform on data, models, visualizations and their mappings?
2. What provenance must be recorded to follow uncertainty through system operations and human insights?
3. Which data variable is mapped to each aesthetic, and which scale controls that mapping?
4. Which operations help an analyst focus on subsets, expose patterns, or derive new values?
5. Is a given uncertainty statistical, an error, or a range?
6. Which selected history views can be exported for a report or presentation?
7. Which elementary graphical-perception tasks does a graph require for decoding its quantitative values?
8. Which observations did users report as insights while analyzing a data set with a visualization tool?
9. Is a reported case study based on a domain expert, close collaboration, visualization researchers, or a
   hypothetical usage scenario?
10. How can user interactions be represented as sequences, grammars, models, or graphs?

14 model calls.

| 5c | Old hold-out set | New hold-out set |
|---|---|---|
| Hold-out questions full (3 runs) | 4, 5, 4 (mean 4.3) | 2, 2, 2 (mean 2.0) |
| ... partly (first test) | 4 | 8 |
| ... not answered (first test) | 2 | 0 |
| Answered at least partly (first test) | 8 of 10 | **10 of 10** |
| Questions that vary between runs | | 2 of 10 |
| Competency questions full (3 runs) | 9, 8, 10 | 9, 9, 10 |
| Reasoner | consistent | consistent |

**Reading the bridge.** No question of the new set goes unanswered: the ontology has the concepts of every question,
which is what selecting by central concepts aimed at, and the results are stable (sd 0). But only two are answered in
full. The check of partial answers (DECISIONS 107) gives its reasons, and they are about the wording, not missing
classes: six of the ten questions ask what *can* or *must* be the case or for *every* member of a set - "which
actions *can* an analyst perform" ("the query identifies recorded actions, not every action an analyst could
potentially perform"), "what provenance *must* be recorded" ("cannot establish that these records are required"),
"which views *can* be exported", "which tasks does a graph *require*", "which operations *help*", "how *can*
interactions be represented". An ontology with sample data shows what is recorded; a question about possibility,
necessity or completeness can only be answered in part. The old set failed for the opposite reason - concepts the
ontology did not have.

So "full" on the new set measures the wording of the questions as much as the ontology. Until that is settled, the
hold-out results are reported with both figures: in full, and at least partly.

**Decided (DECISIONS 134):** questions with modal, normative or exhaustive wording come after the plain ones. The
bridge is repeated on 5c with the new set (the two removed questions stay removed). It keeps four questions of the
first bridge set (3, 5, 8, 9) and adds six:

- How are findings, insights, hypotheses, and knowledge related during trust building?
- Which goals, outputs, questions, and methods are associated with each evaluation scenario?
- How are captured interactions and provenance encoded?
- Which guides are generated for position and non-position scales?
- Does a data assessment examine input quality, output performance, or fairness?
- Which characteristics of data and representation affect visualization complexity?

**Second bridge, first attempt (2026-10-31, 22:56 CET, commit dcf1be1): no hold-out result.** A query of the
hold-out test used `EXISTS { ... }` inside a SELECT expression; rdflib parses it but fails when the rows are read
("What do I do with this CompValue?"). That happened outside the error handling of the single test, so the whole
hold-out test was given up - all three runs (DECISIONS 135). The competency questions were tested (8, 8, 9 of 10).
7 model calls. To be repeated with the fix.

**Second bridge (2026-10-31, 23:07 CET, commit c0c7ffc):** Evaluate 3x on 5c with the same set, 12 model calls.

| 5c | Old set | First bridge (DECISIONS 133) | **Second bridge (DECISIONS 134)** |
|---|---|---|---|
| Hold-out questions full (3 runs) | 4, 5, 4 (mean 4.3) | 2, 2, 2 (2.0) | **4, 4, 3 (3.7)** |
| ... partly | 4 (first test) | 8, 8, 8 | 6, 5, 7 |
| ... not answered | 2 (first test) | 0, 0, 0 | 0, 1, 0 |
| Answered at least partly | 8 (first test) | 10, 10, 10 | **10, 9, 10** |
| Competency questions full (3 runs) | 9, 8, 10 | 9, 9, 10 | 9, 9, 8 |
| Reasoner | consistent | consistent | consistent |

Three questions are answered in full in every run (how findings, insights, hypotheses and knowledge relate; which
data variable is mapped to each aesthetic and which scale controls it; how captured interactions and provenance are
encoded), a fourth in two of three (the guides of position and non-position scales). The rest are partly answered,
now for reasons that concern the ontology or a causal claim rather than the wording of possibility: the evaluation
scenarios have no research questions ("the questions associated with each scenario"), whether a case study was
reported or the collaboration close is not recorded, and "which characteristics *affect* visualization complexity"
asks for an effect the data do not show. Twice in run 3 a query put `EXISTS` inside a SELECT expression again; with
DECISIONS 135 these questions counted as partly answered instead of ending the test.

**The new hold-out series starts here:** for 5c, 3.7 of 10 in full and 9.7 of 10 at least partly. Round 6 is
compared with these figures; earlier hold-out figures (4.1 for 5a-5c) belong to the old set.

## Runs 6a-6c - 2026-10-31/11-02, gpt-6-sol, commit 75b68b4 (DECISIONS 131-135)

**Setup.** Three copies of 5c as it was before its generation (`drafts/round6`, built from the tool's own export):
same inventory, use case, questions, context, vocabularies and the 39-relation core vocabulary as 5a-5c; all decisions
of the generation removed; the hold-out set of the second 5c bridge (with the team's two removals) stored with each
copy. Generate, then Evaluate 3x; no repair. 6a was generated on 2026-10-31 (23:27 CET), 6b and 6c on 2026-11-02
(13:09, 13:26 CET), all on the same code. New since 5a-5c: every exclusion of the plan gets a second look (131), root
classes through vocabularies (132), hold-out questions by central concepts and without modal wording (133, 134), a
failing query fails only its question (135). No failed step; 32-36 calls per run (17-18 for the generation).

| | 5a-5c (mean, sd) | **6a** | **6b** | **6c** | **6a-6c (mean, sd)** |
|---|---|---|---|---|---|
| Central concepts the plan excluded | 40.7 (10.0) | 40 | 65 | 32 | 45.7 (17.2) |
| ... given a second look | 19.3 (protected only) | 40 | 65 | 31 | |
| ... "accounted for as" a planned class | - | 0 | 0 | 1 | |
| **Central concepts excluded in the end** | 21.3 (4.5) | 5 | 8 | 3 | **5.3 (2.5)** |
| Central concepts placed by the completion | 31.3 (4.0) | 31 | 68 | 38 | 45.7 (19.7) |
| Central concepts as a class | 206.7 (7.6) / 78.3 % | 193 | 207 | 207 | 202.3 (8.1) / 76.6 % |
| ... as a property or an individual | 33.3 | 64 | 43 | 46 | 51.0 |
| ... planned but not built by a module | 4.0 | 3 | 7 | 8 | 6.0 |
| Central concepts represented or decided (%) | 98.5 | 98.9 | 97.3 | 97.0 | 97.7 |
| Classes / object properties / axioms | 268.3 / 123.7 / 28.0 | 243 / 114 / 18 | 262 / 128 / 32 | 262 / 118 / 33 | 255.7 / 120.0 / 27.7 |
| Root classes (DECISIONS 132) | 4.3 | 4 | 4 | 4 | 4.0 |
| Top-level relations per class | 0.29 | 0.33 | 0.30 | 0.29 | 0.31 |
| Links to reused vocabularies | 11.3 | 6 | 8 | 10 | 8.0 |
| Broader/narrower relations realized (%) | 55.3 | 42.7 | 59.9 | 59.4 | 54.0 |
| Competency questions full, Evaluate 3x | 7.0 / 8.3 / 9.0 (8.1) | 6.7 | 8.7 | 6.7 | **7.4** |
| Hold-out (new set) full, Evaluate 3x | 5c bridge: 3.7 | 2.3 | 3.7 | 2.7 | **2.9** |
| Hold-out (new set) answered at least partly, per run | 5c bridge: 10, 9, 10 | 9, 10, 10 | 10, 10, 10 | 10, 10, 9 | 9.8 |
| Reasoner | consistent (5b, 5c) | consistent | consistent | consistent | |

### Findings

1. **The second look works (DECISIONS 131):** the plan still excluded between 32 and 65 central concepts for the
   same input, but only 3-8 stayed excluded (5a-5c: 17-26). What stays out is research vocabulary in all three runs
   (`methodology`, `taxonomy`, `design study paper`, `science of interaction`, `technique-driven research`).
2. **The placed concepts became properties and individuals more than classes.** Concepts as a class did not rise
   (202 against 207, within the spread); concepts as a property or individual did (51 against 33): `Algorithm
   Performance` and `Evaluating Collaborative Data Analysis` as individuals of an evaluation scenario, `VIS4ML` as an
   individual, `pitfall` as a property `hasPitfall`, `expressiveness` as `hasTaxonomyExpressiveness`; others, such as
   `interaction primitive` and `reflection`, as classes. Whether research-side concepts belong in the ontology at all
   is the use case's question - one for the expert review. Slightly more planned concepts were not built by their
   module (3-8 against 3-5: `Mapping`, `stability of the task`, `chunking`, `feedback loop`).
3. **The competency questions are within the spread, and the same three are weak as in round 5:** the difference
   between filtering, selection, navigation and semantic zooming (0-1 of 3 in all six runs); tracing an insight back
   through interactions and states; how a person takes part in building an AI model. The reasons are the same in both
   rounds - the ontology records that something happened, not the before-and-after content or the causal and
   temporal order. 7.4 against 8.1 is within the run-to-run spread (5a alone: 7.0); 6a is the weaker run overall
   (243 classes, 42.7 % of the hierarchy realized, 18 axioms).
4. **Hold-out, new set:** 2.3-3.7 in full (5c bridge 3.7), and every question at least partly answered in nearly every
   run - the set is no longer dominated by single-paper details, and the failures are partial answers, not missing
   concepts.
5. **Structure is stable:** 4 root classes in every run, 0.29-0.33 top-level relations per class, reasoner consistent.

### Follow-ups (proposed)

- **Interaction effects and provenance order:** the three weak competency questions ask for what changes in a view and
  in which order things happened. A look at how the Interaction and Provenance modules model state changes and
  temporal order (the core relation `precedes` exists) could lift them in every run.
- **Placements of the second look:** check in the expert review whether research-side concepts (`VIS4ML`, `pitfall`,
  evaluation scenarios) belong to the use case or should stay excluded.
- **Planned but not built:** 3-8 central concepts the plan placed were not created by their module; the step 8 report
  lists them - a repair tool ("Add missing central concepts") exists, but the generation could check this itself.

## Runs 7a-7c - 2026-11-03/05, gpt-6-sol, commits bf77b45 (7a) and 5b4646e (7b, 7c) (DECISIONS 140-146)

**Setup.** As 6a-6c: copies of 5c as it was before its generation (`drafts/round7/VA-run-7a/7b/7c.project.json`, the
6a file with new titles), the same inventory, use case, questions, context, vocabularies, the 39-relation core
vocabulary and the same 10 hold-out questions. Generate, then Evaluate 3x; no repair. 7a on 2026-11-03 (23:12 CET),
7b and 7c on 2026-11-05 (10:13, 10:27). New since 6a-6c: the plan tells the domain from a paper's method (140, as
corrected after the wine run 7-luna), events record what they change and in which order (141), an axiom that puts a
class below two disjoint classes is left out (142); for 7b and 7c also 143-146, which do not touch a sol generation
(no axiom was left out). Calls: 31, 32, 36 per run (17-21 for the generation, 13-15 for Evaluate 3x).

| | 6a-6c (mean) | 7a | 7b | 7c | **7a-7c (mean)** |
|---|---|---|---|---|---|
| Central concepts the plan excluded (all given a second look) | 45.7 | 20 | 36 | 41 | 32.3 |
| **Central concepts excluded in the end** | 5.3 | 6 | 2 | 6 | **4.7** |
| Central concepts placed by the completion | 45.7 | 32 | 46 | 47 | 41.7 |
| Central concepts as a class | 202.3 | 167 | 210 | 205 | 194.0 |
| ... as a property or an individual | 51.0 | 92 | 52 | 53 | 65.7 |
| Classes / object properties | 255.7 / 120.0 | 232 / 148 | 266 / 163 | 269 / 158 | 255.7 / 156.3 |
| Axioms / class restrictions | 27.7 / 65.0 | 37 / 82 | 37 / 107 | 31 / 93 | 35.0 / 94.0 |
| Root classes | 4.0 | 4 | 5 | 4 | 4.3 |
| Top-level relations per class (target 0.3 or fewer) | 0.31 | 0.38 | 0.34 | 0.33 | 0.35 |
| Broader/narrower relations realized (%) | 54.0 | 36.1 | 50.3 | 53.7 | 46.7 |
| Classes with sources (%) | 90.4 | 87.5 | 86.8 | 91.8 | 88.7 |
| **Competency questions full, Evaluate 3x** | 7.4 | 9.0 (9, 9, 9) | 9.7 (10, 10, 9) | 8.3 (8, 9, 8) | **9.0** |
| **Hold-out full, Evaluate 3x** | 2.9 | 3.3 (3, 5, 2) | 4.0 (5, 3, 4) | 4.3 (3, 4, 6) | **3.9** |
| Hold-out answered at least partly, per run | 9.8 | 10, 10, 10 | 10, 10, 10 | 10, 10, 10 | 10 |
| Reasoner (alone / with sample data) | consistent | consistent | consistent | consistent | |

The three weak questions of rounds 5 and 6 (tests in full, of 3):

| Question | 5a-5c | 6a-6c | 7a | 7b | 7c |
|---|---|---|---|---|---|
| How do filtering, selection, navigation and semantic zooming differ, and how can they affect what appears in coordinated views? | 0-1 each | 0, 0, 0 | 0 | **3** | **3** |
| How can I trace an insight back through interactions, visualization states, reasoning and data lineage? | partial | 1, 3, 1 | 3 | 3 | 3 |
| How can a person participate in building or examining an AI model ...? | partial | 0, 3, 2 | 3 | 3 | 0 |

### Findings

1. **The events rule works** (DECISIONS 141): the filtering/zooming question is answered in full for the first time
   (all three tests of 7b and 7c; never in the nine runs of rounds 5 and 6), tracing an insight back in all nine tests
   of round 7, a person's part in building an AI model in 7a and 7b. The ontologies record the state before and after
   an interaction (`hasPriorApplicationState`, `hasResultingApplicationState`) and the model before and after a
   development step (`hasModelBefore`, `hasModelAfter`). Where a test stays partial, it asks for a definition (how the
   operations differ) that a query over sample data does not return.
2. **The best VA round so far:** 9.0 of 10 competency questions in full (round 5: 8.1, round 6: 7.4) and 3.9 of 10
   hold-out questions (2.9), every hold-out question at least partly answered in every run - although the generation
   never saw them.
3. **7a's dip was variance:** 7b and 7c made 210 and 205 central concepts classes, as in round 6 (7a: 167). What stays
   excluded is research vocabulary (`methodology`, `design study paper`, `science of interaction`, `taxonomy`; `VIS4ML`
   in 7a and 7b).
4. **More relations and restrictions:** about 30 % more object properties (156 against 120) and 0.35 top-level
   relations per class, slightly above the target (round 6: 0.29-0.33); 94 class restrictions against 65. The
   before/after relations of the events rule are new module properties; the core vocabulary has `hasState`,
   `precedes` and `changes`.
5. **Stable structure:** 4-5 root classes, reasoner consistent in all runs, also with the sample data.

### Follow-ups (proposed)

- Let the events rule prefer the core relations (`hasState`, `precedes`, `changes`) for before/after and order, to
  bring the relations back under the target.
- Before the paper's measured runs: the plan-size check and the report of unsatisfiable classes (`PAPER.md`), then
  VA with DeepSeek V4.1 (on premise), tested by sol.

## Runs 7-dsv41-a to -c - 2026-11-05, DeepSeek-V4.1-Flash on FhGenie, code of df6159b (the open model; generation only)

**Setup.** The same copy as 6a-6c and 7a-7c (`drafts/round7/VA-run-7a.project.json`), generated with the open model
chosen for the paper (`PAPER.md`): DeepSeek-V4.1-Flash on FhGenie, the model's thinking switched off (DECISIONS 144),
a new user id per call against FhGenie's cache (145), with the plan-size call and the unsatisfiable-class check
(147). Generated through the tool's own endpoints in a separate session folder (11:40-12:02 CET); **not yet
tested** - the Evaluate 3x is to be done by gpt-6-sol, as for every configuration of the paper. The VA plan prompt
(44,085 tokens) is accepted by FhGenie.

| | 7a-7c (gpt-6-sol, mean) | **7-dsv41-a** | **7-dsv41-b** | **7-dsv41-c** |
|---|---|---|---|---|
| Planned classes (target 269) | 220 | 106 -> 109 (plan-size call: 5 concepts) | 161 | 282 |
| Central concepts placed by the plan / by the completion | 218 / 42 | **0 / 264** | 200 / 61 | 212 / 50 |
| Central concepts excluded in the end | 4.7 | 0 | 3 | 2 |
| Classes / object properties | 256 / 156 | 224 / 170 | 343 / 154 | 323 / 121 |
| Axioms / class restrictions | 35 / 94 | 47 / **0** | 60 / 56 | 63 / 83 |
| Individuals | - | 18 | 134 | 54 |
| Placeholder classes (referenced, defined by no module) | - | 4 | 4 | 1 |
| Unsatisfiable classes found and removed (DECISIONS 147) | - | `AnchoringBias`: DisjointClasses(User, UserModel, AnchoringBias) | none | `TransparentModel`: DisjointClasses(TransparentModel, MachineLearningModel) |
| Model calls for the generation | 17-21 | 23 | 22 | 20 |
| Attempts | 1 | 1 | **3** (twice the plan answer cut off at 32,000 tokens) | 1 |

### Findings (before the tests)

1. **The open model can generate the VA ontology:** no failed module, 224-343 classes, the reasoner check found one
   unsatisfiable class in two runs and removed its cause (a disjointness between a class and its own superclass).
2. **The plans vary even more than on wine:** 106 to 282 planned classes. Run a's plan placed none of the 264 central
   concepts (no concept ids), so the completion placed all of them, and its modules wrote no class restrictions. The
   plan-size call barely helped there (106 -> 109): in VA the plan does not exclude concepts, it merges several into
   one class, which the call does not reach.
3. **The modules add far more classes than planned** (b: 161 planned, 343 classes) - more detail or superfluous
   elements, to be seen in the tests and the expert review.
4. **A plan can exceed the output limit:** run b's plan was cut off at 32,000 tokens twice (a complete VA plan of 296
   classes took 21,000 tokens). Splitting large plans and modules across calls (open point in DECISIONS) would make
   VA runs with this model reliable.

### Follow-ups (proposed)

- Evaluate 3x of all three by gpt-6-sol (about 15 calls each).
- Split large plans across calls before the paper's measured runs, if the tests make the open model worth it.

## Dry runs 8-dsv41-dry and -dry2 - 2026-11-05, DeepSeek-V4.1-Flash on FhGenie (key notion links, DECISIONS 148-149)

**Setup.** A functional check of the key notion links (DECISIONS 148) before the measured run 8a with gpt-6-sol: two
copies of the 8a project (the copy of 7a with the 19 links the team approved, all "may", none "every"), generated and
tested with DeepSeek-V4.1-Flash (thinking off) through the tool's endpoints in separate session folders; the 8a
project itself was not changed. **Not comparable with the sol runs:** the open model tested its own ontology.
dry: 15:49-15:57 CET, code 8c9e741. dry2: 16:02-16:14 CET, with the fix of DECISIONS 149.

| | dry | dry2 | 7a-7c (sol) | 7-dsv41-a-c |
|---|---|---|---|---|
| Planned classes (target 269) / classes | 258 / 337 | 245 / 323 | 220 / 256 | 106-282 / 224-343 |
| Links added by the tool / already written by a module | 16 / 3 | 16 / 3 | - | - |
| Links not placed below their core relation (domain or range outside it) | 0 | 2 | - | - |
| **Key-notion pairs linked directly** (of 45) | **20** | **20** | 2 / 1 / 1 | 2 / 2 / 2 |
| Key notions with no link to another key notion | 0 | 0 | 6 / 8 / 8 | 6 / 6 / 6 |
| Class restrictions written / kept | 87 / 81 | 100 / 69 | | |
| Reasoner after the generation | **failed** (see below) | consistent, no unsatisfiable class (8 restrictions removed) | | |
| Reasoner alone / with sample data (evaluation) | failed / inconsistent | ok / inconsistent | | |
| CQs in full, 3 tests (own tester) | 6, 8, 10 | 4, 3, 5 | | |
| Hold-out questions in full, 3 tests (own tester) | 3, 5, 3 | 6, 5, 1 | | |
| Model calls for the generation | 21 | 20 | 17-21 | 20-23 |

### Findings

1. **The links work as built:** all 19 approved links are in both ontologies, either added by the tool or written by
   the module that saw them in its prompt. 20 of 45 key-notion pairs are now linked directly, against 1-2 in every
   round-7 run with either model, and no key notion stands alone - the reviewer's point about an overall schema.
2. **Two links could not go below their core relation** in dry2: `examinesData` (core relation `hasInput`) and
   `visuallyEncodesData` (`encodes`) - this generation gave the core relations domains that do not cover Interaction
   and Visualization. The links are kept as properties of their own and listed in the report.
3. **A misspelt parent property hid the whole reasoner result** (dry): a module put `hasInteractionIntent` below
   `support` (the core relation is `supports`); owlready2 failed on the ontology, and with it the restriction check,
   the unsatisfiable-class repair and the evaluation's reasoner. With that one reference removed by hand, HermiT found
   41 unsatisfiable classes, caused by the modules' restrictions together with the disjointness axioms, not by the
   links. Fixed in DECISIONS 149; in dry2 the checks ran and left no unsatisfiable class.
4. **With sample data both are still inconsistent,** as most DeepSeek ontologies in round 7.

### Follow-ups

- Run 8a with gpt-6-sol (restart the server first: DECISIONS 149), then 8b and 8c from the same copy.
- Check the two links that did not fit below their core relation in 8a's report.

## 7a-7c tested by gpt-6-luna - 2026-11-05, 16:48-17:12 CET, code adb50ce (no generation)

Part of a check whether gpt-6-luna can replace gpt-6-sol as the paper's tester; setup, the seven wine ontologies and
the findings are in [`examples/wine/RUNS.md`](../wine/RUNS.md) ("gpt-6-luna as tester"). Evaluate 3x with Luna on
copies of 7a-7c (the projects themselves unchanged), 12-13 calls each.

| | CQs in full, sol | Luna | Hold-out in full, sol | Luna |
|---|---|---|---|---|
| 7a | 9, 9, 9 (9.0) | 7, 8, 8 (7.7) | 3, 5, 2 (3.3) | 3, 2, 2 (2.3) |
| 7b | 10, 10, 9 (9.7) | 6, 5, 5 (5.3) | 5, 3, 4 (4.0) | 1, 3, 2 (2.0) |
| 7c | 8, 9, 8 (8.3) | 6, 7, 8 (7.0) | 3, 4, 6 (4.3) | 3, 3, 4 (3.3) |

Luna is stricter, as on wine, but not evenly: 7b drops from the best of the three to the worst. Luna's reasons on 7b:
no property links a visual encoding to its mark, scale or visualization, and knowledge is not linked to the insight
or cycle it comes from - things that are recorded side by side but not linked to each other.

## Paper cards of five VA papers by four models - 2026-11-06, 17:10-17:17 CET, code b1eca0d (stage A1, PAPER.md)

**Setup.** Five papers of different kinds, from a copy of run 7a: the Uncertainty Events taxonomy (2023), Design
Study Methodology (2012), The Eyes Have It (1996), the Knowledge Generation Model (2014) and Vega-Lite (2017, a
system paper). Extracted by gpt-6-astra, gpt-6-luna (KI:connect) and DeepSeek-V4.1-Flash (FhGenie, thinking off);
compared with the project's own cards (gpt-6-sol). Files: `drafts/round8/va-cards-{astra,luna,dsv41}.json`.

| Cards by | Concepts | Quote found in the text | Relations | Inventory concepts of these papers found (of 203) | of them central (of 146) | Seconds per paper |
|---|---|---|---|---|---|---|
| gpt-6-sol (project) | 213 | 95 % | 128 | 203 (the inventory is built from these cards) | 146 | - |
| gpt-6-astra | 226 | **100 %** | 147 | 164 | 130 | 69-116 |
| DeepSeek V4.1 | **265** | 82 % | 141 | 164 | 130 | 22-41 |
| gpt-6-luna | 154 | 83 % | 73 | 121 | 96 | 25-42 |

### Findings

1. **On VA, grounding separates the models** (on wine all had 96-100 %): Luna and DeepSeek quote less exactly,
   worst in the Uncertainty Events paper (25 of 47 and 22 of 52 quotes found); Astra has all, sol 95 %.
2. **Luna extracts much less on VA:** 22 concepts from Design Study Methodology where the others find 47-53.
3. **Astra is closest to sol** (mean overlap of concept keys per paper 0.59; the other pairs 0.38-0.49).
4. **Every model puts the system of a system paper into its card** (Vega-Lite: `vega lite`, `reactive vega`,
   `signal`, `event selector syntax`, `view algebra`; DeepSeek also `vega lite compiler`, `smart default`). The card
   lists a paper's concepts; leaving a paper's method out is the plan's task (DECISIONS 140).
5. At list price ($10 / $50 per million tokens) Astra's five cards would cost about $2.70; on KI:connect they took 5
   of its 10 daily calls.

Limits: the coverage counts favour sol (the inventory was built from its cards); one extraction per model.

### Found on the way: four papers are in the corpus twice

The Uncertainty Events taxonomy, Design Study Methodology, The Eyes Have It and Characterizing Provenance are each in
the corpus as two files (probably preprint and published version; their cards differ slightly, e.g. 56 and 53
concepts). Since a concept is central when it has two or more sources, every concept of these papers counts as
central only because the paper is there twice - part of the 264 central concepts.

**Done in the 8a project** (2026-11-06, 17:48-17:52 CET, through the user's server; backup of the state before): one
copy of each removed - the copy with the smaller card (`...Visual_Analytics.pdf`, `Shneiderman1996eyes.pdf`, the
longer Characterizing Provenance file, `dsm.pdf`) - and the inventory rebuilt by gpt-6-sol (1 call, 37k / 12k
tokens, 138 s): 50 sources, 1,394 concepts (before 1,395), **176 central (before 264)**, 10 themes (the same topics),
65 definition conflicts (before 58; none had been decided). Key notion links, core relations and hold-out questions
do not refer to inventory concepts and are unchanged. **8a is therefore not directly comparable with 7a-7c**, whose
inventory counted the duplicates.

## Round 8 - 2026-11-09, code 2f91776 (DECISIONS 149-161): 8a, 8b with gpt-6-sol; 8-dsv41-a to -c with DeepSeek

**Setup.** One starting state for all runs (`drafts/round8/VA-run-8-start.project.json`): the 8a project after the
duplicates were removed and the inventory rebuilt (50 sources, 1,394 concepts, 176 central, 65 definition conflicts
undecided), 19 approved key notion links (DECISIONS 148), approved core relations, 10 CQs, 10 hold-out questions.
8a and 8b on the user's server through its API (8c, a copy of the same state, to come); generation, then Evaluate
3x by gpt-6-sol. DeepSeek-V4.1-Flash (FhGenie, thinking off): three generations from the same state; so far b
tested by sol. Not directly comparable with 7a-7c: their inventory still counted the duplicate papers (264 central).

| Run | Classes (planned) | Obj. props | Restr. | Central placed: plan / completion / excluded | Reasoner: alone / with data | CQs in full, 3 tests (mean) | Hold-out in full (mean) |
|---|---|---|---|---|---|---|---|
| 8a (sol) | 223 (196) | 154 | 67 | 159 / 14 / 3 | ok / ok | 9, 9, 8 (8.7) | 4, 3, 4 (3.7) |
| 8b (sol) | 228 (205) | 135 | 89 | 166 / 8 / 2 | ok / ok | 6, 9, 7 (7.3) | 4, 6, 5 (**5.0**) |
| 8-dsv41-a | 154 (117) | 151 | 45 | 0 / 175 / 1 | not loadable (Data Cube link) | - | - |
| 8-dsv41-b | 223 (203) | 170 | 76 | 130 / 44 / 2 | not loadable (Data Cube link) | 6, 7, 5 (6.0) | 2, 2, 2 (2.0) |
| 8-dsv41-c | 282 (227) | 205 | 60 | 151 / 24 / 1 | - | - | - |
| 7a-7c (round 7, sol) | 232-269 | 106-121 module | 94 | - | ok / ok | 9.0 / 9.7 / 8.3 (9.0) | 3.9 |

Generation with sol: 17-18 calls, 7-8 minutes, about 173k input and 76k output tokens; Evaluate 3x 13 calls each.
All 19 key notion links are in 8a and 8b (none dropped below its core relation, the dry runs had 1-2); the
restriction check removed nothing; no unsatisfiable class, no upper-layer collision. Relations per class 0.35 and
0.32 (8-dsv41-b 0.20). In 8-dsv41-c the new restriction search (DECISIONS 161) removed 27 of 87 restrictions in 16
reasoner runs instead of all.

**Tested by gpt-6-luna as well** (copies, 12 and 15 calls): 8a 7, 9, 7 (7.7), 8b 5, 8, 6 (6.3) - one point under sol,
the same order; 8-dsv41-b 5, 3, 2 (3.3) against sol's 6.0 - 2.7 points under sol on the open model's ontology.

**DeepSeek again, on the fixed code** (`8-dsv41r-a` to `-c`, 11:18-11:36 CET; with DECISIONS 162, `-a` also with 163):
the same start, generation only, sol tests to come.

| Run | Classes (planned) | Restr. kept | Removed by the restriction check | Data Cube links |
|---|---|---|---|---|
| 8-dsv41r-a | 253 (224) | 59 | 9 (on classes they made unsatisfiable) | none |
| 8-dsv41r-b | 238 (184) | 50 | 31 by the search; budget of 24 runs used up, 5 left out untested | none |
| 8-dsv41r-c | 291 (253) | 61 | 28 by the search (22 runs) | none |

The first attempt of `-a` failed after 5 minutes (about 218,000 input tokens): the Turtle did not parse, and the
reasoner check during the merge raised the parse error uncaught, which ended the whole request (fixed in DECISIONS
163; the cause of the invalid Turtle is unknown, nothing was saved).

### Findings

1. **8a and 8b are at the level of round 7** with a cleaner inventory: 8.0 of 10 CQs on average (7a-7c 9.0, within
   the spread of three runs), 4.4 of 10 hold-out questions (3.9); 8b's 5.0 is the best hold-out result so far.
2. **The filtering and zooming question fell back to "partial"** in all six tests of 8a and 8b (7b, 7c: full; 7a:
   partial). The modelling is the same as in 7b/7c (state classes, before/after relations below `hasInput`,
   `produces`, `hasState`); the tester asks for the displayed content before and after and for what semantic zooming
   reveals - as in 7a. Probably the variance seen in round 7, not the events rule (DECISIONS 156); 8c will show more.
3. **DeepSeek on VA: about three quarters of sol on the CQs, less than half on the hold-out questions** (6.0 and 2.0
   against 8.0 and 4.4), with fewer relations (0.20 per class). In 8-dsv41-a the plan assigned no central concept
   itself - the completion placed 175 of 176.
4. **Two of three DeepSeek ontologies could not be loaded by owlready2** ("metaclass conflict"): `Axis` below
   `qb:DimensionProperty`, `Field` and `Attribute` below `qb:AttributeProperty` - Data Cube's classes of properties.
   The restriction check was skipped during generation and the evaluation had no reasoner result. Fixed in
   DECISIONS 162 (such terms are no longer candidates for class links); sol did not make such links.

### Follow-ups

- Restart the server (DECISIONS 162, 163), then 8c with sol; sol tests of 8-dsv41r-a to -c (the runs on the fixed
  code; 8-dsv41-a to -c stay as the state before the fixes).
- Filtering/zooming question: compare 8c; if it fails again, look at what the sample data record about the displayed
  state.
- A version for the domain expert who gave the feedback of DECISIONS 148: 8a and 8b link 20 of 45 key-notion pairs
  directly (round 7: 1-2), Knowledge-Task among them, but **Knowledge-User and Model-Task are not linked at all**,
  not even through the modules - neither pair was among the 19 approved links. Add the two links (e.g. `User
  gainsKnowledge Knowledge`, `Model supportsTask Task`) to a copy of the round-8 start (not to 8c, which stays
  comparable with 8a and 8b), generate with sol and test it (about 18 + 13 calls). 8a is exported for the expert
  in the meantime (`drafts/round8/expert-8a/`, Turtle and documentation).

### 8c and a version for the domain expert - 2026-11-10, 10:33-11:05 CET, code d63dc18 (DECISIONS 162, 163)

**Found before the runs: 8a and 8b were generated without the selected standards.** The script that drove the
server's API read the session one level too high (`/api/session/{id}` wraps the project), so it sent no standards
and an empty domain description. The use case falls back to the same text, and the loaded vocabularies were used as
usual (8a and 8b have PROV-O and DCAT links); only the "Standards to reuse" block of the module prompts (seven names
with reuse hints) was missing. Fixed for 8c and the expert version; 8a and 8b stay as they are, with this note.

**The expert version** (`8-expert`): a copy of the round-8 start with two more approved key-notion links - `User
acquiresKnowledge Knowledge` (no core relation fits a person and an information object) and `Model supportsTask Task`
(below `supports`), neither "every" - for the two pairs the expert named that 8a and 8b left unlinked.

| Run | Classes (planned) | Obj. props | Restr. | Rel. per class | Key-notion pairs direct | Reasoner alone / with data | CQs in full, 3 tests (mean) | Hold-out in full (mean) |
|---|---|---|---|---|---|---|---|---|
| 8a (no standards) | 223 (196) | 154 | 67 | 0.35 | 20 | ok / ok | 9, 9, 8 (8.7) | 4, 3, 4 (3.7) |
| 8b (no standards) | 228 (205) | 135 | 89 | 0.32 | 20 | ok / ok | 6, 9, 7 (7.3) | 4, 6, 5 (5.0) |
| 8c | 235 (203) | 130 | 88 | 0.28 | 19 | ok / ok | 5, 7, 7 (6.3) | 3, 6, 2 (3.7) |
| 8-expert | 195 (165) | 129 | 74 | 0.34 | **21, incl. Knowledge-User and Model-Task** | ok / ok | 8, 8, 9 (8.3) | 2, 2, 2 (2.0) |

Generation 19 calls each (8c 6 minutes, the expert version 15 - slow responses), Evaluate 3x 14 calls each.

- **The standards block did not make 8c better:** 6.3 against 8.7 and 7.3; 8c is partial on marks/channels/scales
  (Q4) and annotations (Q10) in all three tests - the ontology, not the test.
- **The filtering and zooming question** was partial in all nine tests of 8a-8c, but full in 2 of 3 tests of the
  expert version.
- **The expert version links all three pairs of the expert's feedback directly** (Knowledge-Task, Knowledge-User,
  Model-Task); Uncertainty-User, direct in 8a, is linked only through the modules. Exported for the expert:
  `drafts/round8/expert/` (Turtle and documentation; replaces the 8a export).

### The spread of the CQ tests, and the check with the verdict "test" (DECISIONS 164) - 2026-11-10

Of the 30 questions of 8a-8c, 24 got the same verdict in all three tests; 6 flipped and decided the spread (8a: Q4;
8b: Q2, Q4, Q6; 8c: Q7, Q9). Several of their stated gaps lay in the test, not in the ontology (8a Q4: "The
ontology has the relations needed"; 8b Q6: two steps of the sample data not stated to be the same; 8c Q7: the query
follows only one interaction). DECISIONS 164 lets the check of partial answers call such a gap "test" (with the
ontology terms that record it, which must exist) and adds the majority verdict per question.

**Validation:** the new check on the stored first test of 8a, 8b, 8c and the expert version, every answer with a
stated gap (57; also those the old check had lifted as "beyond"), 8 sol calls:

| | 8a | 8b | 8c | 8-expert |
|---|---|---|---|---|
| CQs in full, first test: old check / new check | 9 / 10 | 6 / 8 | 5 / 7 | 8 / 9 |
| ... the other two tests (old check) | 9, 8 | 9, 7 | 7, 7 | 8, 9 |
| Hold-out in full, first test: old / new | 4 / 5 | 4 / 4 | 3 / 4 | 2 / 4 |
| CQs by majority (old check) | 9 | 7 | 7 | 8 |

11 partial answers became full - 7 by "test" (e.g. 8b Q6 `:propagatesThrough`, 8c Q9 `:hasParticipant`, expert Q6
`:introducesUncertainty`; doubtful: 8a Q5, filtering and zooming, where the check names the before/after state
relations although the displayed content is not recorded), 4 by "beyond" - and one full answer became partial (8c
hold-out Q8). The low first runs move towards the other two (8b 6 -> 8, 8c 5 -> 7). Whether the spread of fresh runs
shrinks needs one Evaluate 3x with the new code (about 14 calls). The check is itself not deterministic: the 4
"beyond" and the one "beyond -> missing" did not need the new option.

**8b evaluated again with DECISIONS 164** (Evaluate 3x, fresh, 15 calls, 2026-11-10 afternoon, code b40d1fc):

| 8b | CQs in full (mean, sd) | CQs by majority | Questions that vary | Hold-out in full (mean, sd) |
|---|---|---|---|---|
| Old check (2026-11-09) | 6, 9, 7 (7.3, 1.5) | 7 | 3 (Q2, Q4, Q6) | 4, 6, 5 (5.0, 1.0) |
| New check | **8, 8, 8 (8.0, 0.0)** | **9** | 3 (Q2, Q9, Q10) | 6, 6, 4 (5.3, 1.2) |

The counts per test no longer differ, and Q4 and Q6 are full in all three tests (Q4 by "test": `:encodes`,
`:mapsDataValueToVisualValue`). Still, three questions flipped once each, in different tests - the sd of 0 is partly
luck; per question the test is steadier, not stable. Q2 (data structures, measurement types) was "missing" in the
first test and full in the other two; Q5 (filtering and zooming) stays partial in all three: the ontology records the
states before and after an interaction, not the displayed content or the level of detail. The hold-out questions did
not get steadier (one run of three is not enough to tell).

## Stage C: core relations and key-notion links by other models - 2026-11-10, 12:20 CET, code 385a23e

From the round-8 start (the inventory after the duplicates were removed, 10 key notions, 10 CQs), each model
proposed the core relations (step 7, before the generation) and, with the approved core relations frozen, the
key-notion links. gpt-6-sol once (its own spread), gpt-6-luna and DeepSeek-V4.1-Flash three times each; 2 sol, 6 Luna
calls, about a minute per proposal. Compared with the approved sets (sol's proposals, approved by the team: 39 core
relations, 19 links over 19 pairs); names compared after splitting and stemming, so a synonym counts as different.

| Run | Core relations | ... names also approved | ... with domain or range | Links kept (dropped by the check) | Pairs also approved (of 19) | Jaccard of pairs | Expert pairs linked (of 3) | Key notions left unlinked |
|---|---|---|---|---|---|---|---|---|
| sol, second proposal | 30 | 20 | 26 | 20 (0) | 16 | 0.73 | 1 (Knowledge-Task) | - |
| Luna 1 | 27 | 19 | 19 | 15 (0) | 11 | 0.48 | 1 (Knowledge-User) | - |
| Luna 2 | 28 | 18 | 18 | 14 (2) | 11 | 0.52 | 0 | - |
| Luna 3 | 32 | 20 | 27 | 16 (0) | 13 | 0.59 | 1 (Knowledge-Task) | - |
| DeepSeek 1 | 25 | 15 | 7 | 16 (4) | 10 | 0.40 | 1 (Knowledge-User) | ApplicationDomain |
| DeepSeek 2 | 35 | 14 | 8 | 3 (14) | 1 | 0.05 | 0 | ApplicationDomain, Data, Interaction, Provenance |
| DeepSeek 3 | 28 | 17 | 14 | 11 (10) | 7 | 0.30 | 1 (Knowledge-Task) | - |

Agreement between a model's own runs (mean Jaccard): Luna 0.45 for core-relation names, 0.52 for link pairs;
DeepSeek 0.24 and 0.11.

**Findings.**
1. **The links depend on the model; sol is closest to itself.** A second sol proposal shares 16 of the 19 approved
   pairs, Luna 11-13, DeepSeek 1-10. Core-relation names vary even for sol (20 of 39 again) - the names are a weak
   measure; what the generation needs (domain and range) separates the models more: sol 26 of 30, Luna 18-27,
   DeepSeek 7-14.
2. **DeepSeek does not keep the naming rule:** it uses core relations as link names (`records`, `isDerivedFrom`,
   `encodes`), which the tool's check drops - 14 of 17 links in its second run. The check works as built; a
   retry with the reasons would be an option for open models.
3. **No model finds the expert's missing pairs reliably:** Model-Task in none of the 7 runs, Knowledge-User in 2
   (Luna 1, DeepSeek 1). The review by the team or a domain expert adds what the models miss, whatever the model.

### Follow-ups

- Sol tests of 8-dsv41r-a to -c (about 42 calls), now with DECISIONS 164 - compare them with the new 8b figures, not
  with the old ones.
- More evidence on the spread: the next Evaluate 3x runs with the new check (no extra runs only for this).

## Three testers with the check of DECISIONS 164 - 2026-11-10/11, code b88ac11 (wine figures in `examples/wine/RUNS.md`)

The same nine ontologies - VA 8b and the three DeepSeek reruns 8-dsv41r-a to -c, five wine ontologies - tested
by gpt-6-sol, gpt-6-luna and DeepSeek-V4.1-Flash (thinking off), Evaluate 3x from scratch each, every verdict of the
check of partial answers recorded (`drafts/scripts/run_tester_recheck.py`, `tester_compare.py`). Luna and DeepSeek on
2026-11-10, sol on 2026-11-11 (11:45-12:14 CET, 93 calls; 8b: its server re-test of 2026-11-10). The sol figures of
8-dsv41r-a to -c are also the overdue sol tests of the DeepSeek reruns.

| VA ontology | sol: CQs in full (mean; majority) | Luna | DeepSeek | Hold-out in full, sol / Luna / DeepSeek |
|---|---|---|---|---|
| 8b (sol) | 8, 8, 8 (8.0; 9) | 8, 5, 8 (7.0; 7) | 6, 8, 6 (6.7; 8) | 5.3 / 4.7 / 3.3 |
| 8-dsv41r-a (DeepSeek) | 9, 9, 8 (8.7; 9) | 9, 9, 7 (8.3; 9) | 3, 6, 5 (4.7; 6) | 4.3 / 3.3 / 3.0 |
| 8-dsv41r-b (DeepSeek) | 7, 8, 7 (7.3; 7) | 5, 5, 5 (5.0; 5) | 0, 6, 7 (4.3; 6) | 2.0 / 1.7 / 2.0 |
| 8-dsv41r-c (DeepSeek) | 8, 7, 9 (8.0; 8) | 6, 8, 3 (5.7; 6) | 7, 9, 5 (7.0; 8) | 4.7 / 3.0 / 4.3 |

**Findings.**
1. **The DeepSeek generations on the fixed code are at sol's level on the CQs:** 8.7, 7.3 and 8.0 of 10 (mean 8.0)
   against 8.0 for 8b, all with the new check and the same tester. Before the fixes of DECISIONS 162-163,
   8-dsv41-b reached 6.0 (old check). On the hold-out questions they stay below 8b (2.0-4.7 against 5.3).
   For the paper: the generation can run on an open model hosted in-house.
2. **Luna keeps sol's order** of the four VA ontologies (5 of 5 pairs), 1.5 points lower; **DeepSeek does not**
   (3 of 5), 2.3 lower, and its three tests of one ontology differ by up to 7 (0, 6, 7).
3. Over all nine ontologies: the majority verdict per question agrees with sol on 71 of 90 questions for Luna, 60
   of 90 for DeepSeek. Spread of the three tests of one ontology (sd): sol 0.51, Luna 0.78, DeepSeek 1.40.
4. **Check of partial answers:** sol called 12 gaps "test", Luna 40, DeepSeek 22; DeepSeek named terms that do not
   exist 29 times (the rule of DECISIONS 164 turned them into "missing"), sol and Luna never.
5. **Tester decision:** sol stays the tester. Luna is usable where many runs are needed, as a check of the order,
   not of the level; DeepSeek is not usable as a tester yet - LITMO can generate on premise, but not yet test there.


## 8a and 8c re-tested with the check of DECISIONS 164 - 2026-11-12, 12:44-12:53 CET, code 586535f

Evaluate 3x by sol on the stored round-8 ontologies (26 calls), so all VA figures use the same check.

| VA ontology | CQs in full, new check (mean; majority) | Old check (mean) | Hold-out in full, new (mean) | Old |
|---|---|---|---|---|
| 8a | 9, 9, 9 (9.0; 9) | 8.7 | 4, 4, 4 (4.0) | 3.7 |
| 8b (2026-11-10/11) | 8, 8, 8 (8.0; 9) | 7.3 | 5.3 | 5.0 |
| 8c | 7, 9, 8 (8.0; 8) | 6.3 | 6, 5, 4 (5.0) | 3.7 |
| 8-expert (2026-11-13, 13:59-14:04 CET, 12 calls) | 10, 8, 9 (9.0; 9) | 8.3 | 3, 2, 3 (2.7) | 2.0 |

Checks of partial answers: 8a "test" 2, beyond the ontology 15, missing 20; 8c 6, 13, 18; no unknown terms.
The three sol runs now lie at 8.0-9.0 (before 6.3-8.7); the gap between 8a and 8c shrinks from 2.4 to 1.0. The
expert version (checks: "test" 3, beyond 14, missing 25) answers the team's questions as well as 8a (9.0) but stays
lowest on the hold-out questions (2.7 against 4.0-5.3): it has the fewest classes of the four (195).

## VA entirely on DeepSeek - 2026-11-12, 12:43-13:33 CET, code 586535f (step 4 of the sol budget)

DeepSeek-V4.1-Flash (FhGenie, thinking off) for every model step from the round-8 start: paper cards of the 50
papers, the inventory, the generation (`drafts/scripts/run_va_open.py`; `drafts/round8/VA-run-9-open.project.json`).
No sol calls; the sol test is due on 13 Nov.

- **Cards:** all 50 done; 82 % of the quotes found in the paper text. Three papers are low: a book on the semiology
  of graphics 5 of 54, a taxonomy paper 11 of 37, a survey of uncertainty visualisation 0 of 53 - to be checked
  whether their extracted text is usable.
- **Inventory: not consolidated.** DeepSeek's merge answer was cut off at the client's output limit of 32,000 tokens
  (input 54,661 tokens, 1,712 concepts from 50 papers). LITMO fell back to grouping by name as designed: 288
  concepts named by at least two papers, no themes, no definition conflicts. (Round 8 with sol's cards: 177 by
  name, 176 after sol's merge - most of the difference comes from DeepSeek's cards, not from the missing merge.)
- **Generation:** 22 calls, 443 s, 340 classes (planned 286; round 8 with sol 196-205), 30 class restrictions, no
  module errors, reasoner consistent.

**Findings.**
1. The whole pipeline runs end to end on an open model, but the **merge step does not scale to 50 papers in one
   call** with DeepSeek: it writes more than twice what sol wrote (sol: 12,145 output tokens for 1,394 concepts)
   and runs into the output limit. On wine (5 papers) it worked. The plan is about 40 % larger than with sol's
   inputs, mostly because DeepSeek's cards name more concepts that recur across papers.
2. The warning shown in the inventory step is the generic text of the truncation error ("reduce the ontology: fewer
   modules or key notions"), which does not fit this step.
3. **Plan (decided 2026-11-12):** test this run on 13 Nov as the "before" (all open, merge fallen back to name
   grouping); build the two-stage consolidation (DECISIONS, open points); redo the inventory and generation with
   DeepSeek and test the "after" before the evaluation freeze. Built the same day (DECISIONS 169), see below. Not chosen: only raising the output
   limit for this server - it moves the limit but does not remove it for larger corpora.

### The same cards with the two-stage consolidation (DECISIONS 169) - 2026-11-12, 15:27-15:30 CET

DeepSeek's 50 cards from above, inventory only, by DeepSeek with the two-pass merge (`drafts/scripts/run_va_open_inventory.py`;
`drafts/scripts/results/va-inventory-open-2stage.json`). Free; no generation yet.

| Inventory | Concepts | Named by 2+ sources | Themes | Conflicts | Consolidated definitions | Output tokens |
|---|---|---|---|---|---|---|
| sol, one call, sol's cards (round-8 start) | 1,394 | 176 | 10 | 65 | - | 12,145 |
| DeepSeek, one call (above) | 1,712 | 288 (by name only) | 0 | 0 | 0 | 32,000, cut off |
| DeepSeek, two passes | 1,689 | 270 | 11 | 118 | 116 | 33,662 in 8 calls |

**Findings.**
1. **The merge now completes on DeepSeek:** 1 + 7 calls in 162 s, no part failed, no call near the limit. The
   eleven themes match sol's ten closely (data, uncertainty, visual encoding, interaction, tasks and reasoning,
   provenance, evaluation, machine learning, design); DeepSeek splits visualisation techniques from visual variables.
2. **DeepSeek merges little:** 23 concepts fewer (1,712 to 1,689), the central ones from 288 to 270. Sol's and DeepSeek's central concepts
   share 93 labels; the rest differ mostly because the cards differ.
3. **DeepSeek reports almost twice as many definition conflicts** (118 against 65), some of them differences in
   emphasis rather than meaning. They go to the team as proposals, as with sol; whether they are real is for the
   review, not measured here.
4. Next: generation with DeepSeek from this inventory (free), then the sol test as the "after" (about 15 calls).

### Generation from the two-pass inventory (step 4b) - 2026-11-12, 16:02-16:09 CET, code 2f88ad9

DeepSeek generates from the stored two-pass inventory and its own cards, the team inputs of round 8 as before
(`drafts/scripts/run_va_open2_generate.py`; `drafts/round8/VA-run-9-open2.project.json`). Free; the sol test is
due on 13 Nov, together with the "before".

| VA ontology | Classes (planned) | With sources | Linked to inventory concepts | Modules | Class restrictions | Calls |
|---|---|---|---|---|---|---|
| 8a (sol, sol's inventory) | 223 | 214 | 195 | 11 | - | - |
| 9-open (DeepSeek, merge fell back to names) | 340 (286) | 324 | 292 | 11 | 30 | 22 |
| 9-open2 (DeepSeek, two-pass merge) | 281 (266) | 268 | 259 | 12 | 36 | 24 |

No module errors, reasoner consistent. One module answer was invalid JSON and was repaired by the tool's JSON-repair
call; one rate-limit wait of 5 s. The two-pass inventory makes the plan about 7 % smaller (266 against 286 classes) and
the ontology 17 % smaller (281 against 340); it stays larger than sol's, as expected from DeepSeek's cards.

### Sol test of 9-open (the "before") - 2026-11-12, 16:17-16:21 CET, code a5a4475

Evaluate 3x by sol with the check of DECISIONS 164 (`drafts/scripts/run_soltest_file.py`;
`drafts/round8/VA-run-9-open-soltest.project.json`), 16 calls.

| VA ontology | CQs in full (mean; majority) | Hold-out in full (mean; majority) |
|---|---|---|
| 8a (sol) | 9, 9, 9 (9.0; 9) | 4, 4, 4 (4.0) |
| 8-dsv41r-a to -c (DeepSeek generation, sol's cards and inventory) | mean 8.0 | 2.0-4.7 |
| **9-open (all DeepSeek, merge fell back to names)** | **7, 8, 7 (7.3; 8)** | **3, 3, 2 (2.7; 3)** |

No question unanswered in any run; on the hold-out questions 5-7 partial and 1-2 not answered. All on DeepSeek, the
ontology answers 7-8 of the 10 team questions in full - about one question below the DeepSeek generations from
sol's cards and inventory, and within the range of the hold-out results of those. The "after" (9-open2, two-pass
merge) is tested on 13 Nov.

### Sol test of 9-open2 (the "after") - 2026-11-13, 13:28-13:34 CET, code c0f736e

Evaluate 3x by sol as for 9-open (`drafts/round8/VA-run-9-open2-soltest.project.json`), 13 calls.

| VA ontology (all DeepSeek) | Classes | CQs in full (mean; majority) | Hold-out in full (mean; majority) |
|---|---|---|---|
| 9-open (merge fell back to names) | 340 | 7, 8, 7 (7.3; 8) | 3, 3, 2 (2.7; 3) |
| 9-open2 (two-pass merge) | 281 | 9, 8, 7 (8.0; 9) | 3, 3, 5 (3.7; 3) |
| for comparison: DeepSeek generations from sol's cards and inventory (8-dsv41r-a to -c) | 238-291 | mean 8.0 | 2.0-4.7 |

With the two-pass merge the all-DeepSeek ontology is smaller and reaches the level of the DeepSeek generations from
sol's inputs (8.0 of 10). The gain over 9-open (0.7 team questions, 1.0 hold-out) is within the spread of three tests
(sd up to 1.2) and rests on one generation each, so it shows no loss, not a proven gain. For the paper: every model step
of LITMO, from the paper cards to the generation, ran on DeepSeek hosted in-house, at the level of a DeepSeek
generation from sol's cards and inventory; testing still needs sol.

## VA without literature (ablation, step 1b) - 2026-11-13/14, code c0f736e, gpt-6-sol

Three generations by sol from the round-8 start with the papers, cards and inventory removed (same use case, 10 CQs,
key notions, approved core relations and key-notion links, standards), Evaluate 3x each with the check of DECISIONS
164 (`drafts/scripts/run_va_ablation.py`; `drafts/round8/VA-run-9-nolit-{a,b,c}.project.json`). Run a on 13 Nov,
13:28-13:40 CET (30 calls); b and c on 14 Nov, 16:08-16:23 CET (63 calls). For the test only, the round-8 inventory
and its 10 stored hold-out questions were put back - the CQ test does not read the inventory, but without one LITMO
has no hold-out questions. The comparison is 8a-8c, the same start with literature (all with the new check).

| VA ontology | Classes (planned) | CQs in full (mean) | Hold-out in full, 3 tests (mean) | Hold-out majority: full / partial / none | Central concepts (of 176) as a class | Classes with sources |
|---|---|---|---|---|---|---|
| 8a (with literature) | 223 (196) | 9, 9, 9 (9.0) | 4, 4, 4 (4.0) | 4 / 6 / 0 | 156 | 96 % |
| 8b (with literature) | 228 (205) | 8, 8, 8 (8.0) | 6, 6, 4 (5.3) | 6 / 4 / 0 | 154 | 96 % |
| 8c (with literature) | 235 (203) | 7, 9, 8 (8.0) | 6, 5, 4 (5.0) | 5 / 4 / 1 | 150 | 91 % |
| 9-nolit-a (without) | 114 (97) | 8, 9, 8 (8.3) | 2, 1, 4 (2.3) | 2 / 6 / 2 | 45 | 0 % |
| 9-nolit-b (without) | 115 (102) | 8, 8, 9 (8.3) | 2, 4, 5 (3.7) | 4 / 4 / 2 | 47 | 0 % |
| 9-nolit-c (without) | 116 (108) | 8, 10, 7 (8.3) | 3, 4, 4 (3.7) | 4 / 4 / 2 | 47 | 0 % |

**Findings.**
1. **The team's questions do not need the literature:** 8.3 of 10 in every run without it, 8.3 on average with it
   (8.0-9.0); as on wine (9.0 against 9.1).
2. **The questions the generation did not see gain from it, less than run a alone suggested:** hold-out 3.2 of 10
   in full without the literature (2.3-3.7), 4.8 with it (4.0-5.3); by majority 3.3 against 5.0. The ranges do not
   overlap. Without literature every ontology leaves 2 hold-out questions entirely unanswered, with it 0-1. Run a
   alone (2.3, "about half") overstated the gap; three runs give about a third fewer.
3. **Breadth and traceability as on wine:** half the classes (114-116 against 223-235), a quarter of the central
   concepts as a class (45-47 against 150-156 of 176), no class with a source. The three runs without literature
   are very alike in size, the plan grows from the questions and key notions only.
4. **Caveat:** the hold-out questions come from the same literature as the inventory, so they favour it by
   construction - they measure whether the literature's breadth answers the literature's questions, not questions of
   real users. The difference of 1.6 questions is larger than the spread of one ontology's three tests (sd 0.6-1.5)
   only on average; per ontology the ranges touch (8a 4.0 against b and c 3.7).
