# Engineering-only mixed-domain retrieval diagnostic

Run date: **2026-10-27**  
CI evidence: https://github.com/alproger/ScriptTime-UZ/actions/runs/40508279293  
Source commit: `06b8b0900740886b166150f26c570e8e9989c5e2`

**Do not cite these numbers as scientific findings or in a submitted article.** This dataset and its labels were authored alongside the algorithms, questions are not independently assessed, and it is NOT a held-out benchmark.

## Tested data
- **9** legal source-linked researcher paraphrase records; **5** document families.
- **8** base question groups; **24** scripted variants (old Latin, proposed new Latin, Cyrillic).
- **5** algorithms: BM25, normalized BM25, normalized character trigrams, BM25 with strict operative-time filter, normalized BM25 with operative-time filter.
- **24 technical unit tests passed** in Python 3.10, 3.12 and 3.13. This is software correctness, not empirical validity.

## Engineering diagnostics

| Method | Exact top-1 hits / 24 correlated variants | Hit@1 | Recall@3 | MRR@3 |
| --- | ---: | ---: | ---: | ---: |
| BM25 | 17/24 | 0.7083 | 0.9583 | 0.8333 |
| Normalized BM25 | 18/24 | 0.7500 | 1.0000 | 0.8750 |
| Normalized character trigram | 15/24 | 0.6250 | 1.0000 | 0.8125 |
| BM25 + operative-time filter | 23/24 | 0.9583 | 1.0000 | 0.9722 |
| Normalized BM25 + operative-time filter | 24/24 | 1.0000 | 1.0000 | 1.0000 |

The denominator **24 is not an independent sample size**; there are only 8 unique question groups. Some groups were composed to reflect the known labels. **High accuracy here is NOT evidence of improvement on unseen documents.** Confidence intervals computed over 24 variants would be spuriously narrow.

## Failure cases noted in CI
- Non-time-aware raw and normalized BM25 confuse old/new labor code on questions around the 2023-04-30 boundary.
- Character-trigram matching can favor the wrong legal edition despite common topic words.
- The operative-time filter improves this synthetic diagnostic but may itself solve the task trivially when only a single valid candidate remains.
- Most importantly, strict applicability filtering is the WRONG retrieval predicate for asking about an **already published but not-yet-effective future law** (O‘RQ–1184). See [Issue #8](https://github.com/alproger/ScriptTime-UZ/issues/8).

## Publication blocker
Before reporting any empirical superiority, recruit independent human annotation of true effective clauses and questions; hold out unseen question and document families; include hard same-time negatives; verify script variants; implement and test document-availability retrieval separate from operative-rule filtering; report clustered error uncertainty and negative outcomes.

Relevant source and annotation review: [candidate questions](../data/annotation/candidate_questions_v1.csv), [human review Issues #2–#6](https://github.com/alproger/ScriptTime-UZ/issues), [mixed dataset](../data/experiments/mixed_temporal_records.jsonl).
