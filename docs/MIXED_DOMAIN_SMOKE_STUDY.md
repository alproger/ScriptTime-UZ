# Mixed-domain temporal retrieval smoke test (2026-10-27)

**Research integrity warning:** This is a developer-authored benchmark **smoke test**, not a held-out independent scientific dataset. Original legal sources are linked, but paraphrases and candidate questions have not been blind-reviewed. Results **MUST NOT** be used as conference statistics of generalization.

## Controlled source composition
- Old/new labor code, boundary 2023-04-30 (O‘RQ–798).
- Old/new water law, boundary 2025-10-31 (O‘RQ–1076).
- Existing/announced alphabet, boundary 2027-04-22 (O‘RQ–1184).
- Annex 3a school-quota clause versions, boundary 2026-07-03 (VM 353).
- One additional active governance policy as a negative/distractor (VM 526).
**Total: nine source-linked paraphrase records from five document families; 8 manually drafted question groups × 3 script variants = 24 correlated query rows.**

Important caveat: `study_valid_from` values may denote the *studied snapshot interval*, not the original rule's first legal effective date. The source `available_from` is an operational approximation, not exhaustive version provenance. Do not infer actual historic validity from those fields without a lawyer/reviewer check.

## Four requirements before quantitative paper
1. The corpus must contain enough **same-time, similar-topic** negative documents to make retrieval difficult; single-candidate filtering is a trivial test.
2. Review the orthographic variants: several are manual approximations of new Latin and may not reflect authentic usage.
3. Separate draft question pools from independent human-authored test questions and split by document family, not merely by variants.
4. Report the algorithm's failure on *announced but not yet effective* legislation. Searching for a future rule's effective date is an **information-availability** task, whereas finding a provision that was legally operative on a historical date is a **rule-applicability** task. A naive strict time filter can wrongly exclude an announced future law. Do NOT conceal this distinction.

## Run
```bash
python -m pip install -e .
python -m scripttime evaluate --case mixed_temporal
```
Do not copy these percentages into the manuscript until human-gold data is available. The script emits `DEVELOPMENT_SMOKE_TEST_NOT_PEER_REVIEWED_NOT_HELD_OUT` explicitly.
