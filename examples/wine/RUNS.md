# Runs of the wine test project

Inputs and what to record: [README.md](README.md). Newest run first.


## Without literature (ablation) - 2026-11-12, 12:44-12:59 CET, code 586535f, gpt-6-sol

Three generations by sol from the round-7 start with the papers, cards and inventory removed (same use case,
competency questions, key notions and core relations), Evaluate 3x each with the check of DECISIONS 164
(`drafts/scripts/run_wine_ablation.py`; projects `drafts/round8/wine-9-nolit-{a,b,c}.project.json`). 56 sol calls.
The comparison is sol's three runs with literature, 7a-7c.

| Run | Classes (planned) | CQs in full (mean; majority) |
|---|---|---|
| 9-nolit-a | 48 (41) | 10, 9, 9 (9.3; 9) |
| 9-nolit-b | 44 (38) | 9, 9, 9 (9.0; 9) |
| 9-nolit-c | 41 (35) | 9, 8, 9 (8.7; 9) |
| 7a (with literature) | 68 | 9, 10, 10 (9.7; 10) |
| 7b (with literature) | 76 | 10, 9, 9 (9.3; 10) |
| 7c (with literature) | 67 | 7, 9, 9 (8.3; 9) |

Of the inventory's 82 concepts, the runs without literature have 15-17 as a class, 7a-7c 43-58. Classes with
sources: none without literature, 44-58 with it.

**Findings.**
1. **The literature does not raise the wine CQ score:** 9.0 of 10 on average without it (8.7-9.3), 9.1 with it
   (8.3-9.7; 7a and 7c re-tested with the new check on 2026-11-13, 13:28-13:34 CET, 13 sol calls). The ten questions
   can be answered from the use case alone.
2. **It brings breadth and traceability:** two thirds more classes, about three times as many of the inventory's
   concepts, and 44-58 classes with a source against none. Caveat: the breadth is measured against an inventory built
   from the same literature; whether the extra concepts matter has to come from hold-out questions (VA ablation,
   13 Nov) or the expert.


## Three testers with the check of DECISIONS 164 - 2026-11-10/11 (VA figures and method in `examples/va/RUNS.md`)

Five wine ontologies tested by gpt-6-sol, gpt-6-luna and DeepSeek-V4.1-Flash, Evaluate 3x each, new check.

| Wine ontology | sol: CQs in full (mean; majority) | Luna | DeepSeek |
|---|---|---|---|
| 7b (sol generation) | 10, 9, 9 (9.3; 10) | 8, 9, 8 (8.3; 9) | 2, 5, 7 (4.7; 5) |
| 8-opus-a | 10, 9, 9 (9.3; 10) | 10, 10, 10 (10.0; 10) | 6, 6, 5 (5.7; 6) |
| 8-sonnet-a | 9, 8, 8 (8.3; 8) | 9, 7, 8 (8.0; 8) | 7, 6, 6 (6.3; 6) |
| 7-dsv41r-b (DeepSeek) | 7, 7, 5 (6.3; 7) | 6, 5, 4 (5.0; 4) | 2, 3, 5 (3.3; 3) |
| 8-open (all steps DeepSeek) | 6, 5, 6 (5.7; 5) | 6, 6, 5 (5.7; 6) | 7, 4, 4 (5.0; 5) |

Luna keeps sol's order in 8 of 9 pairs and is 0.4 points lower on average; DeepSeek keeps it in 5 of 9, 2.8 points
lower, and rates the best ontologies (sol, Opus) below Sonnet's. With the new check Luna is no longer clearly stricter
than sol on wine (old check: about 1.2 points).

**The other two DeepSeek reruns with sol** (2026-11-13, 16:47-16:51 CET, 17 calls, new check): 7-dsv41r-a 6, 5, 5
(5.3; majority 5), 7-dsv41r-c 6, 8, 7 (7.0; 8). With b, the three DeepSeek generations reach 6.2 of 10 on average
(5.3-7.0), sol's three 9.1 (8.3-9.7): on wine the gap between the generating models stays about three questions, while
on VA the DeepSeek generations from sol's inputs reach sol's level (8.0 against 8.3).

## Paper cards and inventories by six models - 2026-11-06, 15:11-16:20 CET, code b1eca0d (stage A1, PAPER.md)

**Setup.** The five wine sources extracted to paper cards by gpt-6-sol, DeepSeek-V4.1-Flash (FhGenie, thinking off),
claude-sonnet-5-5, claude-opus-5-5 and gpt-6-astra (KI:connect, 16:12-16:20), from the round 7 copy; gpt-6-luna's
cards are those of the v0.2 walkthrough. Then one concept inventory per card set, **all merged by gpt-6-sol** (one
call each), so that the differences come from the cards alone. Two inventory concepts match when their label or
variants share a comparison key. Files: `drafts/round8/wine-cards*.json`, `drafts/round8/wine-inventories.json`.

| Cards by | Concepts (distinct) | Quote found in the text | Relations | Tokens in / out | Cost | Inventory: concepts / central / themes / conflicts | Consensus core covered (of 104) | Only in this inventory |
|---|---|---|---|---|---|---|---|---|
| gpt-6-luna | 109 (95) | 96 % | 60 | 54k / 18k | - | 81 / 12 / 7 / 3 | 58 | 6 |
| gpt-6-sol | 124 (108) | 98 % | 72 | 61k / 17k | - | 102 / 15 / 7 / 5 | 74 | 1 |
| DeepSeek V4.1 | 221 (200) | 98 % | 112 | 62k / 28k | - | 179 / 25 / 7 / 9 | 92 | 24 |
| Sonnet 5.5 | 128 (109) | 98 % | 57 | 94k / 19k | $0.37 | 90 / 20 / 9 / 7 | 63 | 3 |
| Opus 5.5 | 227 (202) | **100 %** | 112 | 94k / 50k | $1.37 | 174 / **30** / 8 / 12 | **102** | 25 |
| gpt-6-astra | 196 (172) | **100 %** | **144** | 61k / 30k | (about $2.10 at list price) | 161 / 24 / 8 / 9 | 93 | 11 |

Central: in more than one source (as the plan uses it). Consensus core: concepts in at least 3 of the 6 inventories.
Astra's price is from third-party sources ($10 / $50 per million tokens); through KI:connect it costs daily calls
only (10 a day, 5 used). Astra took 66-95 s per source, the others 16-58 s (Opus 58-104 s).

### Findings

1. **Grounding does not separate the models:** 96-100 % of the verbatim quotes are found in the full text.
2. **The central core does not depend on the card model:** 15 concepts are central in at least 3 inventories (wine,
   white wine, food, meal, pairing, grape, vintage, region, producer, body, nose, tannin, acid, fat, fruit); every
   inventory has all 15 except Sonnet's (no "fat").
3. **Beyond the core the models differ widely:** two card sets share 30-54 % of their concepts. Opus covers 102 of
   the 104 core concepts (missing only "class" and "ontology"), Astra 93, DeepSeek 92; Sonnet and sol miss domain
   concepts (the three wine acids, fish, meat; Sonnet also rose and salty, sol the wine faults); Luna and Astra mostly
   method terms (class, slot, facet, knowledge base, competency question).
4. **Consensus is not relevance:** the core also holds method terms that several models took from Noy & McGuinness
   and the OWL guide; the plan excludes them later (DECISIONS 140).
5. **Opus, Astra and DeepSeek extract about twice as much**, but differently: Opus mostly domain detail (Bordeaux,
   Medoc, Pauillac, Riesling, Zinfandel, wine glass); Astra is closest to Opus (Jaccard 0.52) and sol (0.51), adds
   the pairing types of the food-pairing article (acid, fat, salt, sweet pairing) and has the most relations;
   DeepSeek also noise (OWL terms such as `owl lite`, `cardinality`; WineGraph's method such as `word2vec`,
   `metapath2vec`; relations written as concepts such as `has color`).
6. **The card model sets the size of the plan's task:** Opus, DeepSeek and Astra give 2-2.5 times as many central
   concepts as Luna (24-30 against 12).
7. **The merge is stable:** Luna's cards merged by sol give 81 concepts and 12 central, the original (merged by
   Luna) 82 and 12.
8. Claude counts the same texts as about 50 % more input tokens (its tokenizer); token numbers are not comparable
   across providers.

Limits: one extraction per model; the matching by variants joins a few groups that do not belong together (the
largest mixes body, sweetness, sugar and flavour, as Luna's inventory already did), and it misses different wordings
(Astra's "lactic", "malic", "tartaric" do not match "lactic acid" etc.); both lower the coverage counts. A coverage
measure against concepts marked by hand is still to come.

### The merge varied, and the first all-open run (17:10-17:12 CET)

**Stage A2:** gpt-6-sol's cards merged into an inventory by three models (one call each; DeepSeek on FhGenie,
thinking off). File: `drafts/round8/wine-inventories-a2.json`.

| Cards by | Merged by | Concepts | Central | Themes | Conflicts |
|---|---|---|---|---|---|
| gpt-6-sol | gpt-6-sol (above) | 102 | 15 | 7 | 5 |
| gpt-6-sol | gpt-6-luna | 102 | 15 | 8 | 3 |
| gpt-6-sol | DeepSeek V4.1 | 85 | 18 | 8 | 7 |
| DeepSeek V4.1 | DeepSeek V4.1 | 154 | 24 | 7 | 9 |

Luna merges like sol; DeepSeek merges more (85 concepts instead of 102), so more concepts become central. The merging
model matters less than the card model (81-179 concepts by card model, above), but not nothing.

**All open (cards, inventory and generation by DeepSeek V4.1):** from the DeepSeek/DeepSeek inventory (154 concepts,
24 central), DeepSeek generated in the round 7 copy (78 s, 14 calls, free): **44 classes (34 planned)**, 19
restrictions, no module errors; the unsatisfiable-class check (DECISIONS 147) traced `Country` to
`DisjointClasses(Region, Country)` and removed it. The plan is small again - the plan-size call did not lift it -,
the known weakness of DeepSeek. Saved with CQnew1: `drafts/round8/wine-8-open.project.json`.

**Tested by gpt-6-sol** (2026-11-09, 17 calls): 6, 5, 6 of 10 in full (**5.7**), CQ4OE 3.0 of 5 (the gold standard's
score), consistent also with the sample data - the same as DeepSeek generating from sol's inventory (`dsv41r-a` to
`-c`: 5.0, 5.7, 6.3, mean 5.7). DeepSeek's own cards and inventory cost nothing measurable here; the distance to sol
(8.9) lies in the generation. Missed in all three tests, as by every DeepSeek ontology: good vintages, the best wine
for grilled meat, the change of bouquet or body with the vintage.

### Generation from the Opus and the Sonnet inventory (15:35-15:57 CET)

**Setup.** Does a larger inventory give a better ontology? gpt-6-sol generates from the inventory of the Opus cards
and from that of the Sonnet cards, in the round 7 copy with only the cards and the inventory replaced (use case, CQs,
key notions, core relations, vocabularies and data file unchanged), then CQnew1 and Evaluate 3x by gpt-6-sol. The
definition decisions apply where the concept key matches: round 7 had all 3 conflicts decided, the new inventories
1 of 12 (Opus) and 0 of 7 (Sonnet). Projects: `drafts/round8/wine-8-inv-{opus,sonnet}.project.json`.

| Run | Inventory from the cards of | Classes (planned) | Restr. | Individuals | Reasoner: alone / with data | CQs in full, 3 tests (mean of 10) | CQ4OE 5 in full |
|---|---|---|---|---|---|---|---|
| 8-inv-opus | Opus (174 concepts, 30 central) | **101** (84) | 29 | 68 | ok / ok | 9, 9, 9 (9.0) | **5.0** |
| 8-inv-sonnet | Sonnet (90, 20) | 85 (76) | 29 | 13 | ok / ok | 9, 8, 9 (8.7) | 4.7 |
| 7a-7c-sol (round 7) | Luna (82, 12) | 67-76 (58-67) | 10-20 | - | ok / ok | 9.3 / 9.7 / 7.7 (8.9) | 4.2 |

Sol calls: 14 per generation (round 7: 10-11; more central concepts to place), 12 and 16 for the tests (the Sonnet
test took 18 minutes). With the cards, inventories and Claude tests: 77 sol calls on 2026-11-06.

1. **A larger inventory gives a larger ontology, not a worse one; the CQ scores stay the same** within the noise
   (8.7-9.0 against 8.9). The questions need mostly the core concepts, which every inventory has (finding 2 above),
   so the CQ test cannot show what the extra breadth is worth: that needs hold-out questions or the expert review.
2. **The plan copes with 174 concepts:** 84 planned classes; left out with reasons were the paper's method (WineGraph
   concepts), generic ontology vocabulary (slot, facet, knowledge base) and detail outside the use case (wine glass,
   corkscrew, sommelier). No module errors, consistent also with the sample data.
3. **8-inv-opus is the first run that answers all five CQ4OE questions in all three tests**, including the change
   with vintage and "Is Bordeaux red or white" - one run, so a hint.
4. **Observation:** 8-inv-sonnet has two classes `PairingGraph` and `PairingGraphNode` the plan did not exclude,
   while it excluded `wine graph` and `flavor graph` as a paper's method. Whether they carry over WineGraph's method or
   model a recorded graph of pairings is a judgement; no check of the tool works on names (DECISIONS 140 is a rule of
   the planning prompt).
5. The undecided definition conflicts had no visible effect (no module errors, no reasoner problems).

## Claude Sonnet 5.5 and Opus 5.5, tested by gpt-6-sol - 2026-11-06, 14:56-15:07 CET, code b1eca0d

**Setup.** As round 7: each run starts from the same copy of the project before its generation
(`drafts/round7/wine-7-luna-2.project.json`), generated with `claude-sonnet-5-5` or `claude-opus-5-5` (Anthropic API,
key from the server variable `LITMO_ANTHROPIC_KEY`, DECISIONS 152), then the CQ4OE question CQnew1 added and
Evaluate 3x with **gpt-6-sol** as the one tester. **One run per model** (budget), so no spread; the code is newer than
round 7's (DECISIONS 147-152; the wine project has no key notion links, so 148/150 do not apply).
Projects: `drafts/round8/wine-8-{sonnet,opus}-a.project.json`.

| Run | Classes (planned) | Restr. | Reasoner: alone / with data | CQs in full, 3 tests (mean of 10) | CQ4OE 5 in full | Tokens in / out | Cost |
|---|---|---|---|---|---|---|---|
| 8-opus-a | **84** (77) | **27** | ok / ok | 10, 10, 9 (**9.7**) | **4.7** | 108k / 84k | $2.11 |
| 8-sonnet-a | 64 (56) | 17 | ok / ok | 7, 8, 8 (7.7) | 3.7 | 101k / 56k | $0.76 |
| 7a-7c-sol (round 7) | 67-76 (58-67) | 10-20 | ok / ok | 9.3 / 9.7 / 7.7 (8.9) | 4.2 | - | - |
| Gold standard `sub_wine` | - | - | ok | - | 3.0 | - | - |

