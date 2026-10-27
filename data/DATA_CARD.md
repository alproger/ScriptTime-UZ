# Dataset card — prototype ONLY

The `data/seed/` records are three researcher-authored paraphrases linking to official sources. They are NOT full legal texts, NOT a human-audited gold benchmark, and NOT independently annotated evidence.

The 9 rows of `queries.csv` represent **3 independent question groups** in three script variants. These variants are correlated. Smoke-test percentages do not establish scientific validity.

Sources in seed data:
- 1993 alphabet law: https://lex.uz/docs/-112286
- 2026 alphabet law: https://lex.uz/docs/8548754
- 2023 school admissions resolution 214: https://lex.uz/docs/6479366

`study_valid_from` and `study_valid_to` represent an experimental applicability interval, which may be clipped to the study window and must not be described as the law's historical full validity span.

Future corpus must retain source URL, revision ID, clause identifier, human rationale, publication/access and clause-effective dates, annotator agreement, source license assessment, and question-family grouping.

No private student records or user-uploaded Toolbase documents are permitted.
