# ScriptTime-UZ research protocol — draft

Date: 2026-10-27
Status: not peer-reviewed, not preregistered.

## Research question
What is the effect of query-script normalization, evidence validity filtering, and their interaction on correctly retrieving historical evidence in Uzbek regulatory texts?

## Hypotheses to test (not findings)
- H1: Normalization improves cross-script retrieval relative to raw lexical matching.
- H2: Filtering by applicable evidence interval reduces wrong-version top-1 retrieval.
- H3: A combined approach may perform differently from the sum of each individual modification.
- H4: Simple metadata filtering fails when clauses of a single law have different effective dates.

## Dataset methodology
Target at least 30 versioned official clauses across at least 10 independent document families. Have independent annotators verify document URL, version, publication time, effect interval, clause, and gold evidence. Author 60 or more independent question groups plus independently reviewed Latin, revised Latin and Cyrillic variants. Exclude unstable interpretations until adjudicated.

## Time fields
- `published_at` or `available_from`: information available to the system
- `valid_from` / `valid_to`: clause-specific rule applicability
- `as_of`: historical/legal date in the question
- `known_at`: cutoff on evidence publication available to the system
These must never be conflated. Some records in the seed data use *study-window* bounds, not original legal effective dates.

## Methods
M0 BM25 (raw); M1 BM25 normalized; M2 normalized character 3-grams; M3 BM25 + time filter; M4 normalized BM25 + time filter. Dense retriever and fine-tuned small encoder are **future** work, not yet trained.

## Evaluation
Hit@1, Recall@3, MRR@3, invalid-evidence@1, family-level error taxonomy, timing, confidence intervals via original-question clusters; supplementary document-family clustering. Split original questions and revisions of a document family together to avoid leakage. Annotate retrieval *coverage*, not only accuracy.

## Threats to validity
Small data, correlated question variants, mistaken legal-effective intervals, license restrictions, generated paraphrase bias, imperfect transliteration, ambiguous historical interpretation, and domain shifts. Inference should never use the seed dataset as statistical proof.

## Publication gate
Verify source texts and source rights, human-review gold answers, freeze train/test partitions, run experiments reproducibly, calculate group-wise CIs, log failures, verify every quote/reference, disclose material AI assistance under venue rules, obtain author's approval.