Both generations took 11 calls (Sonnet 4 minutes, Opus 8); the sol tests 5-6 calls each (round 7: 8-9), since fewer
queries needed a correction.

### Findings

1. **Opus 5.5 is at the level of sol's best run** (7b: 9.7 of 10, 4.7 of 5): the largest plan of any model (77 of
   about 82 concepts; sol 58-67), the most class restrictions (27; sol 10-20), consistent also with the sample data.
   It is the only run that answers "the best choice of wine for grilled meat" in all three tests (`CookingMethod`,
   `Richness`, `FoodWeight`, `CustomerPreference`, `WineRecommendation`) and "Is Bordeaux red or white" in all three.
2. **Sonnet 5.5 is at the level of sol's weakest run** (7c: 7.7 of 10, 3.7 of 5): grilled meat only partly (no
   cooking method), the vintage change only partly (body, but not the bouquet), Bordeaux once partly (a region).
3. **Both keep the method fix** (DECISIONS 140): the same seven WineGraph concepts excluded as a paper's method, no
   graph or vector class; both keep the pairing rules and strategies.
4. **Cost:** a wine generation is $0.76 with Sonnet and $2.11 with Opus (output tokens dominate: Opus wrote 50 % more).
   One run each - differences of about 1.5 points between configurations are not reliable (Luna comparison above).

## gpt-6-luna as tester - 2026-11-05, 16:24-17:12 CET, code adb50ce (no generation)

**Setup.** Can the cheaper gpt-6-luna (500 calls a day on KI:connect) replace gpt-6-sol (100) as the one tester of
the paper? Evaluate 3x with Luna on copies of ten ontologies sol has already tested: seven wine ontologies of round 7
(7a-7c-sol, 7-luna, 7-oss-a, 7-dsv41-b, 7-gemma-a) and VA 7a-7c (recorded in `examples/va/RUNS.md`). Evaluate 3x
writes new sample data and queries in every test, so Luna's tests are independent of sol's. The projects themselves
were not changed. 96 Luna calls: 6-9 per wine ontology, 12-13 per VA ontology; 3-4 minutes per wine ontology, 7-9
per VA ontology.

| Ontology | CQs in full, 3 tests: sol | Luna | Mean sol / Luna (of 10) |
|---|---|---|---|
| 7a-sol | 9, 9, 10 | 8, 8, 7 | 9.3 / 7.7 |
| 7b-sol | 10, 10, 9 | 9, 8, 8 | 9.7 / 8.3 |
| 7c-sol | 7, 8, 8 | 4, 6, 6 | 7.7 / 5.3 |
| 7-luna | 6, 5, 6 | 7, 5, 7 | 5.7 / **6.3** |
| 7-oss-a | 6, 5, 4 | 3, 2, 4 | 5.0 / 3.0 |
| 7-dsv41-b | 6, 6, 6 | 4, 6, 6 | 6.0 / 5.3 |
| 7-gemma-a | 6, 6, 6 | 4, 6, 4 | 6.0 / 4.7 |
| VA 7a | 9, 9, 9 | 7, 8, 8 | 9.0 / 7.7 |
| VA 7b | 10, 10, 9 | 6, 5, 5 | 9.7 / **5.3** |
| VA 7c | 8, 9, 8 | 6, 7, 8 | 8.3 / 7.0 |
| **Mean** | | | **7.6 / 6.1** |

### Findings

1. **Luna is stricter, in the same direction almost everywhere:** 1.6 fewer questions in full of 10 on average. Of
   130 questions (both testers, same ontology), 102 differ by at most one of three tests; where they differ by two or
   more, Luna is lower 24 times and higher 4 times. It mostly moves "full" to "partial", seldom to "none". Its
   reasons are mostly sound - "the best choice" with no ranking in the ontology, "my preferences" with no customer
   preferences modelled, "Is Bordeaux red or white" with Bordeaux a region - where sol counted these as full.
   Which tester is closer to an expert is open.
2. **The order of the ontologies mostly holds:** 32 of 39 pairs in the same order. The distance between the
   sol-generated and the open-model ontologies stays about the same (3.2 points under sol, 2.8 under Luna).
3. **Close results can flip:** VA 7b is the best of the three VA runs under sol (9.7) and the worst under Luna (5.3);
   Luna finds several of its relations recorded side by side but not linked. Differences of about 1.5 points between
   configurations are not reliable with either tester.
4. **Possibly a slight preference for its own ontology:** 7-luna is the only one Luna scores higher than sol (6.3
   against 5.7) - one ontology, so only a hint.

### Second set: five more ontologies (2026-11-06, 17:10-17:32 CET, code b1eca0d)

The five ontologies sol tested on 2026-11-06 (Claude runs, generations from the Opus and Sonnet inventories,
DeepSeek `dsv41r-c`), tested by Luna the same way; 43 Luna calls (4-13 per ontology, 2.5-9 minutes each).

| Ontology | CQs in full, 3 tests: sol | Luna | Mean sol / Luna (of 10) |
|---|---|---|---|
| 8-opus-a | 10, 10, 9 | 7, 10, 10 | 9.7 / 9.0 |
| 8-sonnet-a | 7, 8, 8 | 8, 8, 7 | 7.7 / 7.7 |
| 8-inv-opus | 9, 9, 9 | 8, 8, 9 | 9.0 / 8.3 |
| 8-inv-sonnet | 9, 8, 9 | 8, 9, 7 | 8.7 / 8.0 |
| 7-dsv41r-c | 7, 7, 5 | 7, 6, 7 | 6.3 / **6.7** |
| **Mean of these five** | | | **8.3 / 7.9** |
| **Mean of all 15** | | | **7.8 / 6.7** |

- **This time Luna was hardly stricter** (0.3 points against 1.6 in the first set): of 50 questions, 7 differ by two
  or more tests, Luna 3 times lower and 4 times higher - no direction (first set: 24 lower, 4 higher). Why is open:
  these ontologies are better and give less to object to, or Luna varies between days; neither the test code nor
  the prompts changed in between.
- **The order holds as before:** over all 15 ontologies, 76 of 92 pairs in the same order (83 %; first set 82 %).
- The gap between the testers varies from 0 to 4.3 points per ontology, so scores of the two are never mixed.

### Consequences

- Numbers of different testers are never compared; every comparison names its tester.
- For the paper: Luna as the one tester for all runs would allow many more runs; sol as a check on a few. The choice
  is an open decision in `PAPER.md`.

## Round 7 - 2026-11-03/04: the method fix, sol, seven models, and the gold standard re-tested (DECISIONS 140-146)

