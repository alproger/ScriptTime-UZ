# Two-factor temporal experiment and grouped uncertainty — preregistration draft

## Factorial design, not yet a validated benchmark
Main dimensions:
- script variant: old Latin / proposed revised Latin / Cyrillic
- evidence intent: published_document / operative_rule
- retrieval normalizer: raw / normalized
- operative time constraint: disabled / enabled (only meaningful in operative_rule queries)

**Do not combine both intents' scores without a stratified breakdown.** A published future rule (O‘RQ–1184 in October 2026) is retrievable as a document but not yet enforceable as an operative rule.

## Sample size and leakage
The currently added `intent_boundary_queries.csv` has just **2 original question groups** and their 6 correlated script variants; it only tests plumbing. The mixed-domain sample has only **8 original question groups** across 5 related legal families, authored by the developers; it cannot support claims about real-world performance.

For future human-reviewed experiments:
- exact-gold evidence IDs bound to dates (not only title/URL)
- no paraphrased question group appears in both dev and test
- if possible split by entire law families to test generalization to unseen regulations
- include same-time negative documents so date filters do not trivially leave one answer
- predefine failure taxonomy (wrong version, wrong family, script mismatch, unpublished evidence, not yet effective, no evidence)
- stratify findings by task intent and writing system
- compare paired baselines by *original question group*, not by variant count.

## Statistical report
`src/scripttime/analysis.py` computes an explicitly exploratory **paired percentile bootstrap** across question groups. It is reproducible with a fixed RNG seed.

It does **not** account for document-family dependence and is not credible with tiny group count or developer-authored test cases. An eventual paper should use a larger independent dataset, nested resampling and human adjudication.

## Evidence sources
- O‘RQ–1184 law, 2026: https://lex.uz/uz/docs/8548754
- Nam et al., TimelyRAG, EMNLP Findings 2026: https://aclanthology.org/2026.findings-emnlp.398/
- Kang et al., R-GDA, EACL Findings 2026: https://aclanthology.org/2026.findings-eacl.259/

The new evaluation scenario is **methodological infrastructure**, not a novel trained model, breakthrough, or accepted publication.
