# Tutorial: a wine recommendation ontology from five sources

This tutorial takes you once through every step of LITMO on a small domain: an ontology for a wine shop that helps
customers choose a wine, built from five openly available texts. It takes about two hours, most of it waiting for
the model, and about 45-55 model calls.

The domain is deliberately well known, so you can judge the result yourself. For the same reason it is not a test of
whether the tool generalises: the models know the W3C wine ontology (see [README.md](README.md)). The recorded runs
on this domain are in [RUNS.md](RUNS.md).

**You need:** LITMO running (`start.bat`, then http://localhost:8000/app; see the [Quick start](../../README.md#quick-start)),
an API key for one of the supported providers, and the five sources below.

## 0. Collect the sources

The sources are not part of the repository: download them from their original places. Save the web pages as PDF
(print to PDF) or as plain text; the tool reads both.

| # | Source | Where |
|---|---|---|
| 1 | N. F. Noy, D. L. McGuinness: *Ontology Development 101: A Guide to Creating Your First Ontology* (2001) | linked from https://protegewiki.stanford.edu/wiki/Ontology101 |
| 2 | W3C: *OWL Web Ontology Language Guide* (2004), built around a wine and food ontology | https://www.w3.org/TR/owl-guide/ |
| 3 | *WineGraph: A Graph Representation For Food-Wine Pairing* (2024) | https://arxiv.org/abs/2407.00107 |
| 4 | Wikipedia: *Wine and food pairing* | https://en.wikipedia.org/wiki/Wine_and_food_pairing |
| 5 | Wikipedia: *Wine tasting descriptors* | https://en.wikipedia.org/wiki/Wine_tasting_descriptors |

Also use [`wines.csv`](wines.csv), a wine list of 15 wines (the vintages, body, sweetness and prices are
illustrative).

Why these five: 1 and 2 are the classic wine examples of ontology engineering (the competency questions below come
from 1), 3 is a recent research paper on food-wine pairing, 4 and 5 give everyday wine vocabulary. They overlap
enough that some concepts appear in two or more sources and become *central*. Source 1 also brings
ontology-engineering vocabulary (class, slot, instance), which should not end up in a wine ontology; source 3 brings
the vocabulary of its method (graphs, embeddings). Watch in step 8 whether the tool keeps both out.

Do **not** add the W3C wine ontology itself (`wine.rdf`) as a source or as a vocabulary: it is the reference to
compare with at the end.

## 1. Model and key

1. Header: **New project**.
2. Choose the provider, enter your key, choose the model. **Continue**.

Any model of the supported providers works; the recorded runs used GPT-6 sol (and, as the open model,
DeepSeek-V4.1-Flash). Small models plan smaller ontologies and make more logical errors ([RUNS.md](RUNS.md), round 7).

## 2. Use case and data

1. **Use case or problem**:
   > A wine shop wants to help its customers choose a wine. The ontology describes wines by their characteristics,
   > their origin and their vintage, and says which wines go well with which dishes, so that a recommendation
   > service can answer customers' questions.
2. **Data sources**: `The shop's wine list (wines.csv): name, grape, colour, region, country, vintage, body,
   sweetness, price.`
3. Drop `wines.csv` into the file area. It appears with a short profile (columns, rows).
4. **Continue → Literature**.

## 3. Literature

1. Drop the five sources.
2. **Extract paper cards**: one model call per source. Each card lists the concepts of the source with a definition,
   the page and a quote; quotes that cannot be found in the text are marked.
3. Open one or two cards and read them.
4. **Build concept inventory**: the concepts of all sources merged, with how many sources name them, conflicting
   definitions and themes (candidate modules).
5. **Continue → Project context**.

## 4. Project context

1. **Draft project context**.
2. Go through the tabs:
   - **Context document**: what the ontology is for and what it leaves out. Edit it where it is wrong.
   - **Open questions**: answer two or three, then **Apply answers**.
   - **Definitions**: the conflicting definitions from the inventory. Accept one proposal or write your own.
   - **Conventions**: namespace `https://example.org/wine#`, prefix `wine`, label language English.
   - **Upper layer**: the few general classes every module hangs from. Keep the default.
3. **Continue → Competency questions**.

## 5. Competency questions

1. Add the seven questions of Noy & McGuinness with **Add question**:
   - Which wine characteristics should I consider when choosing a wine?
   - Is Bordeaux a red or white wine?
   - Does Cabernet Sauvignon go well with seafood?
   - What is the best choice of wine for grilled meat?
   - Which characteristics of a wine affect its appropriateness for a dish?
   - Does a bouquet or body of a specific wine change with vintage year?
   - What were good vintages for Napa Zinfandel?
2. **Suggest questions** once; accept one or two that fit the use case, discard the rest.
3. **Continue → Key notions**.

Questions from the literature that the suggestion has not seen are kept back as *hold-out questions* for step 9.
With only five sources the suggestion sees all of them, so this project has none.

## 6. Key notions and modules

1. Add **Wine**, **Dish**, **Grape** and **Region**, each with a one-line description, or take them from the
   inventory's themes.
2. **Suggest missing key notions** once; a pairing notion (e.g. **FoodWinePairing**) is a typical good proposal.
3. **Continue → Design decisions**.

Each key notion becomes one module of the ontology.

## 7. Design decisions

1. **Patterns**: **Suggest design patterns**; keep the one or two that fit, deselect the rest.
2. **Core relations**: **Propose core relations**. The table is the small set of general relations all modules
   share (for five modules about 10-20). Remove one that seems wrong, then **Approve**.
3. **Key notion links**: **Propose links**. These say how the key notions relate to each other (e.g. a wine is made
   from a grape, a pairing recommends a wine for a dish). Check each link and its reading, edit or remove links,
   then **Approve**.
4. **Vocabularies and prefixes**: select one or two general vocabularies if you want links to them (e.g. Schema.org);
   leave out the W3C wine ontology.
5. **Continue → Generate**.

## 8. Generate

1. **Generate Ontology**. The tool plans all modules first, generates them one by one, merges them and checks the
   result (Turtle syntax, logical checks, a reasoner). This takes several minutes.
2. Read the report. Look at:
   - **plan size**: how many classes were planned, and whether the plan was extended;
   - **central concepts**: every concept named in two or more sources is either a class or excluded with a reason;
   - **class restrictions** written, refused by the checks or removed by the reasoner;
   - **key notion links** added.
3. Look at the tabs **Classes**, **Properties**, **Individuals**, **Graph** and **OWL / Turtle**. Each class has a
   definition and, where it comes from the literature, its sources.
4. **Continue → Evaluate & Refine**.

A typical result with a large model: five modules, 60-80 classes, all central concepts placed, the reasoner
consistent.

## 9. Evaluate and refine

1. **Evaluate 3×**: the competency questions are translated into SPARQL three times and run against sample data
   generated for the ontology. Because the model is involved, results vary; three runs show the spread.
2. **Overview**: the scores per question and the structure figures; **Needs attention** lists what to look at.
3. **Questions**: per question the three runs, the SPARQL and the answer.
4. **Repair tools**: run one that is offered (e.g. adding class restrictions or building the hierarchy); the dialog
   says how many model calls it needs.
5. **Evaluate** again. The overview now compares the new iteration with the previous one.
6. **Edit**: one refinement in plain language, e.g. "Add a class SparklingWine below Wine", then **Refine**. The
   model returns precise changes and the server applies them, so nothing you did not ask for changes. In the Turtle
   editor (**Open editor**) you can also change the file directly and **Save & Apply**.
7. **Export**: the ontology as Turtle, the documentation (HTML or Markdown, one chapter per module) and, with
   **Generate SHACL**, shapes for the data.

## 10. Keep the project

**Export project** in the header saves the whole project, including the source texts and every decision, as one
file. **Import** brings it back on any LITMO installation. Do not pass the file on if your sources may not be
redistributed.

## 11. Compare with a reference (optional)

The CQ4OE benchmark (github.com/oeg-upm/cq4oe-benchmark, Apache-2.0) has a gold standard for these questions:
`sub_wine.owl`, an excerpt of the W3C wine ontology, with five questions (it drops the three dish questions and adds
"What grapes are used to make Bordeaux wine?").

1. **New project**; in step 2 **Start from an existing ontology** and load `sub_wine.owl`. The import note says what
   it could not read (some restrictions and enumerations).
2. Step 5: add the five questions; step 9: **Evaluate 3×**.
3. In your wine project add "What grapes are used to make Bordeaux wine?" and **Evaluate 3×** again.

Both are then tested on the same five questions, the same way. The recorded comparison is in [RUNS.md](RUNS.md).