**Setup.** Every run starts from a copy of the v0.2 walkthrough project as it was before its generation (built from
the tool's own export; `drafts/round7/`): the same inventory (82 concepts, 12 central), use case, 9 competency
questions, decided definitions, key notions, vocabularies (PROV-O, SKOS, Schema.org, FoodOn), data file and the 21
approved core relations; everything a generation, evaluation or repair wrote removed. Generate, then add the CQ4OE
question the generation never saw ("What grapes are used to make Bordeaux wine?", CQnew1), then Evaluate 3x. No repair.
No hold-out set (the step-5 suggestions had seen all 37 literature questions, as in the walkthrough). **Each model
tested its own ontology** - so the numbers of different models are not directly comparable (see the findings).

| Run (code) | Model | Classes (planned) | Restr. | Reasoner: alone / with data | CQs in full, 3 tests (mean of 10) | CQ4OE 5 in full |
|---|---|---|---|---|---|---|
| 7-luna (8065a98) | gpt-6-luna; tested by gpt-6-sol | 41 (35) | 8 | ok / ok | 6, 5, 6 (5.7) | 2.3 |
| 7-luna-2 (8065a98 + 140 corrected) | gpt-6-luna | 82 (74) | 6 | `Vintage` unsatisfiable / inconsistent | 6, 7, 3 (5.3) | 2.3 |
| 7a-sol (bf77b45) | gpt-6-sol | 68 (58) | 17 | ok / ok | 9, 9, 10 (9.3) | 4.3 |
| 7b-sol | gpt-6-sol | 76 (67) | 10 | ok / ok | 10, 10, 9 (9.7) | 4.7 |
| 7c-sol | gpt-6-sol | 67 (59) | 20 | ok / ok | 7, 8, 8 (7.7) | 3.7 |
| 7-mistral-a (43a4b59) | mistral-small-4-119b | 56 (39) | 11 | inconsistent / inconsistent | 3, 1, 2 (2.0) | 2.0 |
| 7-mistral-b | mistral-small-4-119b | 38 (28) | 9 | 1 unsatisfiable / - | test failed (invalid JSON) | - |
| 7-mistral-c | mistral-small-4-119b | 38 (23) | 9 | inconsistent / inconsistent | 2, 3, 2 (2.3) | 2.0 |
| 7-qwen-a (43a4b59 + 144) | qwen3.8-27b, thinking off | 37 (19) | 7 | ok / ok | 5, 4, 2 (3.7) | 3.3 |
| 7-qwen-b | qwen3.8-27b, thinking off | 45 (38) | 3 | 1 unsatisfiable / inconsistent | 6, 7, 3 (5.3) | 3.3 |
| 7-qwen-c | qwen3.8-27b, thinking off | 28 (20) | 7 | ok / ok | 0, 5, 5 (3.3) | 2.0 |
| 7-gemma-a (ff5dcf4) | gemma-4-31b-it (Open WebUI) | 34 (25) | 6 | `Meal` unsatisfiable / same | 8, 6, 6 (6.7) | 3.7 |
| 7-gemma-b | gemma-4-31b-it | 35 (23) | 4 | `Meal` unsatisfiable / same | 6, 6, 4 (5.3) | 3.0 |
| 7-gemma-c | gemma-4-31b-it | 39 (26) | 5 | `Meal` unsatisfiable / same | 5, 2, 5 (4.0) | 2.7 |
| 7-dsv41-a (ff5dcf4 + 145) | DeepSeek-V4.1-Flash (FhGenie), thinking off | 67 (46) | 22 | not checked: `DisjointClasses(RedWine, RedWine)` | 2, 1, 6 (3.0) | 1.7 |
| 7-dsv41-b | DeepSeek-V4.1-Flash, thinking off | 67 (60) | 12 | 4 unsatisfiable / inconsistent | 4, 1, 3 (2.7) | 1.7 |
| 7-dsv41-c | DeepSeek-V4.1-Flash, thinking off | 39 (31) | 16 | `Country` unsatisfiable / inconsistent | 5, 3, 3 (3.7) | 2.0 |
| 7-oss-a (ce02a1c) | gpt-oss-120b (KI:connect) | 43 (37) | 12 | ok / ok | 5, 8, 5 (6.0) | 3.0 |
| 7-oss-b | gpt-oss-120b | 41 (34) | 9 | ok / ok | 5, 5 - third test invalid JSON (5.0) | 2.0 |
| 7-oss-c | gpt-oss-120b | 38 (30) | 7 | ok / inconsistent | 3, 5, 4 (4.0) | 2.3 |

Failed attempts, not in the table: qwen3.8-27b with thinking (two generations, the plan call ran past the client's 10
minutes three times each); deepseek-v4-flash on Open WebUI (three generations) and DeepSeek-V4.1-Flash on FhGenie with
thinking (three generations): the plan call spent all 32,000 output tokens thinking (129,000 characters, no answer).
Model calls per run: 10-11 for the generation, 7-10 for Evaluate 3x, whatever the model.

**The gold standard, re-tested.** The walkthrough's comparison (below) used a copy of `sub_wine` that had lost its
class definitions (imported before the server ran DECISIONS 138: `Bordeaux`, `RedWine`, `Zinfandel` without
superclass, 12 root classes), and the CQ test dropped all sample data about the 21 individuals typed only as
`owl:Thing` (fixed in DECISIONS 143). Re-imported with the current code (6 superclasses from definitions, 6 root
classes) and tested with the same five questions:

| Question (CQ4OE id) | Gold standard, Luna | Gold standard, sol | 7a / 7b / 7c-sol |
|---|---|---|---|
| Which wine characteristics should I consider when choosing a wine? (CQ1) | 3 of 3 | 3 of 3 | 3 / 3 / 3 |
| Is Bordeaux a red or white wine? (CQ2) | 3 of 3 | 3 of 3 | 1 / 2 / 2 |
| Does a bouquet or body of a specific wine change with vintage year? (CQ6) | 0 | 0 (partly) | 3 / 3 / 3 |
| What were good vintages for Napa Zinfandel? (CQ7) | 0 | 0 (partly) | 3 / 3 / 0 |
| What grapes are used to make Bordeaux wine? (CQnew1) | 3 of 3 | 3 of 3 | 3 / 3 / 3 |
| **Mean in full per run** | **3.0 of 5** | **3.0 of 5** | **4.3 / 4.7 / 3.7 (4.2)** |

**One tester for all: three open-model ontologies tested by gpt-6-sol** (2026-11-04, 23:05-23:12 CET, code 4f40ff7;
8 calls each, all three tests complete). One ontology per open model, chosen before the test: DeepSeek V4.1 b (the
largest), gpt-oss a and Gemma a (the best self-tests).

| Ontology | CQs in full, 3 tests (sol) | Mean of 10 | Its own test | CQ4OE 5 in full | Reasoner |
|---|---|---|---|---|---|
| 7a-7c-sol | 9, 9, 10 / 10, 10, 9 / 7, 8, 8 | 8.9 | - | 4.2 | ok |
| 7-dsv41-b | 6, 6, 6 | 6.0 | 2.7 | 3.3 | `WhiteWine`, `RoseWine` unsatisfiable |
| 7-gemma-a | 6, 6, 6 | 6.0 | 6.7 | 2.3 | `Meal` unsatisfiable |
| 7-oss-a | 6, 5, 4 | 5.0 | 6.0 | 2.3 | ok |
| Gold standard `sub_wine` | - | - | - | 3.0 | ok |

What the open models miss most under sol: the best wine for grilled meat (0 of 9 tests), good vintages for Napa
Zinfandel (0 of 9), the vintage change (DeepSeek 2 of 3, gpt-oss 1, Gemma 0) - the questions the sol generations
answer with vintage assessments and pairing results. Gemma and gpt-oss tested themselves a little too generously,
DeepSeek much too harshly (invalid Turtle and wrongly typed sample data in its own tests).

**Reruns with DeepSeek V4.1 after DECISIONS 147** (2026-11-05, FhGenie, thinking off; each tested by itself).
`dsv41p` on 1356492 (plan-size call and unsatisfiable-class check), 11:01-11:12 CET; `dsv41r` on 409fa51 (also
inconsistent ontologies traced to their unsatisfiable classes), 11:18-11:27 CET.

| Run | Plan -> after the plan-size call | Classes | Restr. | Unsatisfiable classes (check) | Reasoner: alone / with data | CQs in full (mean) |
|---|---|---|---|---|---|---|
| 7-dsv41p-a | 47 -> 47 (25 placed in existing classes or as properties/individuals) | 58 | 24 | ontology inconsistent - not traced yet | inconsistent / inconsistent | 2, 3, 2 (2.3) |
| 7-dsv41p-b | **13 -> 74** (61 new classes) | 80 | 14 | ontology inconsistent - not traced yet | inconsistent / inconsistent | 6, 0, 1 (2.3) |
| 7-dsv41p-c | 72, no call | 79 | 22 | none | ok / inconsistent | 5, 4, 5 (4.7) |
| 7-dsv41r-a | 33 -> 40 (10 placed, 7 new classes) | 50 | 21 | `Grape`: DisjointClasses(Grape, GrapeVariety) removed, consistent again | ok / ok | 3, 1, 4 (2.7) |
| 7-dsv41r-b | 52, no call | 58 | 11 | none | ok / ok | 3, 1, 5 (3.0) |
| 7-dsv41r-c | 59, no call | 76 | 12 | none | ok / ok | 4, 5, 2 (3.7) |

In `dsv41p-a` and `-b`, DeepSeek had written individuals of unsatisfiable classes (`Country`, `Meal`; `WineRegion`,
`WineGrape`), which makes the whole ontology inconsistent - hence the addition to DECISIONS 147. Applied afterwards
to the stored ontologies, the check removed three disjointness axioms between a class and its own superclass, and
both became consistent (`Meal` stays unsatisfiable). The three `dsv41r` ontologies are the first DeepSeek ontologies
that are consistent also with the sample data. `dsv41r-a` has two method classes again (`HeterogeneousNetwork`,
`FlavorGraph`): the plan-size call offered the plan's own exclusions once more, and the model placed them. The plan
size of one model varies widely (13 to 72 planned classes over six runs); the call lifts the smallest plans but does
not even them out. The self-tests stay unreliable.

**Sol test of `dsv41r-c`** (2026-11-06, 16:12-16:15 CET, code b1eca0d; 8 calls; project
`drafts/round8/wine-7-dsv41r-c-soltest.project.json`): 7, 7, 5 of 10 in full (mean **6.3**; its own test 4, 5, 2),
CQ4OE 3.0 of 5 (the gold standard's score), consistent also with the sample data - the best DeepSeek ontology under
sol so far (`dsv41-b` 6.0), sol's own generations 8.9. Missed in all three tests: good vintages for Napa Zinfandel (no
notion of a good vintage), the change of bouquet or body with the vintage, and rich, fatty, salty dishes (taste
attributes only as numbers).

**Sol test of `dsv41r-b`** (2026-11-09; 6 calls): 6, 6, 5 of 10 in full (**5.7**), CQ4OE 2.7 of 5, consistent also
with the sample data. With `-a` and `-c`: DeepSeek V4.1 reaches 5.0 / 5.7 / 6.3 under sol (mean 5.7).

**Sol test of `dsv41r-a`** (2026-11-06, 17:10-17:12 CET; 7 calls; `drafts/round8/wine-7-dsv41r-a-soltest.project.json`):
6, 4, 5 of 10 in full (mean **5.0**; its own test 3, 1, 4), CQ4OE 2.7 of 5, consistent also with the sample data.
Smaller than `-c` (50 classes against 76) and missing the same questions (good vintages, rich and fatty dishes, the
best wine for grilled meat). With the current code, DeepSeek V4.1 reaches 5.0 and 6.3 under sol; sol's own
generations 8.9.

### Findings

1. **The method fix holds** (DECISIONS 140): no graph, vector or similarity class in any of the 20 ontologies; the
   walkthrough had six. The first version excluded every WineGraph concept, also its elimination and pairing rules,
   and planned 35 instead of 60 classes (7-luna); judging each concept, not the paper, brought the rules back
   (`PairingRule`, `EliminationRule` in all sol runs).
2. **Changes over time are modelled with sol** (DECISIONS 141): "Does the body of a wine change with vintage year?"
   is answered in full in all nine sol tests (7c even with a class `VintageSensoryChange`); Luna 1 of 3, the
   walkthrough 0.
3. **Class restrictions depend on the model, not on the small modules:** sol wrote 10-20 per run, Luna 6-8 on the same
   input - the question the walkthrough left open.
4. **With the same tester, the sol generations answer more of the benchmark's questions than the gold standard**
   (4.2 against 3.0 of 5): the gold standard has no link from a wine to its vintage and no notion of a good vintage;
   it answers "Bordeaux red or white" through `RedBordeaux` and `WhiteBordeaux`, where the generated ontologies
   model Bordeaux as a region. Limits: five questions, a 26-term excerpt, hasValue restrictions and enumerations
   not read by the import.
5. **All open models plan far too small:** 19-60 planned classes for a target of about 82 (Luna 74, sol 58-67), and
   their ontologies have 28-67 classes. What they leave out is mostly the tasting descriptors and the food
   characteristics (up to 68 of the 82 concepts excluded in one run, Qwen c; sol 6-8).
6. **Logical errors are more frequent with the open models:** Mistral two inconsistent ontologies of three;
   DeepSeek V4.1 an invalid axiom and unsatisfiable classes (DECISIONS 146); Gemma `Meal` unsatisfiable in all three
   runs. Luna-2's `Vintage` (below Process and, by an axiom, InformationObject) led to DECISIONS 142.
7. **Thinking models need the thinking switched off or limited** (DECISIONS 144): Qwen and DeepSeek fail at the plan
   call otherwise; gpt-oss-120b thinks moderately (about 4,700 tokens) and answers. **FhGenie caches identical
   requests** (DECISIONS 145): without a new `user` per call the three generations and the three tests would have
   been copies.
8. **Self-tests mix the tester's errors into the score**, in both directions: with gpt-6-sol as the tester DeepSeek
   V4.1 rose from 2.7 to 6.0 of 10, Gemma fell from 6.7 to 6.0 and gpt-oss from 6.0 to 5.0. A comparison of
   generators needs one tester (gpt-6-sol), as planned for the paper (PAPER.md).
9. **With one tester, the open models reach about two thirds of sol** (5.0-6.0 against 8.9 of 10). DeepSeek V4.1
   Flash comes closest on the benchmark (3.3 of 5, the gold standard 3.0), has the largest ontologies and as many
   restrictions as sol, and runs on premise (FhGenie): chosen as the open model of the evaluation (PAPER.md).

10. **The checks of DECISIONS 147 work, the plan size stays variable:** the plan-size call lifted a plan of 13
   classes to 74; the unsatisfiable-class check traced every case to one axiom and made all three `dsv41r` ontologies
   consistent. A plan of 33 grew only to 40 (the model placed most concepts in existing classes), and the call can
   bring a paper's method back (`dsv41r-a`).

### Follow-ups (proposed)

- ~~The open models' small plans~~ and ~~unsatisfiable classes~~: built in DECISIONS 147.
- ~~Sol tests of `dsv41r-a` to `-c`~~: 5.0, 5.7 and 6.3 of 10 (mean 5.7; 2026-11-06/09).
- The plan-size call should not place what the plan excluded as a paper's method: offer only the plan's other
  exclusions again, or keep the method reason.
- `Meal` unsatisfiable in all Gemma runs: find the axiom (probably a disjointness with a FoodOn link).

## v0.2 walkthrough - 2026-11-02, gpt-6-luna, commits 84c82a0-15ad3b2 (all steps; comparison with the CQ4OE gold standard)

A new wine project through all ten steps, as the functional check before recording v0.2 (the walkthrough checklist and
the sources were kept outside the repository, in `drafts/wine-walkthrough/`). Unlike runs 1-14 it has **literature**:
Noy & McGuinness, *Ontology Development 101* (2001); the W3C *OWL Web Ontology Language Guide* (2004); *WineGraph: A
Graph Representation For Food-Wine Pairing* (arXiv 2407.00107, 2024); the Wikipedia articles *Wine and food pairing*
and *Wine tasting descriptors*. The W3C wine ontology was deliberately **not** a source and not a loaded vocabulary: it
is the reference. Data file: a wine list of 15 wines (illustrative values). Fixes found on the way: DECISIONS 137 and
138.

**Project:** inventory of 82 concepts (12 central, 6 themes, 3 conflicting definitions, 37 literature questions); 3
definitions decided; 9 competency questions (the 7 of Noy & McGuinness and 2 from "Suggest questions"); key notions
Wine, Dish, Region, Grape, FoodWinePairing; 21 core relations. Generation: 5 modules, 60 planned classes -> 68 classes,
no module error, no placeholder, all 12 central concepts placed, 5 class restrictions, reasoner consistent. No hold-out
questions: the suggestions had seen all 37 literature questions (DECISIONS 137). Step 9: consolidation of properties,
one refinement (Merlot as a grape variety), further edits up to iteration 5; your questions in full went from 2 (iteration 1) to 6 of 9
(iteration 3), shown in the new comparison table. Export and re-import gave an identical copy. 43 calls for steps 1-10.

### Comparison with a reference

**The W3C wine ontology** (`wine.rdf`, 74 classes) is not a fair reference: it was built as an OWL tutorial example,
the pairing lives in `food.rdf` (expressed with hasValue restrictions the tool cannot read yet), and two of the
project's sources were written by its authors. Loaded before DECISIONS 138, it lost its class definitions (62 of 74
classes as roots) and answered 1 of 9 questions.

**The CQ4OE gold standard** (github.com/oeg-upm/cq4oe-benchmark, Apache-2.0) was built for these questions:
`sub_wine.owl`, a 26-term excerpt of the W3C wine ontology, with 68 axioms annotated by the question they answer. Its
authors dropped the three dish questions (no food model) and added "What grapes are used to make Bordeaux wine?".
Imported with DECISIONS 138: 17 classes, 9 properties, 71 individuals, hierarchy intact; not read: 6 hasValue
restrictions, 8 enumerations, 1 union. Both projects were tested on its five questions with Evaluate 3x (Luna):

| Question (CQ4OE id) | Generated | Gold standard |
|---|---|---|
| Which wine characteristics should I consider when choosing a wine? (CQ1) | 2 of 3 in full | 3 of 3 |
| Is Bordeaux a red or white wine? (CQ2) | 0 (partly, not, partly) | 0 (not answered) |
| Does a bouquet or body of a specific wine change with vintage year? (CQ6) | 0 | 0 |
| What were good vintages for Napa Zinfandel? (CQ7) | 1 of 3 | 0 |
| What grapes are used to make Bordeaux wine? (CQnew1; not among the generation's questions) | 3 of 3 | 2 of 3 |
| **Mean in full per run** | **2.0 of 5** | **1.7 of 5** |

Neither models whether a vintage was "good" or how a wine's body changes across vintages. The gold standard's answer
to "Bordeaux red or white" (both, through RedBordeaux and WhiteBordeaux) is in its class hierarchy; the SPARQL test
queries asserted triples only and does not reason over subclasses.

**Terms:** of the gold standard's 26 terms (matched by hand), 15 are in the generated ontology (Wine, WineDescriptor,
WineColor, Region, Body, SugarLevel, Taste, WineVintage, WineVintageYear, Grape, wineColor, locatedIn, madeFrom,
hasVintage, vintageYear), 7 in another form (RedWine and WhiteWine as individuals of WineType; Zinfandel as a grape
variety, not a wine; body and sugar as text values; a flavour descriptor class; the descriptor relation only as the
general hasQuality), 4 are missing (Bordeaux, RedBordeaux, WhiteBordeaux, a flavour property of wines).

**Reading:** the two follow different modelling styles - the gold standard classifies wines (Bordeaux, red Bordeaux,
Zinfandel as a wine), the generated ontology describes them by characteristics, with grapes and wine types as values -
and on the benchmark's own questions they come out about equal. Limits: one generation with Luna, three test runs; the
gold standard was evaluated through the tool's import and SPARQL test; two sources describe the W3C ontology. For the
paper, a comparison with sol and several generations, and against the nine models CQ4OE reports, would be the fair
version.

**Correction (2026-11-04):** the gold standard's 1.7 of 5 is not valid. The project had been imported before the
server ran DECISIONS 138, so its class definitions were lost after all (no superclass for `Bordeaux`, `RedWine`,
`Zinfandel`; "hierarchy intact" above is wrong), and the CQ test dropped the sample data about its 21 individuals
typed only as `owl:Thing` (DECISIONS 143). Re-imported and re-tested in round 7: 3.0 of 5 with Luna and with sol.

### Found and not yet fixed

- A paper's own method leaks into the ontology: from WineGraph, `Graph`, `GraphNode`, `GraphLink`, `FlavorGraph`,
  `AromaVector` became classes of a wine shop's ontology (DECISIONS 138; fixed in DECISIONS 140, round 7).
- Import: hasValue restrictions and enumerations are reported but not read (DECISIONS 138).
- `Winery` outside the upper layer (6 root classes).

## Run 14 - 2026-10-30, gpt-6-luna, commit 2e25b08 (DECISIONS 103-125 on the second domain; Evaluate 3x)

A copy of run 13's project (same inputs, core relations and `vin` vocabulary), generated with everything since: the
review fixes, the steps after the modules, class restrictions and "Evaluate 3x". The project has no literature, so the
plan completion (3e) and the hierarchy from the literature (3d, 111) do not run - as intended. 14 model calls in all
(generation 6, CQ tests 2, Evaluate 3x 6).

**Generation report:** 2 modules, 15 planned classes -> 18 classes (3 upper) and 15 properties; no module error, no
placeholder, no invalid axiom; **vocabulary links: 6 candidates, 4 linked as equivalent** (`Wine = vin:Wine`,
`WineColor = vin:WineColor`, `Body = vin:WineBody`, `Region = vin:Region`), 2 declined with a reason
(`VintageQuality`, `WineCharacteristic`); core relations after the modules: 2 module relations offered, both kept
with a reason; **no class restrictions written** (the VA modules wrote 85 in run 5a with gpt-6-sol).

| | Run 13 | Run 14 |
|---|---|---|
| Planned classes / classes / object / datatype properties / individuals | 10 / 13 / 7 (5 core) / 1 / 10 | 15 / 18 / 7 (5 core) / 8 / 10 |
| Links: same meaning / a kind of | 4 / 1 (`Region -> vin:Region`) | 4 / 0 (`Region = vin:Region`) |
| Relations / top-level / inverse pairs | 6 / 6 / 1 | 6 / 6 / 1 (the core relation `suitableFor`) |
| Root classes, hierarchy depth | 3 (upper); max 3, mean 2.15 | 3 (upper); max 3, mean 2.33 |
| Class restrictions | - | 0 (1 pair offered to the repair tool) |
| Competency questions full / partial / none | 3 / 4 / 0 (one run; really 4 / 3 / 0) | **4 / 2 / 1, 4 / 2 / 1, 4 / 3 / 0 - full 4.0 (sd 0)** |
| Reasoner | consistent | consistent, also with the sample data |
| Traceability (basis: competency questions) | 53.8 % untraceable | **27.8 %** untraceable |
| Tokens of the generation (input / output) | 8.9k / 11.4k | 10.6k / 11.9k |

