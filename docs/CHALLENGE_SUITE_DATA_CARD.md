# Adversarial temporal-intent development suite — 29 October 2026

**STATUS: NOT AN INDEPENDENT BENCHMARK.** This suite contains **13** source-linked researcher summaries, **24 question templates and 72 correlated orthographic variants**. It was developed knowing the document collection and algorithms, so any metric is **engineering diagnostics only**.

## Why this exists
- Tests exact day-before/day-of transition boundaries (labor 2023-04-30; water 2025-10-31; Annex 3a quota 2026-07-03; alphabet 2027-04-22).
- Distinguishes questions about a **published future document** from a **currently operative provision**.
- Contains **seven** deliberately unanswerable query templates (no exact eligible evidence in this **finite** toy corpus), requiring abstention rather than substituting another document.
- Adds source-linked same-time distractors: 214 Annex 3 committee paragraphs 7 and 8; law 1184 Articles 2 and 4. These are paraphrases, not full legal text.
- Includes Cyrillic and algorithmically converted revised Latin variants. Revised Latin variants are *not linguistically human-verified*.
- Removes **post-2023/2025/2026 hindsight statements** from records incorrectly presented as historically available old sources.

## Important caveats
1. Old legal records are researcher summaries, not verbatim frozen historical editions. `available_from` for snapshot paraphrases does not always represent genuine original publication; the source registry must be audited.
2. `study_valid_from` for historic excerpts means a **confirmed study snapshot**, not an independently established first legal validity date.
3. Certain **no-answer labels reflect missing exact admissible evidence** in this controlled passage set; they are not determinations that the real legal question lacks an answer.
4. Temporal retrieval can still score highly by rejecting obvious wrong-date documents; the corpus is small and not a realistic law library.
5. Same law family appears repeatedly. There are not 24 independent legal families.
6. **Gold answer and eligibility may be mismatched in future copies** if source metadata is later corrected. Recompute after human review, never silently retain labels.
7. Do not use these 72 variants as 72 independent observations, as evidence of an AI model being trained, or as an unbiased claim of effectiveness.
8. Question CH16 and CH23 deliberately require a *metadata-based* no-evidence policy; a generative model could answer "no" from other evidence. The target task is passage retrieval, NOT full question answering.

## Official cross-checks
- Alphabet law: https://lex.uz/uz/docs/8548754 (O‘RQ–1184, 2026-10-21; effective 2027-04-22)
- 214 Annex 3a old and new: https://lex.uz/uz/docs/-6479366?ONDATE=26.11.2025 and https://lex.uz/uz/docs/-6479366?ONDATE=03.07.2026
- 214 Annex 3 clauses 7 and 8: https://lex.uz/uz/docs/-6479366
- Labor code: https://lex.uz/uz/docs/-142859 and https://lex.uz/uz/docs/-6257288
- Water laws: https://lex.uz/uz/docs/-12328 and https://lex.uz/uz/docs/-7655336

## Reproduce
```bash
python -m pip install -e .
python -m scripttime evaluate --case challenge
```
