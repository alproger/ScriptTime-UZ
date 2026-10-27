# Temporal intent: published evidence vs operative legal rule

Issue: [#8](https://github.com/alproger/ScriptTime-UZ/issues/8). Status: implemented as a **simple baseline**.

## Explicit distinction

- **`published_document`**: The user asks what document *says*, e.g. “On 27 October 2026, when is O‘RQ–1184 scheduled to take effect?” The source must have been published by `known_at`, even if not legally effective on that date. It must not be silently removed.
- **`operative_rule`**: The user asks which provision *was legally in force at* `as_of`. Filter for publication by `known_at` **and** applicable study interval at `as_of`.

The law of 21 October 2026 that changes Uzbek alphabet only becomes effective on 22 April 2027. Its amended 28-letter rule is not yet operative on 27 October 2026, but the law is published and its future entry-into-force date can already be found. Source: https://lex.uz/uz/docs/8548754.

## Running both modes

```bash
python -m scripttime query "O'RQ-1184 28 harf" --method bm25_norm_time --case seed --known-at 2026-10-27 --as-of 2026-10-27 --evidence-mode published_document
python -m scripttime query "amaldagi alifbo" --method bm25_norm_time --case seed --known-at 2026-10-27 --as-of 2026-10-27 --evidence-mode operative_rule
```

## Integrity caveats
1. Temporal intent is explicitly set by the caller; **no automatic intent classification has been trained**.
2. `available_from` is an approximation of the source publication record. Published *amendments* may not be reflected as a new record, so a production use must index the complete source revision history.
3. `study_valid_from` can be the **beginning of our audited window**, not actual law's original effective date. Do not equate them.
4. Scores are simple lexical relevance values, **not calibrated probabilities**. Rejecting zero-overlap documents is not sufficient reliable abstention.
5. This is not TimelyRAG: no clause-level overlapping-revision temporal reranking, no learned retrieval model, no held-out validation.
6. A discovery question and an operative-rule question are different evaluation tasks; never combine their accuracy in one unlabelled percentage.
7. A time-aware baseline differs from a lexical baseline in its *operative validity constraint*; both filter by publication cutoff for fair exposure.

## Research hypothesis
Can a low-resource Uzbek query-intent classifier distinguish **publication/discovery** from **operative applicability**, and how does script variation influence misclassification and downstream retrieval? This is a proposed study, not completed results.

## Research inspirations
Nam et al., *TimelyRAG*, Findings of EMNLP 2026: https://aclanthology.org/2026.findings-emnlp.398/
Kang et al., *R-GDA*, Findings of EACL 2026: https://aclanthology.org/2026.findings-eacl.259/
Uzbek regulatory RAG: https://innovativepublication.uz/index.php/jelsi/article/view/6287