The ontology:
- **PhysicalObject:** `Wine` (Bordeaux, Cabernet Sauvignon, Napa Zinfandel as wines); `Place` > `Country`, `Region`
  (Bordeaux, Napa); `Dish`.
- **Quality:** `WineCharacteristic` > `WineColor` (Red, White), `Bouquet`, `Body`, `Acidity`, `Sweetness`,
  `TanninLevel`, `AlcoholContent` (disjoint); `VintageQuality` (Good) with `vintageQualityYear`.
- **InformationObject:** `DishCategory` (Seafood, GrilledMeat).
- Values per wine as datatype properties (`bouquetValue`, `acidityValue`, `vintageYear` ...).

Competency questions, three independent runs: 1, 2, 3 and 5 full in every run; 4 partial in every run (no ranking of
suitable wines); 6 partial in every run (bouquet and body are values of the wine, not of a vintage); 7 none, none,
partial ("a property linking a wine or its vintage to a VintageQuality is missing").

### Findings

1. **The second domain runs cleanly with everything since run 13**: no error, the steps that need literature are left
   out, the reasoner is consistent with the vocabulary's axioms and the sample data.
2. **Evaluate 3x shows the wine questions are stable**: 4 of 7 full in all three runs, the same questions partial for
   the same reasons. For this small ontology the test is not the noise: the differences between wine runs 8-13
   (3-4 full) are more likely differences of the ontologies. In VA run 5a, by contrast, the team's questions varied by 3 (9, 6, 6) - there the test itself is noisy.
3. **Characteristics twice**: `Bouquet`, `Body`, `Acidity` ... are classes below `WineCharacteristic` *and* datatype
   values of the wine (`bouquetValue` ...); DECISIONS 95 asks for one representation per distinction. The classes
   carry no individuals except the colours, so the values are what the questions use.
4. **A vintage quality without a wine**: `VintageQuality` has a year and a self-relation
   (`hasVintageQualityValue: VintageQuality -> VintageQuality`), but nothing connects it to a wine or region -
   question 7 fails on exactly this. A class restriction would not help; the module misses a relation.
5. **No restrictions with gpt-6-luna**: the small modules wrote none, the VA modules with gpt-6-sol 85. Whether that is
   the model or the domain is open; the repair tool offers one pair here.
6. **`Region = vin:Region` again** (run 13: `Region -> vin:Region`): with only the vocabulary's own class as
   candidate, the link step takes "same meaning" when the names match - in line with DECISIONS 106.

## Run 13 - 2026-10-28, gpt-6-luna, commit b0ad9c7 (careful equivalences, remembered "no link", fewer inverses, DECISIONS 102)

Same project and inputs as run 12, `vin` still loaded ("align"); a development test only, as runs 11 and 12.

**Generation report:** 2 modules, 10 planned classes -> 13 classes (3 upper) and 8 properties; 8 superclasses planned,
all kept; **vocabulary links: 6 classes with candidates, 5 linked** (`Wine = vin:Wine`, `WineBody = vin:WineBody`,
`WineColor = vin:WineColor`, `Vintage = vin:Vintage`, **`Region -> vin:Region`**), **1 declined with a reason**
(`WineBouquet`: "the only candidate, vin:Wine, denotes a wine rather than a bouquet"); core relations: none below them,
2 module relations without one.

| | Run 12 | Run 13 |
|---|---|---|
| Planned classes / classes / object / datatype properties / individuals | 16 / 19 / 21 / 1 / 10 | 10 / 13 / 7 (5 core) / 1 / 10 |
| Links: same meaning / a kind of | 4 / 0 | 4 / 1 (`Region -> vin:Region`) |
| Declined, remembered as align decisions | - (not stored) | 1, with its reason |
| Classes left for "Align" in the evaluation | 6 | 2 |
| Relations / top-level / inverse pairs | 12 / 12 / 8 | **6 / 6 / 1** (only the core relation `suitableFor`) |
| Root classes, hierarchy depth | 3 (upper); max 4 | 3 (upper); max 3, mean 2.15 |
| Competency questions full / partial / none | 4 / 2 / 1 | 3 / 4 / 0 - question 5 a false partial, really 4 / 3 / 0 |
| Reasoner | consistent | consistent, with the vocabulary's axioms, also with the sample data |
| Traceability (basis: competency questions) | 52.6 % untraceable | 53.8 % |
| Tokens (input / output) | 14.5k / 15.6k | 12.8k / 16.4k (plan 1.9k/5.0k, links 0.5k/1.9k, modules 6.5k/4.5k, CQ tests 3.8k/5.0k) |

The ontology:
- **PhysicalObject:** `Wine` (Bordeaux, Cabernet Sauvignon, Napa Zinfandel as wines); `Place` > `Country`, `Region`
  (BordeauxRegion, Napa); `Dish` (Seafood, GrilledMeat).
- **Quality:** `Characteristic` > `WineBouquet`, `WineBody`, `WineColor` (Red, White, Rose).
- **InformationObject:** `Vintage` (`vintageYear`), linked to a wine by `hasVintage` and to qualities by
  `describesQuality` - characteristics per vintage.

Competency questions (fresh sample data, no issue): 1, 2, 3 full; 4 partial (no ranking); 5 partial (the author names
something the question does not ask - a false partial); 6 partial (characteristics per vintage, but no values to
compare); 7 partial (years only).

### Findings

1. **The broader term is now a subclass link**: `Region -> vin:Region` instead of run 12's `WineRegion = vin:Region`.
   The other equivalences are same-named classes with the same meaning (`Wine`, `WineBody`, `WineColor`, `Vintage`).
2. **A declined link is remembered**: `WineBouquet` is stored as an align decision with the link step's reason, the
   evaluation lists it, and "Align with vin" offers 2 classes instead of 6 (classes without candidates at planning).
3. **Inverses: 1 pair instead of 8** - only the core relation's own; the module relations come in one direction,
   which brings the top-level relations from 12 to 6. Questions still find what they need (one direction suffices).
4. **The ontology is lean** (10 planned classes; the Dish module is one class with two dish individuals) and drops the
   grape variety again; question 6 now has a vintage with qualities, but no values to compare.
5. **"Leaves out" over-reports once again** (question 5) - as in runs 8, 10 and 12; the expert review should check the
   partial results too.

### Wine runs: where they stand (3a-3c)

Runs 9-13 cover the upper layer (3b) and reuse (3c) on top of core relations (3a): every top class below the upper
layer, links to a loaded vocabulary decided per planned class, careful equivalences, remembered decisions, inverses only
where needed, about 13-15k input tokens per generation and test. The competency questions stay at about 4 of 7
fully answered; the rest needs modelling decisions the questions ask for (a ranking, a vintage quality, comparable
characteristic values). The remaining phase-3 items (3d hierarchy from the literature, 3e every central concept
planned or excluded) need literature: the VA project.

## Run 12 - 2026-10-28, gpt-6-luna, commit a3f7be0 (vocabulary links after planning, DECISIONS 101)

