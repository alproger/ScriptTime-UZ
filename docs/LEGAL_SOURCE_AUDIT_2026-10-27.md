# Evidence-source audit and limits (2026-10-27)

## Selection method
Five legal domains are represented in `candidate_questions_v1.csv`. These are 30 **draft question groups**, not 30 statistically independent human-annotated samples. Several questions share the same document passage and cannot count as independent evidence.

| Domain | Source(s) | Independently located fact | Limits |
| --- | --- | --- | --- |
| Alphabet reform | https://lex.uz/docs/8548754 | Law O‘RQ–1184 adopted 2026-10-21; effective 2027-04-22; 28 letters and an apostrophe sign | Other future amendments may change historical applicability; current law not effective yet |
| Labor | https://lex.uz/uz/docs/-142859 and https://lex.uz/docs/-6257345 and https://lex.uz/uz/docs/-6257288 | 1995 labor code replaced by O‘RQ–798; effective from 2023-04-30 | Old and new codes are DIFFERENT document IDs, not identical clause revisions |
| Water | https://lex.uz/uz/docs/-12328 and https://lex.uz/uz/docs/-7655336 | 1993 water law replaced by O‘RQ–1076 (adopted 2025-07-30; effective 2025-10-31) | Full provisions and transitional exceptions require separate legal review |
| School annex | https://lex.uz/uz/docs/-6479366?ONDATE=26.11.2025 and https://lex.uz/uz/docs/-6479366?ONDATE=03.07.2026 | Annex 3a introduced via resolution 740/2025 and clause 3 amended via 353/2026 | Concerns foreign-language-specialized school boarding schools, **not** Presidential school admissions |
| School governance | https://lex.uz/docs/-4387224 | Resolution 526/2019 annex chapter 5 repealed from 2023-06-02; para 4 updated 2025-03-01; chapter 19 wording amended 2025-12-19 | Mix of metadata and legal content; need precise historical snapshots to train or test |

## Critical research limitations
- This file is a *candidate question pool*. Answers are model-prepared, referenced and **await human review**. The human-review status is deliberately not gold.
- Metadata-only questions ("when was X adopted?") are relatively easy and should be separately stratified from semantic retrieval and hard temporal conflict questions.
- Same law, same paragraph, and paraphrased prompts are correlated. Count unique document families and question groups; use no duplicate text across train/test.
- Date awareness must not be evaluated only in a corpus where the time filter leaves one candidate. That is a tautological smoke test.
- Do not synthesize old law versions that have not been verified.
- Publication rights and direct quotes: original full texts are NOT copied here; registry uses citations and paraphrases.
- Future planned variant generation must be reviewed for Uzbek linguistic fidelity, especially new/old Latin conversion and Cyrillic transliteration.

## Human review
Review the five issue lists (#2–#6). Reply in each issue with `ID ✅`, `ID ❌: correction` or `ID ⚠️: ambiguity`. Only after the reviewer verifies sources and scope should `review_status` become `author_verified`.

## Holdout conditions
Candidate answers have already been drafted from retrieved sources, so they can serve as **development** labels only after review. A blind held-out test must be written and reviewed independently, with document-family separation when feasible. Do not report post-hoc performance on this pool as an unbiased generalization estimate.