Same project and inputs as run 11, the W3C wine ontology still loaded (`vin`, "align"). New: the plan no longer sees
the vocabulary; links are decided per planned class after planning. Like run 11 a development test only (the loaded
vocabulary is the domain's reference). The server stopped once before the evaluation (the app closed its preview); the
evaluation was run again afterwards, nothing was lost.

**Generation report:** 2 modules, **16 planned classes** (run 11: 35) -> 19 classes (3 upper) and 22 properties; 15
superclasses planned, all kept; **vocabulary links: 7 planned classes had candidates, 4 linked, all as the same
meaning** (`Wine = vin:Wine`, `WineColor = vin:WineColor`, `Body = vin:WineBody`, `WineRegion = vin:Region`), nothing
dropped by the server; upper layer as in run 10; core relations: none below them, 8 module relations without one.

| | Run 10 | Run 11 | Run 12 |
|---|---|---|---|
| Planned classes / classes / object / datatype properties / individuals | 11 / 14 / 9 / 1 / 10 | 35 / 39 / 15 / 1 / 5 | **16** / 19 / 21 / 1 / 10 |
| Links to the reused vocabulary | 0 (none loaded) | 29 SubClassOf | **4 EquivalentClasses** |
| Classes left for "Align" in the evaluation | - | 7 | 6 |
| Root classes, hierarchy depth | 3 (upper); max 3 | 3; max 5 | 3; max 4, mean 2.32 |
| Relations / top-level | 6 / 6 | 9 / 9 | 12 / 12 (every module relation with an inverse) |
| Competency questions full / partial / none | 3 / 3 / 1 | 3 / 4 / 0 | 4 / 2 / 1 |
| Reasoner | consistent | consistent | consistent, with the vocabulary's axioms, also with the sample data |
| Traceability (basis: competency questions) | 57.1 % untraceable | 61.5 % | 52.6 % |
| Tokens (input / output) | 11.5k / 11.9k | 16.8k / 19.5k | 14.5k / 15.6k (plan 1.9k/5.3k, **links 0.5k/0.9k**, modules 6.6k/6.4k, CQ tests 5.5k/3.0k) |

The ontology:
- **PhysicalObject:** `Wine` (with `vintageYear`, `hasGrapeVariety`, `hasWineStyle`); `GeographicPlace` > `Country`,
  `WineRegion` (BordeauxRegion, Napa); `Dish` > `SeafoodDish`, `MeatDish` > `GrilledMeatDish`; `DishIngredient`.
- **Quality:** `WineCharacteristic` > `WineColor` (Red, White), `Bouquet`, `Body` (disjoint).
- **InformationObject:** `GrapeVariety` (Cabernet Sauvignon, Zinfandel), `WineStyle` (Bordeaux, Napa Zinfandel - with
  colour, region and grape), `WineRecommendation` (a wine recommended for a dish).

Competency questions (fresh sample data, no issue):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full - the kinds, though with the superclasses `Quality` and `WineCharacteristic` among them |
| 2 | Is Bordeaux a red or white wine? | full - through the Bordeaux region's wine style and its colour |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - a wine of the grape variety, suitable for seafood |
| 4 | What is the best choice of wine for grilled meat? | partial - no ranking (a `WineRecommendation` exists, but without a score) |
| 5 | Which characteristics affect appropriateness for a dish? | full on paper - the query asks for characteristics that affect the *wine*, not the dish |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | not answerable |
| 7 | What were good vintages for Napa Zinfandel? | partial - years only |

### Findings

1. **The fix works**: 16 planned classes instead of 35, no copied kinds of wine; the link call costs about 0.5k input
   tokens, and 3 of the 7 classes with candidates were left without a link.
2. **All four links are "same meaning"**, although the rule calls "subclass" the usual case. `Wine = vin:Wine` and
   `WineColor = vin:WineColor` are plausible; `WineRegion = vin:Region` (the W3C Region is any region, not only a wine
   region) and `Body = vin:WineBody` are claims a subclass would make more safely. Equivalence imports every axiom of
   the term into the class - an expert check (stage D) should look at equivalences first.
3. **The link step's "no link" decisions are not remembered**: the evaluation still offers "Align with vin" for 6
   classes, among them the ones the link step had just declined - the align action would ask again.
4. **Inverses for every module relation** (8 pairs) bring the top-level relations to 12 - the open point "fewer
   inverses" (DECISIONS) again.
5. **Question 5 passes on a hollow query** (characteristics that affect the wine) - the limit of the self-statement.

### Follow-ups (proposed)

- Link rule: "equivalent" only if the term's definition says the same as the planned class's note; a term that is
  broader (any region) gives "subclass" (finding 2).
- Record the link step's "no link" decisions as align decisions, so "Align" does not ask again (finding 3).
- Fewer inverses: an inverse only where a question needs both directions (finding 4).

All three built in [DECISIONS 102](../../DECISIONS.md).

## Run 11 - 2026-10-28, gpt-6-luna, commit 6620abd (reuse in planning, PLAN.md phase 3c, DECISIONS 98)

Same project, inputs, key notions, upper layer and core relations as run 10; new: the **W3C wine ontology loaded as a
vocabulary** (`vin`, 74 classes, 13 properties, decision "align"). **A development test of 3c only**: the loaded
vocabulary is the reference the wine domain is compared with (EVALUATION.md, section 5), so this run partly copies the
reference and must not be used in a comparison.

**Generation report:** 2 modules, **35 planned classes** (runs 9 and 10: 10-11) -> 39 classes (3 upper) and 16
properties; 34 superclasses planned, all kept; **28 planned links to `vin:` terms, none dropped**; 29 links to the
vocabulary in the ontology after the merge (one more set by a module); upper layer as in run 10; core relations: none
below them, 5 module relations without one.

| | Run 10 | Run 11 |
|---|---|---|
| Classes / object / datatype properties / individuals | 14 / 9 / 1 / 10 | 39 / 15 / 1 / 5 |
| Links to a reused vocabulary | 0 | **29** (all SubClassOf; 7 more candidates left for "Align") |
| Root classes, hierarchy depth | 3 (upper); max 3 | 3 (upper); **max 5**, mean 2.97 |
| Axioms | 2 | 32 (29 links, 3 disjointness) |
| Competency questions full / partial / none | 3 / 3 / 1 | 3 / 4 / 0 (finding 4) |
| Reasoner | consistent | consistent, with the vocabulary's axioms for the linked terms, also with the sample data |
| Traceability (basis: competency questions) | 57.1 % untraceable | 61.5 % (24 classes, mostly the mirrored wine kinds) |
| Tokens (input / output) | 11.5k / 11.9k | **16.8k / 19.5k** (plan 2.4k/5.7k, modules 7.8k/9.6k, CQ tests 6.7k/4.2k) |

The ontology: `Wine` with 17 subclasses mirroring the W3C wine ontology one by one (`RedWine`, `WhiteWine`, `RoseWine`,
`DryWine`, `SweetWine`, `DessertWine`, `TableWine`, `IceWine`, `FrenchWine` > `AlsatianWine`, `BordeauxWine` >
`RedBordeaux`, `WhiteBordeaux`, `GermanWine`, `ItalianWine`, `AmericanWine` > `CaliforniaWine`, `TexasWine`,
`CabernetSauvignon`, `Zinfandel`), each linked `SubClassOf vin:<same name>`; `WineDescriptor` > `WineColor`,
`WineTaste` > `WineBody`, `WineFlavor` > `WineBouquet`, `WineSugar` (as in the W3C ontology); `WineGrape`;
`VintageYear` with `hasVintageRating` -> `VintageRating` (GoodVintageRating); `Place` > `Country`, `Region` (Bordeaux,
Napa); `Dish`, `DishCategory`.

Competency questions (fresh sample data, no issue):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full - the kinds of descriptor |
| 2 | Is Bordeaux a red or white wine? | partial - the query returns red and white Bordeaux wines; Bordeaux itself is a region here (as in the W3C ontology), which the author reports |
| 3 | Does Cabernet Sauvignon go well with seafood? | full on paper - `ASK { ?wine :suitableForDishCategory :seafood }` drops Cabernet Sauvignon and answers "does any wine go with seafood"; not reported (finding 4) |
| 4 | What is the best choice of wine for grilled meat? | partial - no ranking |
| 5 | Which characteristics affect appropriateness for a dish? | partial - the author again names something the question does not ask |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | partial - characteristics are not tied to a vintage |
| 7 | What were good vintages for Napa Zinfandel? | **full** - `VintageYear` with a `VintageRating`, the first run with a vintage quality |

### Findings

1. **Planned reuse works mechanically**: 28 planned links, all to existing `vin:` classes, none dropped; 29 links in
   the ontology against 0 in run 10 and 2 in the VA run of DECISIONS 77; the reasoner accepts them with the
   vocabulary's axioms.
2. **But the plan mirrored the vocabulary**: 35 planned classes instead of 10-11, most of them same-named copies of
   `vin:` classes the use case does not ask for (`IceWine`, `TexasWine`, `AlsatianWine`, `GermanWine` ...). The term
   list in the plan prompt acted as a class catalogue. Two causes: (a) the rule says how to link a planned class, but
   not that the listed terms are candidates for links rather than classes to plan; (b) the selection is generous - the
   key notion "Wine" matches every two-word term ending in "wine" by word overlap (Jaccard 0.5), so the 40 offered
   terms were mostly kinds of wine. The output grew accordingly (+64 % output tokens).
3. **A same-named copy is linked as SubClassOf** - for `RedWine` and `vin:RedWine` the meaning is the same; with only
   SubClassOf available, the plan cannot say so (EquivalentClasses), and a team that wanted the vocabulary's classes
   themselves would choose "use terms directly".
4. **Question 3 answers an easier question without saying so** (any wine with seafood) - the limit of the
   self-statement (DECISIONS 91); question 5 again over-reports. With the mirrored hierarchy, Bordeaux became a region
   and question 2 partial for a reason the model states correctly.
5. **Vintage quality modelled for the first time** (`VintageRating`), so question 7 is answered - borrowed from the
   W3C ontology's structure rather than planned for the question.

### Follow-ups (proposed)

- Plan rule: the listed terms are candidates for links, not a list of classes; plan a class only where the use case,
  the questions, the key notions or the data need it (finding 2a).
- Selection: offer the plan terms that match a key notion, a question or an inventory concept closely (same name or
  label, or the head word), not on a single shared word (finding 2b) - or link after planning: candidates per planned
  class, as the align action does (the original wording of PLAN.md 3c).
- Allow `EquivalentClasses` for a link where the planned class and the term mean the same (finding 3).

## Run 10 - 2026-10-28, gpt-6-luna, commit b4bc1b5 (new core relations with upper classes)

Same project, inputs, key notions and upper layer as run 9; the core relations were proposed again, now with the
upper classes available as domain and range, and approved unchanged.

**The vocabulary** (nothing dropped; labels with the proposal):

| Relation | Domain -> range | Inverse | Covers |
|---|---|---|---|
| `hasQuality` | Wine -> **Quality** | - | CQ1, CQ2 |
| `originatesIn` | Wine -> **PhysicalObject** | - | CQ7 |
| `suitableFor` | Wine -> Dish | `hasSuitableWine` | CQ3, CQ4 |
| `affects` | any -> any | - | CQ5 |

**Generation report:** 2 modules, 11 planned classes -> 14 classes (3 upper) and 10 properties; 10 superclasses
planned, all kept; upper layer: PhysicalObject, InformationObject, Quality used, Process, Agent, Specification
removed, no top class outside; core relations: none below them, 2 module relations without one (`hasGrapeVariety`,
`hasDishCategory`), no violation.

| | Run 9 | Run 10 |
|---|---|---|
| Classes / object / datatype properties / individuals | 13 / 9 / 1 / 8 | 14 / 9 (5 core) / 1 / 10 |
| Root classes, hierarchy depth | 3 (upper); max 3, mean 2.15 | 3 (upper); max 3, mean 2.14 |
| Relations / top-level / below a core relation | 6 / 6 / 0 | 6 / 6 / 0 |
| Narrow property beside a core relation | 1 (`wineCharacteristicAffectsSuitabilityForCategory`) | **none** |
| Unconnected classes / second inverses | 0 / 0 | 0 / 0 |
| Competency questions full / partial / none | 4 / 3 / 0 | 3 / 3 / 1 - question 5 a false partial (finding 3), really 4 / 2 / 1 |
| Reasoner | consistent | consistent, also with the sample data |
| Traceability (basis: competency questions) | 38.5 % untraceable | 57.1 % |
| Tokens (input / output) | 11.5k / 10.4k | 11.5k / 11.9k (plan 1.9k/4.0k, modules 5.6k/3.5k, CQ tests 4.0k/4.4k), plus the proposal call |

The ontology:
- **PhysicalObject:** `Wine` (with `vintageYear`), `Place` > `Country`, `Region` (Napa), `Dish`.
- **Quality:** `WineCharacteristic` > `WineColor` (Red, White, Rose), `WineBouquet`, `WineBody` (disjoint).
- **InformationObject:** `GrapeVariety` (Zinfandel), `DishCategory` (Seafood, GrilledMeat).
- Bordeaux, Cabernet Sauvignon and Napa Zinfandel are wines; Zinfandel is also a grape variety.

Competency questions (fresh sample data, no issue):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full - the kinds of characteristic (Bouquet, Color, Body), DISTINCT |
| 2 | Is Bordeaux a red or white wine? | full - `:BordeauxWine :hasQuality :Red` |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - Cabernet Sauvignon is a wine here |
| 4 | What is the best choice of wine for grilled meat? | partial - no ranking |
| 5 | Which characteristics affect appropriateness for a dish? | partial - but the query answers it (`WineBody`); the author adds that the ontology does not say whether the influence changes a particular pairing, which the question does not ask (finding 3) |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | not answerable - no characteristic per vintage |
| 7 | What were good vintages for Napa Zinfandel? | partial - years only, no quality |

### Findings

1. **The vocabulary uses the upper layer**: `hasQuality` points to Quality, `originatesIn` to PhysicalObject, so the
   characteristics and the places are reached through relations with a meaningful range instead of "any". Run 9's
   narrow `wineCharacteristicAffectsSuitabilityForCategory` is gone; question 5 now uses the core relation `affects`.
2. **`affects` is still any -> any**: its domain could be Quality. The proposal prompt allows "any" only for relations
   that connect many kinds of things; the model judged an influence to be one.
3. **"Leaves out" still over-reports about once per run**: run 8 question 1, run 10 question 5 - the author names
   something the question does not ask. The rule of DECISIONS 91 is followed most of the time; the residue is the
   price of a self-statement that can only lower a result. For the paper, the expert review (stage D) should check
   the partial results as well, not only the full ones.
4. **No module property below a core relation** - in all runs. With a four-relation vocabulary and own properties only
   for own kinds of connection (DECISIONS 90) that is consistent; whether it holds with a large vocabulary (VA) is open.
5. **Grape variety is back** (as an information object - a kind, like a dish category), but Cabernet Sauvignon is
   still a wine while Zinfandel is a grape variety. The vintage is an attribute again, so question 6 is not answerable.

### Wine runs: where they stand

Runs 6-10 give 4 of 7 questions fully answered (after correcting test errors), a hierarchy of depth 2-3 under the
upper layer, no modelling error the checks find, about 11-12k input tokens per generation and test. The three
remaining questions need modelling decisions (a ranking of pairings, a vintage quality, characteristics per vintage)
that no rule supplies; what still varies is single-run variance. Phases 3a and 3b are covered by the wine project;
3c-3e need loaded vocabularies and literature, i.e. the VA project.

## Run 9 - 2026-10-27, gpt-6-luna, commit b4bc1b5 (upper layer in planning, PLAN.md phase 3b, DECISIONS 97)

Same project, inputs, key notions and approved core relations as runs 4-8; the default upper layer, used by the
generation for the first time. The core relations were proposed before upper classes were allowed as domain or range,
so they do not use them yet.

**Generation report:** 2 modules, 10 planned classes -> 13 classes (3 of them upper) and 10 properties; **10
superclasses planned, all kept** by the modules; **upper layer: PhysicalObject, InformationObject, Quality used;
Process, Agent, Specification removed as empty; no top class outside it**; no second inverse, no redundant axiom, no
placeholder; core relations: none below them, 2 module relations without one, no violation.

| | Run 8 | Run 9 |
|---|---|---|
| Classes / object / datatype properties / individuals | 12 / 13 / 3 / 9 | 13 (3 upper) / 9 (5 core) / 1 / 8 |
| Root classes, hierarchy depth | 7 of 12; max 3, mean 1.58 | **3 of 13 (the upper classes); max 3, mean 2.15** |
| Disjointness axioms | 2 | 2 (the upper classes; colour, body, bouquet) |
| Relations / top-level / below a core relation | 8 / 8 / 0 | 6 / 6 / 0 |
| Unconnected classes / second inverses | 0 / 0 | 0 / 0 |
| Competency questions full / partial / none | 4 / 3 / 0 | 4 / 3 / 0 |
| CQ test: queries kept / sample issues | 0 / none | 0 / none |
| Reasoner | consistent | consistent with the disjoint upper classes, also with the sample data |
| Roots for "Group root classes" (repair) | - | 0 - nothing left to repair |
| Traceability (basis: competency questions) | 50 % untraceable | 38.5 % |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 11.3k / 12.4k | 11.5k / 10.4k (plan 1.9k/3.3k, modules 5.6k/3.3k, CQ tests 4.0k/3.8k) |

The ontology:
- **PhysicalObject:** `Wine`; `Place` > `Country`, `Region` (Napa); `Dish`.
- **Quality:** `WineCharacteristic` > `WineColor` (red, white), `WineBody`, `WineBouquet` (disjoint).
- **InformationObject:** `DishCategory` (Seafood, GrilledMeat).
- `hasVintageYear` on the wine; no vintage class, no grape variety (Bordeaux, Cabernet Sauvignon, Napa Zinfandel are
  wines).

Competency questions (fresh sample data, no issue): 1, 2, 3 and 5 full; 4 partial (no ranking), 6 partial (no change
over time), 7 partial (no vintage quality).

### Findings

1. **The upper layer works in the plan**: every top class is below an upper class, three upper classes are used and
   the three empty ones removed, the reasoner accepts the disjointness, and the evaluation finds no root class left for
   "Group root classes" - in the VA project that repair cost about 0.26 M input tokens. The plan's input grew by about
   0.3k tokens for the layer's definitions.
2. **The placements are plausible**: wine, places and dishes as physical objects, dish categories as information
   objects, characteristics as qualities. A region as a "material thing that occupies space" is the one to argue about;
   upper ontologies such as DOLCE treat geographic places as physical too.
3. **Colour, body and bouquet are each modelled once** - kinds of `WineCharacteristic`, colour with a value set - the
   first run without a duplicated representation.
4. **A narrow property beside a core relation**: `wineCharacteristicAffectsSuitabilityForCategory` (WineCharacteristic
   -> DishCategory) next to the core `affectsSuitabilityFor` (any -> Dish). The core relation's range is too narrow for
   categories, so the module made its own, named by the classes it connects. The vocabulary predates the upper layer;
   a new proposal can now choose an upper class as range.
5. **Vintage and grape variety are missing again** - variance, as before; questions 6 and 7 stay partial.

### Follow-ups (proposed)

- Run 10: propose the core relations again (now with upper classes available as domain and range), approve, regenerate.

## Run 8 - 2026-10-27, gpt-6-luna, commit 025b336 (untyped data individuals, fresh sample data, DECISIONS 96)

Same project, inputs, key notions and approved core relations as runs 4-7. The first run whose CQ tests started from
fresh sample data after the regeneration.

**Generation report:** 2 modules, 11 planned classes -> 12 classes and 16 properties; 5 superclasses planned, all kept
by the modules; no second inverse, no redundant axiom, no placeholder; core relations: none below them, 4 module
relations without one (`hasColor`, `hasVintage`, `hasVintageProfile`, `recordsVintage`), no violation.

| | Run 7 | Run 8 |
|---|---|---|
| Classes / object / datatype properties / individuals | 11 / 7 / 3 / 7 | 12 / 13 (5 core) / 3 / 9 |
| Root classes, hierarchy depth | 6 of 11; max 2 | 7 of 12; **max 3**, mean 1.58 (`Place` > `Origin` > `Country`, `Region`) |
| Subclass links / disjointness axioms | 5 / 3 | 5 / 2 |
| Relations / top-level / below a core relation | 5 / 5 / 0 | 8 / 8 / 0 |
| Unconnected classes / second inverses | 1 / 0 | 0 / 0 |
| Competency questions full / partial / none | 4 / 3 / 0 | 4 / 3 / 0 |
| CQ test: queries kept / sample issues | 2 / 29 old triples dropped | **0 / none** - fresh sample data, as intended |
| Reasoner | consistent | consistent, also with the sample data |
| Traceability (basis: competency questions) | 72.7 % untraceable | 50 % |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 11.0k / 12.1k | 11.3k / 12.4k (plan 1.6k/4.5k, modules 5.5k/4.7k, CQ tests 4.1k/3.3k) |

The ontology:
- **Wine module:** `Wine` with `hasColor` -> `Color` (Red, White); `Characteristic` with `BodyCharacteristic` and
  `BouquetCharacteristic` (disjoint); `Place` > `Origin` > `Country`, `Region` (BordeauxRegion, Napa); `Vintage`
  with `vintageYear`; `WineVintageProfile` - the body and bouquet of a wine in one vintage (`bodyValue`,
  `bouquetValue`, `recordsVintage`).
- **Dish module:** only `Dish`; Seafood and GrilledMeat are dishes (individuals), no dish category.
- Bordeaux the wine (`BordeauxWine`) and Bordeaux the region (`BordeauxRegion`) are kept apart; Cabernet Sauvignon is a
  wine, no grape variety.

Competency questions (nothing kept, no sample issue):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | partial - the author names two things it leaves out: what a customer "should" consider (a judgement, which the rule of DECISIONS 91 excludes) and the body and bouquet values of the vintage profiles, which the query indeed misses |
| 2 | Is Bordeaux a red or white wine? | full - `:BordeauxWine :hasColor :Red` |
| 3 | Does Cabernet Sauvignon go well with seafood? | full |
| 4 | What is the best choice of wine for grilled meat? | partial - no ranking |
| 5 | Which characteristics affect appropriateness for a dish? | full |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | **full, with values** - two vintage profiles of Napa Zinfandel, 2018 "black pepper" / "medium-bodied", 2020 "ripe berry" / "full-bodied" |
| 7 | What were good vintages for Napa Zinfandel? | partial - years only, no quality |

### Findings

1. **The CQ test now runs clean**: fresh sample data, no dropped triples, no undeclared terms, every partial result
   explained by its author. Run 8 is the first run whose result needs no correction.
2. **Question 6 has the best answer of all runs**: a vintage profile holds the body and bouquet of a wine in one
   vintage, so a change across vintages can be read from data.
3. **Body and bouquet still appear twice** - as kinds of characteristic (classes) and as literal values of a vintage
   profile; here at least with a reason (kind versus value per vintage), but nothing links a profile's values to the
   characteristic kinds.
4. **The Dish module is a single class**: dish kinds became individuals of `Dish`, no category, no ingredients; the
   module answer was 504 tokens. Variance again.
5. **Question 1 is partial partly for a reason the rule excludes** (what a customer "should" consider); the other reason
   (the profile values are not returned) is right. The narrowed rule is followed most of the time, not always.

### Runs 4-8 at a glance

| Run | Change | Top classes / depth | Relations (top-level) | CQ full / partial / none (corrected) |
|---|---|---|---|---|
| 4 | catch-all ruled out | 9 of 9 / 1 | 8 (8) | 5 / 2 / 0 after the CQ fixes (6 / 0 / 1 as first reported) |
| 5 | planned superclasses | 9 of 12 / 2 | 12 (12) | 5 / 2 / 0 |
| 6 | category rule, one inverse | 6 of 14 / 2 | 7 (7) | 4 / 3 / 0 |
| 7 | one representation per distinction | 6 of 11 / 2 | 5 (5) | 4 / 3 / 0 |
| 8 | fresh sample data | 7 of 12 / 3 | 8 (8) | 4 / 3 / 0 |

Since run 6 the results are stable: a hierarchy of depth 2-3 with about half the classes at the top, no modelling
error the checks find, and 4 of 7 questions fully answered. The three that stay partial need a ranking of pairings,
a vintage quality and (in some runs) characteristics per vintage - modelling decisions the questions ask for and no
rule supplies. What still varies between runs (grape variety or not, dish categories, how body and bouquet are
modelled) is the variance of single runs; it calls for repeated runs (PLAN.md phase 6), not more rules.

## Run 7 - 2026-10-27, gpt-6-luna, commit 98d6b1b (class answers from data, one representation per distinction, DECISIONS 95)

Same project, inputs, key notions and approved core relations as runs 4-6.

**Generation report:** 2 modules, 11 planned classes -> 11 classes and 10 properties; 5 superclasses planned, all kept
by the modules; no second inverse, no redundant axiom, no placeholder; core relations: none below them, 1 module
relation without one (`hasDishCategory`), no violation.

| | Run 6 (corrected) | Run 7 |
|---|---|---|
| Classes / object / datatype properties / individuals | 14 / 11 / 1 / 10 | 11 / 7 (5 core) / 3 / 7 |
| Root classes, hierarchy depth | 6 of 14; max 2 | 6 of 11; max 2, mean 1.45 |
| Subclass links / disjointness axioms | 8 / 1 | 5 / 3 (characteristic kinds, country and region, dish and dish category) |
| Relations / top-level / below a core relation | 7 / 7 / 0 | 5 / 5 / 0 |
| Unconnected classes / second inverses | 0 / 0 | 1 (`WineColorValue`) / 0 |
| Competency questions full / partial / none | 4 / 3 / 0 | 4 / 3 / 0 - two of the partial ones fail on the test, not the ontology (finding 2) |
| Reasoner | consistent | consistent, also with the sample data |
| Traceability (basis: competency questions) | 78.6 % untraceable | 72.7 % |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 11.4k / 13.5k | 11.0k / 12.1k (plan 1.6k/3.6k, modules 5.5k/4.4k, CQ tests 3.9k/4.1k) |

The ontology:
- **Wine module:** `Wine` with `hasVintageYear`, `hasBodyValue` and `hasBouquetValue` (literals); `WineCharacteristic`
  with `WineColorCharacteristic`, `WineBodyCharacteristic`, `WineBouquetCharacteristic` (disjoint); `WineColorValue`
  (Red, White); `Place` with `Country` and `Region` (disjoint).
- **Dish module:** `Dish`; `DishCategory` (Seafood, GrilledMeat), disjoint from `Dish`.
- Bordeaux, Cabernet Sauvignon and Zinfandel are all wines; no grape variety, no vintage class, no place individuals.

Competency questions (two queries kept from run 6; 29 triples of run 6's sample data dropped):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full - the kinds of characteristic, but the list includes `:Wine`, because the kept sample data say `:NapaZinfandel :hasCharacteristic :Zinfandel` and Zinfandel is a wine here (finding 3) |
| 2 | Is Bordeaux a red or white wine? | full - through the value set: `:Bordeaux :hasCharacteristic ?c . ?c a :WineColorValue` |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - query kept from run 6 |
| 4 | What is the best choice of wine for grilled meat? | partial (failed) - `:grilledMeat` counts as undeclared, although the sample data use it (finding 2); partial anyway, no ranking |
| 5 | Which characteristics affect appropriateness for a dish? | full - query kept from run 6 |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | partial - two Napa Zinfandel wines per year with body and bouquet values, but nothing says they are the same wine |
| 7 | What were good vintages for Napa Zinfandel? | partial (failed) - `:Napa` counts as undeclared, although the sample data use it (finding 2); partial anyway, no quality |

### Findings

1. **The rule "one representation per distinction" worked for colour, not for body and bouquet.** Colour is no longer
   both subclasses of wine and a value set. But body and bouquet are now both classes (`WineBodyCharacteristic`,
   `WineBouquetCharacteristic`) and literal properties of the wine (`hasBodyValue`, `hasBouquetValue`), and nothing
   connects `WineColorCharacteristic` with its values `WineColorValue` (unconnected).
2. **The CQ test treats individuals that appear only in the sample data, untyped, as undeclared terms.** `:Napa` and
   `:grilledMeat` occur in the sample data (as objects of `hasOrigin` and `hasDishCategory`), but only typed subjects
   count as sample individuals. The check exists to stop invented classes and properties; an individual of the sample
   data is data, whether typed or not.
3. **Kept sample data carry earlier ontologies' individuals into a new one.** The sample data are kept across
   iterations so that results stay comparable (DECISIONS 67). After a regeneration that keeps triples like
   `:NapaZinfandel :hasCharacteristic :Zinfandel` (from run 6, where Zinfandel was a grape variety) and the spelling
   `:grilledMeat` (run 6's data; the ontologies have `:GrilledMeat`). They fit the new ontology formally but not in
   meaning - question 1 now lists "Wine" as a kind of characteristic.
4. **The ontology is smaller again** (no vintage, grape variety or place individuals) - variance between single runs.
5. **Hierarchy stable**: 5 superclasses planned and all kept, 6 top classes, and three disjointness axioms - the most
   so far.

### Follow-ups (proposed)

- CQ test: every IRI in subject or object position of the sample data counts as a sample individual (finding 2).
  **Done** (DECISIONS 96). Re-running this run's queries: questions 4 and 7 now run and return rows; with what their
  author says they leave out (no ranking, no quality) they stay partial - 4 full, 3 partial, for the right reasons.
- CQ test after a regeneration: start from fresh sample data, as a new ontology is not comparable with the old one's
  data; keep them only between iterations of the same generation (finding 3). **Done** (DECISIONS 96).

## Run 6 - 2026-10-27, gpt-6-luna, commit e25f467 (category rule, one inverse per property, DECISIONS 94)

Same project, inputs, key notions and approved core relations as runs 4 and 5. Changes since run 5: a class of
categories is never placed below the thing it categorizes; a second inverse is removed at the merge. The generation
report was stored in the project for the first time.

**Generation report:** 2 modules, 14 planned classes -> 14 classes and 12 properties; **8 superclasses planned, all
kept by the modules** (none had to be set from the plan, none placed differently); no second inverse, no redundant
axiom, no placeholder; core relations: none below them, 3 module relations without one (`hasVintage`,
`hasVintageCharacteristic`, `hasDishCategory`), no violation.

| | Run 5 | Run 6 |
|---|---|---|
| Classes / object / datatype properties / individuals | 12 / 20 / 3 / 11 | 14 / 11 (5 core) / 1 / 10 |
| Root classes, hierarchy depth | 9 of 12; max 2, mean 1.25 | **6 of 14; max 2, mean 1.57** |
| Subclass links | 3 (one wrong: `DishCategory` < `Dish`) | 8, all plausible (finding 1) |
| Relations / top-level / below a core relation | 12 / 12 / 0 | 7 / 7 / 0 |
| Unconnected classes / second inverses | 0 / 1 | 0 / 0 |
| Competency questions full / partial / none | 5 / 2 / 0 | 3 / 4 / 0 - with question 2 a false negative (finding 3), really 4 / 3 / 0 |
| Reasoner | consistent | consistent, also with the sample data |
| Labelled / without domain or range | 100 % / 0 | 100 % / 0 |
| Traceability (basis: competency questions) | 50 % untraceable | 78.6 % (the subclasses are named by no passing query) |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 12.1k / 15.8k | 11.4k / 13.5k (plan 1.6k/4.6k, modules 5.5k/4.1k, CQ tests 4.3k/4.8k) |

The ontology:
- **Wine module:** `Wine` with `RedWine` and `WhiteWine` (disjoint); `Characteristic` with `ColorCharacteristic`
  (Red, White), `BodyCharacteristic`, `BouquetCharacteristic` and `GrapeVariety` (Zinfandel); `Origin` with `Country`
  and `Region` (Napa, BordeauxRegion); `Vintage` with `vintageYear` and `hasVintageCharacteristic` (characteristics
  per vintage).
- **Dish module:** `Dish`; `DishCategory` (Seafood, GrilledMeat) as a class of its own, not below `Dish`.

Competency questions (one query reused from run 5; 15 triples of run 5's sample data dropped):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full |
| 2 | Is Bordeaux a red or white wine? | **failed** - `SELECT ?type WHERE { :Bordeaux a ?type . VALUES ?type { :RedWine :WhiteWine } }` returns `:RedWine`, which is right; the guard against "answers from the schema" rejects it because the answer is a class (finding 3) |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - the query kept from run 5; Cabernet Sauvignon is a wine in this ontology |
| 4 | What is the best choice of wine for grilled meat? | partial - the query uses `:grilledMeat`, the ontology has `:GrilledMeat` (finding 4); without a ranking it would be partial anyway |
| 5 | Which characteristics affect appropriateness for a dish? | full |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | partial - characteristics per vintage, but no values to compare |
| 7 | What were good vintages for Napa Zinfandel? | partial - years only, no quality |

### Findings

1. **The hierarchy is the best so far, and the category rule worked**: 8 subclass links, all kept by the modules,
   6 of 14 classes at the top. `DishCategory` stands on its own, kinds of wine (`RedWine`, `WhiteWine`, disjoint) and
   kinds of characteristic exist. `GrapeVariety` below `Characteristic` is a choice one can argue about, but not wrong
   for "what describes a wine".
2. **Colour is modelled twice**: as subclasses (`RedWine`, `WhiteWine`) and as a value set (`ColorCharacteristic` with
   Red and White). The planned hierarchy invited the subclasses; nothing tells the plan that one of the two is enough.
3. **The CQ test rejects a correct answer that is a class (bug in the test).** The guard "the result consists only of
   ontology terms - it answers from the schema" exists to catch queries that list schema terms without touching the
   data. Here the query asks for the type of a data individual, and the answer is a class by nature. The guard should
   ask whether the answer depends on the sample data - run the query on the ontology alone: if it returns nothing
   there, the answer comes from the data.
4. **A query names an individual in the wrong case** (`:grilledMeat` for `:GrilledMeat`), in the query and the sample
   data. The test reports it as an undeclared term, which is right; it costs nothing here because the question is
   partial anyway.
5. **Cabernet Sauvignon is a wine, Zinfandel a grape variety** - the plan does not keep the questions' named things
   consistent. As in run 5, this is single-run variance rather than a rule to add.
6. **Traceability looks worse (78.6 %) because the new subclasses are named by no passing query** - a limit of the
   CQ-based measure without literature, not of the hierarchy.

### Follow-ups (proposed)

- CQ test: replace "only ontology terms" by "the answer depends on the sample data" - an answer counts unless the
  same query already returns it on the ontology alone (finding 3). **Done** (DECISIONS 95; the schema alone is the
  ontology without its individuals). Re-running this run's queries with it: question 2 passes, nothing else changes -
  4 full, 3 partial.
- Plan rule: one representation per distinction - a distinction is either subclasses or a value set, not both
  (finding 2). **Done** (DECISIONS 95).

## Run 5 - 2026-10-27, gpt-6-luna, commit 4b08690 (planned superclasses, DECISIONS 92)

Same project, inputs, key notions and approved core relations as run 4 (`hasCharacteristic`, `hasOrigin`,
`goesWellWith`, `affectsSuitabilityFor`); the only change is that the plan gives every class its superclass. The
generation report was not copied and was not yet stored in the project (it is since this run), so the plan's own
numbers - superclasses planned, set from the plan, placed differently by a module - are lost; the table shows the
hierarchy as it ended up.

| | Run 4 (re-test) | Run 5 |
|---|---|---|
| Classes / object / datatype properties / individuals | 9 / 13 / 4 / 10 | 12 / 20 (5 core) / 3 / 11 |
| Root classes, hierarchy depth | 9 of 9; max 1 | 9 of 12; max 2, mean 1.25 |
| Subclass links | none | `Country`, `WineRegion` < `OriginPlace`; `DishCategory` < `Dish` (wrong, finding 2) |
| Relations / top-level / below a core relation | 8 / 8 / 0 | 12 / 12 / 0 (8 module relations without one) |
| Unconnected classes | 2 (`Country`, `Region`) | 0 |
| Competency questions full / partial / none | 5 / 2 / 0 | 5 / 2 / 0 |
| Reasoner | consistent | consistent, also with the sample data |
| Labelled in all languages / without domain or range | 100 % / 0 | 100 % / 0 |
| Traceability (basis: competency questions) | 22.2 % untraceable | 50 % (`OriginPlace`, `Country`, `WineRegion`, `DishCategory`, `DishIngredient`, `CookingMethod`) |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 10.6k / 11.3k + re-tests | 12.1k / 15.8k (plan 1.5k/4.7k, modules 5.6k/6.5k, CQ tests 5.0k/4.6k) |

The ontology:
- **Wine module:** `Wine`; `Characteristic` (Bouquet, Body as individuals) with `CharacteristicObservation` (a value
  of a characteristic for a wine, linked to a `Vintage`); `OriginPlace` with `Country` and `WineRegion` (disjoint);
  `Vintage` with `hasVintageYear`; `WineColorCategory` (Red, White).
- **Dish module:** `Dish` with `DishCategory` below it (Seafood, GrilledMeat as individuals); `DishIngredient`;
  `CookingMethod` (Grilling).
- **No grape variety class**: Bordeaux, Cabernet Sauvignon and Napa Zinfandel are all wines again.

Competency questions (nothing reused - a new ontology; 16 triples of run 4's sample data dropped; no other sample
issue):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider? | full - the characteristics (Bouquet, Body), DISTINCT as the new rule asks |
| 2 | Is Bordeaux a red or white wine? | full |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - `:CabernetSauvignon :goesWellWith :seafoodDish`, right for this ontology, where Cabernet Sauvignon is a wine |
| 4 | What is the best choice of wine for grilled meat? | partial - no ranking |
| 5 | Which characteristics of a wine affect its appropriateness for a dish? | full |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | **full, new** - two observations of the same characteristic of one wine for two vintages |
| 7 | What were good vintages for Napa Zinfandel? | partial - years only, nothing says what is good (run 4 had a quality value) |

### Findings

1. **The hierarchy is no longer flat, but still shallow**: three subclass links instead of none, and the plan
   introduced a broader class of its own (`OriginPlace` over `Country` and `WineRegion`), which connects the two
   classes that were unconnected in run 4. Nine of twelve classes are still roots; no kinds of wine, no kinds of
   dish (dish kinds are individuals of `DishCategory`).
2. **`DishCategory` was placed below `Dish`**: a category of dishes is not a dish - its individuals (Seafood,
   GrilledMeat) are categories, and the subclass link makes every category a dish. The plan rule "plan a broader class
   where several classes are kinds of one notion" does not say that a value set describing X is not a kind of X.
3. **The grape variety is gone again**: run 4 had `GrapeVariety` with `hasGrapeVariety`; run 5 has no such class and
   types Cabernet Sauvignon as a wine. The questions name the grape, but nothing in the plan rules asks for the
   distinction; it varies between runs (runs 2 and 4 had it, 3 and 5 did not).
4. **A property has two inverses**: `isVintageOfObservation` (Vintage -> CharacteristicObservation) is declared the
   inverse of `hasVintage` (Wine -> Vintage), which already has `isVintageOf`. The reasoner does not object, but it
   would type every observation linked from a vintage as a wine.
5. **Question 6 is answered for the first time with the right structure** - characteristic observations per vintage
   (`CharacteristicObservation`) - and question 7 lost its quality value. Between runs the model trades one modelling
   decision for another; single runs do not show a trend.
6. **No module property below a core relation, inverses for every module property** - as in run 4.

### Follow-ups (proposed)

- **Done** (DECISIONS 94): plan rule: a class whose members are categories, types or grades of X (a value set) is never a subclass of X
  (finding 2).
- **Done** (DECISIONS 94): merge or evaluation: report a property declared as the inverse of a property that already has another inverse
  (finding 4).
- The generation report is now stored in the project and shown after a reload (DECISIONS 93).
- Findings 3 and 5 are variance between single runs; the paper's runs need repetitions (EVALUATION.md, "evaluate 3x"
  in PLAN.md phase 6) rather than more prompt rules.

## Run 4 - 2026-10-27, gpt-6-luna, commit 0fee2f3 (follow-ups of run 3, DECISIONS 90)

Same project, inputs and key notions as runs 2 and 3. The core-relation vocabulary was proposed again with the
sharpened prompt (no catch-alls) and approved unchanged; the modules got the new rule (own property for an own kind
of connection, below a core relation only if it shares its meaning).

**The vocabulary** (nothing dropped; labels came with the proposal):

| Relation | Domain -> range | Inverse | Covers |
|---|---|---|---|
| `hasCharacteristic` | Wine -> any | - | CQ1, CQ2, CQ5, CQ6, CQ7 |
| `hasOrigin` | Wine -> any | - | CQ7 |
| `goesWellWith` | Wine -> Dish | `hasSuitableWine` | CQ3, CQ4, CQ5 |
| `affectsSuitabilityFor` | any -> Dish | - | CQ5 |

| | Run 2 (re-test) | Run 3 | Run 4 |
|---|---|---|---|
| Classes / object / datatype properties / individuals | 15 / 21 / 1 / 7 | 13 / 11 / 1 / 11 | 9 / 13 (5 core) / 4 / 10 |
| Relations / top-level relations | 11 / 8 | 7 / 5 | 8 / 8 |
| Below a core relation / without one | - | 2 / 1 | 0 / 4 (`hasWineColor`, `hasGrapeVariety`, `hasCharacteristicType`, `hasDishCategory`) |
| Root classes, hierarchy depth | 7; max 3 | 7; max 3 | **9 of 9; max 1 - no subclass at all** |
| Unconnected classes | 0 | 1 | 2 (`Country`, `Region`) |
| Competency questions full / partial / none | 4 / 0 / 3 | 4 / 1 / 2 | **6 / 0 / 1** |
| Labelled in all languages / properties without domain or range | 100 % / 0 | 86.1 % / 3 | 100 % / 0 |
| Reasoner | consistent | consistent | consistent, also with the sample data |
| Traceability (basis: competency questions) | 53.3 % untraceable | 61.5 % | 11.1 % (only `Country`) |
| OOPS! | timeout | timeout | timeout |
| Tokens (input / output) | 15.8k / 14.5k | 10.6k / 14.7k | 10.6k / 11.3k (plan 1.4k/3.7k, modules 5.3k/4.8k, CQ tests 3.9k/2.8k), plus the proposal call |

The ontology:
- **Wine module:** `Wine` with `hasWineColor` -> `WineColor`, `hasGrapeVariety` -> `GrapeVariety`, `hasVintageYear`
  (`xsd:integer`) and `hasVintageQuality` (`xsd:decimal`); `Characteristic` as an entity with
  `hasCharacteristicType` -> `CharacteristicType` (Bouquet, Body) and a text or numeric value; `Country` and `Region`,
  reached only through the core relation `hasOrigin` (range "any").
- **Dish module:** `Dish` and `DishCategory` (seafood, grilled meat as individuals), declared disjoint.
- **Individuals:** Bordeaux (Wine), Cabernet Sauvignon and Zinfandel (GrapeVariety), Napa (Region), Red and White,
  Bouquet and Body, the two dish categories.

Competency questions (nothing reused - a new ontology; 12 triples of run 3's sample data dropped):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider when choosing a wine? | full - characteristic types (Body, Bouquet) through `hasCharacteristic` |
| 2 | Is Bordeaux a red or white wine? | full - `:Bordeaux :hasWineColor :Red` |
| 3 | Does Cabernet Sauvignon go well with seafood? | full on paper - but the query treats the grape variety `:CabernetSauvignon` as a wine (`goesWellWith` has domain Wine, so the reasoner silently types the grape as a wine) |
| 4 | What is the best choice of wine for grilled meat? | full on paper - the query lists wines that go with grilled meat; nothing ranks them ("best" is ignored) |
| 5 | Which characteristics of a wine affect its appropriateness for a dish? | full - `affectsSuitabilityFor` |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | not answerable: characteristics are not tied to a vintage |
| 7 | What were good vintages for Napa Zinfandel? | **full, new** - `hasVintageQuality` with `hasVintageYear` on the wine, ordered by quality |

### Findings

1. **The sharpened prompt removed the catch-all**: the vocabulary names specific connections (characteristic,
   origin, pairing, influence on suitability), the modules created their own `hasWineColor` and `hasGrapeVariety`,
   Cabernet Sauvignon is a grape variety again, labels are complete and nothing is counted as lacking domain or range.
2. **6 of 7 questions pass, but two passes are wrong or hollow.** Question 3 answers through a grape treated as a wine;
   question 4 drops "best" and passes on a plain list - the test model wrote a query that answers an easier question.
   Real coverage is about 4 of 7. The CQ test checks that a query runs and returns rows, not that it answers the
   question; this needs a check of the query against the question (e.g. the test model states which part of the
   question each query part answers, and a question with a superlative or comparison needs an ORDER BY or a filter).
3. **The class hierarchy collapsed**: 9 root classes, no subclass at all (run 3: `GeographicPlace` over `Country` and
   `WineRegion`, `Dish` over seafood and meat dishes). The plan made dish kinds individuals of `DishCategory` (a
   legitimate value-set choice) and left country and region side by side. Nothing in the run 4 changes concerns the
   hierarchy; it is the variance of a single run, and a reason to plan the hierarchy explicitly (phase 3d, here
   without literature: the plan could be asked for the broader class of each planned class).
4. **`Country` and `Region` are unconnected**: they are only reachable through `hasOrigin`, whose range is "any",
   because before generation only key notions may be domain or range (DECISIONS 89). A place class planned by
   the model cannot be named in the vocabulary. A module property below `hasOrigin` (Wine -> Region) would have
   connected them; the model did not create one.
5. **No module property was placed below a core relation** (run 3: two, both wrong). `hasWineColor` could have been
   placed below `hasCharacteristic` - the model kept them apart. With four relations this is harmless; with a large
   vocabulary the top level grows again.
6. **The vintage is an attribute of the wine** (`hasVintageYear`, `hasVintageQuality`), which answers question 7
   because each wine individual stands for one vintage, but not question 6.
7. **Inverses remain for all four module properties.**
8. **The pattern cleanup worked**: the list holds only Wine and Dish now.

### Follow-ups (proposed)

- CQ test: make the test model say how its query answers the question, and treat a query that answers an easier
  question (drops a superlative or comparison, uses an individual of the wrong class) as partial (finding 2).
  **Done** (DECISIONS 91): the sample-data check drops `:CabernetSauvignon :goesWellWith :SeafoodPlate` from this
  run's data (the only triple it drops), so question 3 would no longer pass; question 4 depends on the test model
  reporting what its query leaves out.
  **Re-test from scratch with commit 2221dff** (same ontology, new sample data and queries, 3.9k / 3.5k tokens):
  2 full, 4 partial, 1 none. Question 3 now passes correctly, through a wine of the grape variety
  (`?wine :hasGrapeVariety :CabernetSauvignon ; :goesWellWith ?dish`); question 4 is partial (nothing to rank by),
  as intended. Questions 1 and 5 were marked partial wrongly ("does not say which ones a customer should consider",
  "does not rank the degree"), question 7 is borderline (no threshold for "good", but the query sorts by quality).
  The rule was narrowed the same day (DECISIONS 91, revision).
  **Second re-test from scratch with the narrowed rule** (4.0k / 4.1k tokens): **5 full, 2 partial, 0 none**, no
  sample issues. Questions 1, 2, 3, 5 and 7 full - 3 again through a wine of the grape variety, 7 returns the
  vintages with their quality value. Question 4 partial (no ranking), as intended; question 6 now partial instead of
  not answerable: the query lists body and bouquet with the vintage year of each wine and says that the ontology
  cannot show a change across vintages. Traceability: 22.2 % untraceable (`Country`, `Region`, see finding 4).
  Every test from scratch writes new sample data and queries, so single results vary; this one matches the reading
  of the questions in the table above.
- Planning: ask for the broader class of each planned class, so a flat plan becomes the exception (finding 3, a
  first step towards phase 3d). **Done** (DECISIONS 92).
- Vocabulary: let the plan name the domain and range of a core relation more precisely after planning, or allow the
  module to place a narrower property below it - to be decided with phase 3b (upper layer in planning), which gives
  "any" a set of upper classes to choose from (finding 4).
- Fewer inverses: an inverse only where a question needs both directions (open point in DECISIONS).

## Run 3 - 2026-10-27, gpt-6-luna, commit 2d916f2 (core relations from step 7)

Same project, inputs and key notions (Wine, Dish) as run 2; the only change is the approved core-relation vocabulary
from step 7 (PLAN.md phase 3a, DECISIONS 89). Run 2's ontology was replaced by the regeneration.

**The vocabulary** (one proposal call, approved unchanged; one proposed relation dropped because its inverse
`hasSuitableWine` was named twice):

| Relation | Domain -> range | Inverse | Covers |
|---|---|---|---|
| `hasDescription` | Wine -> any | - | CQ1, CQ2, CQ6, CQ7 |
| `goesWellWith` | Wine -> Dish | `hasSuitableWine` | CQ3, CQ4 |
| `influences` | any -> any | - | CQ5 |
| `variesWith` | any -> any | - | CQ6 |

The model's summary: a general description relation for wine details "whose representation may vary"; origin,
vintage and characteristic values left to the modules.

| | Run 2 (re-test) | Run 3 |
|---|---|---|
| Modules | Wine, Dish | Wine, Dish, CoreRelations |
| Classes / object / datatype properties / individuals | 15 / 21 / 1 / 7 | 13 / 11 (5 core) / 1 / 11 |
| Relations (one per inverse pair) / top-level relations | 11 / 8 | 7 / 5 |
| Below a core relation / without one | - | 2 (`hasOrigin`, `hasVintage`, both below `hasDescription`) / 1 (`hasDishCategory`); no domain/range violation |
| Axioms | 5 (3 repeating the hierarchy) | 1 (Seafood and meat dishes disjoint) |
| Root classes, hierarchy depth | 7; max 3, mean 1.6 | 7; max 3, mean 1.54 |
| Competency questions full / partial / none | 4 / 0 / 3 | 4 / 1 / 2 |
| Reasoner | consistent | consistent, also with the sample data |
| Labelled in all languages | 100 % | 86.1 % - the core relations have no labels (finding 4) |
| Unconnected classes / properties without domain or range | 0 / 0 | 1 (`WineVariety`) / 3 (the core relations with "any") |
| Traceability (basis: competency questions) | 53.3 % untraceable | 61.5 % untraceable |
| OOPS! | timeout | timeout |
| Tokens (input / output) | 15.8k / 14.5k (+ re-test 4.9k / 2.5k) | 10.6k / 14.7k (plan 1.4k/4.4k, modules 5.3k/7.5k, CQ tests 3.8k/2.8k), plus the proposal call |

The ontology:
- **Wine module:** `Wine`; `WineCharacteristic` with `WineColor`; `WineVariety`; `GeographicPlace` with `Country` and
  `WineRegion`; `Vintage` with `vintageYear` (`xsd:integer`), linked by `hasVintage`.
- **Dish module:** `Dish` with `SeafoodDish` and `MeatDish` > `GrilledMeatDish`; `DishCategory`.
- **Individuals:** Bordeaux, CabernetSauvignon and NapaZinfandel (Wine), Zinfandel (WineVariety), Napa (WineRegion),
  Red and White (WineColor), Body and Bouquet (WineCharacteristic), two dish categories.

Competency questions (CQ test: nothing reused - a new ontology - and 13 triples of run 2's sample data dropped
because their properties are gone):

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider when choosing a wine? | full - `hasDescription` to a `WineCharacteristic` |
| 2 | Is Bordeaux a red or white wine? | partial - `:Bordeaux :hasDescription ?c . ?c a :WineColor` is right, but the sample data say nothing about Bordeaux |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - but Cabernet Sauvignon is now a wine, not a grape variety |
| 4 | What is the best choice of wine for grilled meat? | not answerable: nothing ranks a pairing |
| 5 | Which characteristics of a wine affect its appropriateness for a dish? | full - newly via `influences` (characteristic -> dish) |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | **full, new** - `Vintage` is a class, `variesWith` links a characteristic to a vintage |
| 7 | What were good vintages for Napa Zinfandel? | not answerable: no vintage quality |

### Findings

1. **The core relations remove the duplicate relation and shrink the relation count**: `goesWellWith` exists once
   (run 1 and 2 had a second version in the Dish module), 7 instead of 11 relations, 5 instead of 8 at the top level.
   `Vintage` became a class, and question 6 is answered for the first time.
2. **The vocabulary is too general, and the modules followed it too literally.** `hasDescription` (Wine -> any) is a
   catch-all: colour, characteristics and grape variety are now only reachable through it, `hasOrigin` and
   `hasVintage` were placed below it although origin and vintage are not descriptions, `WineVariety` lost its link
   to `Wine` (unconnected), and Cabernet Sauvignon became a wine instead of a grape variety. The proposal prompt asks
   to prefer "any" to a narrow domain or range, and the module rule allows an own property "only where a competency
   question needs a distinction" - together they push everything into the most general relation. The questions still
   pass, through `rdf:type` filters (`?c a :WineColor`), but the ontology says less than run 2's (`hasColor`,
   `hasGrapeVariety`, `hasOrigin` as relations of their own).
3. **`influences` and `variesWith` make questions 5 and 6 pass on thin data**: `:Body :variesWith
   :NapaZinfandelVintage` says that "body" in general varies with one vintage, not that this wine's body does. Like
   finding 9 of run 2, "full" overstates the answer.
4. **The core relations have no labels and no language-tagged descriptions** (bug in `core_properties`, which builds
   them directly instead of through the edit operations the consolidation uses). Labelled entities drop from 100 % to
   86.1 %.
5. **The structural check counts the core relations with "any" as "properties without domain or range"** - for a
   general relation that is intended, not a problem.
6. **Question 2 fails on missing sample data**: the CQ test wrote nothing about `:Bordeaux` (no sample issue is
   reported, so it was not dropped). A model omission; a re-run of the CQ tests would likely pass it.
7. **Inverses remain for the module properties** (`isOriginOf`, `isVintageOf`, `categoryOfDish`); the core vocabulary
   itself has one inverse only.
8. **The pattern list still holds run 1's stale entries**: the cleanup runs only on "Continue" from step 6, and step 7
   was opened through the sidebar.

### Follow-ups

The first four are built in [DECISIONS 90](../../DECISIONS.md); run 4 is open.

- Labels for the core relations in every label language, as the consolidation gives them (finding 4) - a bug fix.
- Proposal prompt: no catch-all relations ("has description", "has property", "is related to"); each relation names
  one kind of connection. Module rule: an own property for a connection of its own kind (a value set, a variety, a
  place, a time), below a core relation only if it shares its meaning (finding 2).
- Structural metrics: leave the core relations out of "properties without domain or range" (finding 5).
- Pattern cleanup also when step 7 is opened from the sidebar (finding 8).
- Then run 4 with a new proposal of the vocabulary, to see whether finding 2 is solved.

## Run 2 - 2026-10-27, gpt-6-luna, commit 92ab90d (two key notions)

Same project as run 1 (`0241c125`, renamed "Wine Run 2"), same use case, conventions and seven questions, no
literature, no data files, no standards. Two key notions added from the suggestions: **Wine** and **Dish**. The
pattern list still holds run 1's six entries for the invented notions (none selected, so they did not reach the
generation); the pattern step was not run again for the two real notions.

The first CQ test lost its sample data to a bug (finding 1). After the fix (DECISIONS 87) the
CQ tests were re-run on the same ontology ("Re-run tests", keeping the sample data) and the evaluation repeated;
the figures below are from that re-test.

| | Run 1 | Run 2 |
|---|---|---|
| Modules | 3, proposed by the plan | 2, the key notions |
| Classes / object / datatype properties / individuals | 6 / 7 / 5 / 0 | 15 / 21 / 1 / 7 |
| Axioms | 2 | 5 (2 DisjointClasses, 3 SubClassOf that repeat the hierarchy) |
| Root classes, hierarchy depth | 4; max 2, mean 1.33 | 7; max 3, mean 1.6 |
| Competency questions full / partial / none | 3 / 0 / 4 | 4 / 0 / 3 (first test, with the bug: 0 / 4 / 3) |
| Reasoner | error on `xsd:gYear` | consistent, also with the sample data; no datatype outside OWL 2 |
| OOPS! | minor only | not checked: the service timed out (60 s) |
| Traceability (basis: competency questions) | 50 % untraceable | 73.3 % untraceable (11 of 15; see finding 9) |
| Tokens (input / output) | 10.6k / 10.8k in 5 calls | 15.8k / 14.5k in 5 calls (plan 1.4k/3.0k, two modules 4.8k/6.0k, CQ tests twice 9.6k/5.4k); the re-test 4.9k / 2.5k more |

The ontology:
- **Wine module:** `Wine`; `WineCharacteristic` with `WineColor`, `BodyCharacteristic` and `BouquetCharacteristic`;
  `GrapeVariety`; `OriginLocation` with `Country` and `Region`.
- **Dish module:** `Dish` with `SeafoodDish` and `MeatDish` > `GrilledMeatDish`; `FoodIngredient`; `CookingMethod`.
- **Individuals:** Bordeaux (Wine), CabernetSauvignon and Zinfandel (GrapeVariety), Napa (Region), Red and White
  (WineColor), Grilling (CookingMethod).
- **Properties:** the vintage is `hasVintageYear` (`xsd:integer`). `isRelevantToDish` links a characteristic to a
  dish, for question 5.

Competency questions:

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider when choosing a wine? | full - lists every value of `hasWineCharacteristic`; as in run 1 it passes on any wine data |
| 2 | Is Bordeaux a red or white wine? | full - `:Bordeaux :hasColor ?color` returns `:Red`; Bordeaux is the ontology's individual |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - a wine with grape `:CabernetSauvignon` that `goesWellWith` a `SeafoodDish`; the sample wine was made up for the question |
| 4 | What is the best choice of wine for grilled meat? | not answerable: nothing ranks a pairing |
| 5 | Which characteristics of a wine affect its appropriateness for a dish? | full - via `isRelevantToDish`, but the query narrows the question to grilled-meat dishes |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | not answerable: no vintage as a thing of its own |
| 7 | What were good vintages for Napa Zinfandel? | not answerable: no vintage quality |

### Findings

1. **The CQ test throws away the sample data about the ontology's own individuals (bug).** The sample-data guard
   (`_split_sample_data` in `testing.py`) rejects every triple whose subject occurs in the ontology, to stop the
   test from changing classes or properties. Since run 2 the ontology has individuals, and the model rightly wrote its
   data about them: all nine triples with `:Bordeaux` as subject were dropped as "changes an ontology term". The
   remaining ten triples contain no wine with a colour, a characteristic or a dish it goes with, which is what the
   queries ask for (the expected answers name `:Bordeaux`, `:Red`, `:MediumBody`), so four sound queries return
   nothing. Run 1 was not affected: it had no individuals. **Fixed** (DECISIONS 87); the re-test on the same
   ontology answers questions 1, 2, 3 and 5 fully, with no sample-data issues.
2. **The plan is fuller with key notions and the new planning rules**: 15 instead of 6 classes, value sets
   (`WineColor`), grape variety, origin with country and region, kinds of dishes, ingredients and cooking methods,
   and the individuals the questions name. Still missing: kinds of wine (red, white, sparkling as classes or a
   value set beyond colour), winery/producer, sweetness, values for body and bouquet.
3. **The datatype fix works**: the vintage is an `xsd:integer`, the reasoner runs, and nothing outside OWL 2 is reported.
4. **A relation is still modelled twice across modules**: the Wine module defines `goesWellWith`/`isSuitableForWine`,
   the Dish module `isSuitableWithWine` (Dish to Wine, also declared inverse of `goesWellWith`). As in run 1; phase 3a.
5. **Every object property comes with an inverse** (21 of 21), which doubles the property count; only 22.7 %
   of the properties are used by a CQ query. "Fewer inverse properties" is an open point in DECISIONS.
6. **The SubClassOf axioms repeat the hierarchy** (`SeafoodDish` SubClassOf `Dish` and so on). This is redundant, not
   wrong, but it inflates the axiom count.
7. **The vintage is still an attribute**, so questions 6 and 7 stay unanswerable; question 4 needs a ranked pairing.
   As in run 1, these need modelling decisions (phase 3a/5), not more terms.
8. **Patterns of notions that no longer exist stay in the list**, and the pattern step is not offered again when the
   key notions change, because it only runs automatically while the list is empty.
9. **"Full" says little about how good the answer is.** The passing queries are thin: question 1 lists every
   characteristic of any wine, question 3 passes on a sample wine invented to answer it, question 5 answers only for
   grilled meat. And traceability counted only classes a passing query names: `WineColor` and `GrapeVariety` are
   reached through `hasColor` and `hasGrapeVariety` (ranges of used properties) but counted as untraceable. The first
   is a limit of the measure, worth stating in the paper. The second is fixed (DECISIONS 88): domains and ranges of
   the properties a passing query uses count as well, which brings this run from 73.3 % to 53.3 % untraceable (8 of
   15: the body, bouquet, origin, meat-dish, ingredient and cooking-method classes, which no passing query reaches).

### Follow-ups (proposed)

- Fix the sample-data guard: triples about the ontology's individuals are instance data; only schema statements
  (typing as a class or property, `subClassOf`, `domain`, `range` and the like) about ontology terms are rejected.
  **Done** ([DECISIONS 87](../../DECISIONS.md)); re-test recorded above.
- Patterns: when key notions change, drop or mark the choices of notions that are gone, and offer the pattern step
  for new notions. **Done** (DECISIONS 88).
- Leave out SubClassOf axioms that only repeat the `parent` of a class when merging the modules. **Done** (DECISIONS 88).
- Duplicate relations, inverses and the vintage as an entity belong to phase 3a (core relations before generation).
- Traceability: count the domain and range classes of the properties a passing query uses (finding 9). **Done**
  (DECISIONS 88).

## Run 1 - 2026-10-16, gpt-6-luna, commit baf0514 (no key notions in effect)

Project `0241c125`, RWTHgpt/KI:connect `gpt-6-luna`. Use case, conventions and the seven questions as in the README;
no data files, no patterns, no standards. The context was drafted and two rounds of questions answered.

**Key notions did not reach the generation.** The key-notion suggestions were requested but not added with "+ Add";
the list kept its empty placeholder row. The server counted that row as a key notion, so the pattern step ran anyway
and the model made up six notions for it from the glossary (Wine, Characteristic, Origin, Vintage, Dish, Goes well
with). The generation filtered the empty row out and the plan proposed the modules itself. This run is therefore the
"without key notions" variant.

| | |
|---|---|
| Modules | 3, proposed by the plan: Wine, Place, Dish |
| Classes / object / datatype properties / individuals | 6 / 7 / 5 / 0 |
| Axioms | 2 (DisjointClasses Wine-Characteristic, Country-Region) |
| Root classes, hierarchy depth | 4; max 2, mean 1.33 |
| Top-level relations | 4 |
| Competency questions | 3 of 7 fully covered, 4 not answerable |
| Reasoner | error: HermiT rejects `xsd:gYear` (not in the OWL 2 datatype map) |
| OOPS! | minor only (P04 on `opla:Module`) |
| Tokens | 10,623 input / 10,824 output in 5 calls (plan 1.3k/2.8k, three modules 6.2k/5.3k, CQ tests 3.1k/2.8k) |

The ontology: `Wine` with `Characteristic`; `Place` with `Country` and `Region`; `Dish`. Colour, body and bouquet are
string datatype properties next to a `Characteristic` class, the grape variety a string (`hasGrapeVarietyName`),
the vintage a year (`hasVintageYear`, `xsd:gYear`).

Competency questions:

| # | Question | Result |
|---|---|---|
| 1 | Which wine characteristics should I consider when choosing a wine? | full - lists colour, bouquet and body with OPTIONAL, so it passes on any wine |
| 2 | Is Bordeaux a red or white wine? | full - Bordeaux is a wine individual in the sample data, not a region or wine type |
| 3 | Does Cabernet Sauvignon go well with seafood? | full - grape as a string, Seafood a Dish individual |
| 4 | What is the best choice of wine for grilled meat? | not answerable: nothing ranks a pairing |
| 5 | Which characteristics of a wine affect its appropriateness for a dish? | not answerable: nothing links a characteristic to a pairing |
| 6 | Does a bouquet or body of a specific wine change with vintage year? | not answerable: no vintage as a thing of its own |
| 7 | What were good vintages for Napa Zinfandel? | not answerable: no vintage quality |

### Findings

1. **The path without literature runs end to end** (plan, three modules, merge, OOPS!, CQ tests, evaluation) and
   is cheap: about 21k tokens in total.
2. **Empty key notions count as key notions** (UI and server). Suggestions that are not added are lost without a
   warning, and the pattern step accepts a list with only an empty row and lets the model invent notions.
3. **The plan is very small**: 6 classes against 4-15 per module asked for. Without literature the plan only has the
   use case, seven questions and a thin context, and plans the minimum. Notions a wine shop obviously needs are
   missing as classes: grape variety, winery, vintage, wine colour/sugar/body/flavour as value sets, kinds of wine,
   meal courses or kinds of food. Nothing is modelled as individuals although the questions name them (Bordeaux,
   Cabernet Sauvignon, Napa, seafood, grilled meat).
4. **The four failed questions need modelling decisions**, not more terms: a vintage as an entity with a quality, a
   pairing as an entity with a strength or a ranking, a link from characteristics to pairings. CQ4OE reports 0 % full
   coverage on wine for all nine models; the questions are hard by design.
5. **A relation was modelled twice across modules**: the Wine module defined `goesWellWith`/`isSuitableForWine`, the
   Dish module its own `goesWellWithWine` (Dish to Wine). Modules run in parallel and do not see each other's
   properties. Phase 3a (core relations before generation) addresses this.
6. **`xsd:gYear` breaks the reasoner and is outside OWL 2 DL** although the conventions say OWL 2 DL. The prompts do
   not name the allowed datatypes, and the reasoner check does not handle them.
7. **Traceability is not meaningful without literature**: 50 % "untraceable" only because there are no sources and
   no inventory; only passing CQ queries could count.
8. **No hold-out test** without an inventory (expected); the evaluation says so.

### Follow-ups

Built in [DECISIONS 86](../../DECISIONS.md) except run 2. Re-evaluating this run's ontology with the fixed reasoner
check: consistent, also with the CQ sample data; `xsd:gYear` (hasVintageYear) reported as outside OWL 2. Traceability
now says it rests on the competency questions only.

- Key notions: ignore empty rows everywhere (save, pattern step, counts); warn on leaving step 6 with suggestions
  that were not added; refuse the pattern step without a named key notion.
- Datatypes: name the OWL 2 datatypes in the module prompt (years as `xsd:integer` or `xsd:gYear` only outside OWL 2
  DL); map non-OWL-2 datatypes for the reasoner check and report them.
- Planning without literature: ask for the notions a domain expert would expect for the use case beyond the literal
  words of the questions, and for individuals the questions name.
- Traceability without literature: base it on the competency questions only and say so.
- Run 2 with key notions, after these fixes.
