# Independent-methodology audit for ScriptTime-UZ v0.2

Date: 2026-10-27 · **Research integrity report, not peer review**

## What is demonstrably implemented
- Five deterministic lexical retrieval configurations (BM25, normalized BM25, normalized character-trigram, BM25 + operative filter, normalized BM25 + operative filter).
- Two explicit temporal information intents: `published_document` and `operative_rule`. Date filtering no longer hides an announced-but-future law during document discovery. **There is no trained intent classifier.**
- A historical version-pair case for 214/3a appendix, and a mixed-domain development corpus linked to selected LexUZ records.
- Automated tests across three Python versions; reproducible diagnostic scripts.
- Clustered-by-question *exploratory* paired bootstrap (not by script variant), with explicit statistical caveats.

## What is **not** scientifically proven
- No independent corpus of clause-level legal validity intervals has been fully audited and adjudicated.
- The mixed sample has **9 paraphrase passages**, 8 base question groups and 24 correlated variants; it is development data, not held-out evaluation.
- The 30 drafted human-review questions (#2–#6) are still pending author approval; even author approval is not blind annotation by an independent evaluator.
- A few original document-date fields are approximations, and some `study_valid_from` values mean the **start of the observed experimental snapshot**, not real original effective date.
- The implemented time filter is trivial in one-candidate situations. A hard-negative benchmark must keep multiple plausible candidates simultaneously.
- No dense encoder has been fine-tuned; there is no benchmarked AI model checkpoint.
- No production Toolbase deployment, professor endorsement, Scopus indexing or publication acceptance.

## Scientific novelty audit: comparisons
1. **Nam et al. (2026), TimelyRAG (EMNLP Findings):** already models complex temporal validity in overlapping-evolving regulations. Our simple filter is not novel. A possible distinctive contribution is a human-audited Uzbek cross-script × temporal-intent benchmark plus errors and new low-resource transfer findings. That novelty remains **unverified**.
   https://aclanthology.org/2026.findings-emnlp.398/
2. **Kang et al. (2026), R-GDA (EACL Findings):** approaches data augmentation fidelity for *named-entity recognition*. It does not validate ScriptTime-UZ nor directly provide a retrieval baseline. Its lesson is careful synthetic-data validation.
   https://aclanthology.org/2026.findings-eacl.259/
3. **Adxamov (2026), Uzbek hybrid RAG:** already covers Uzbek documents, BM25+dense retrieval and Cyrillic–Latin preprocessing; our work cannot claim to introduce those features.
   https://innovativepublication.uz/index.php/jelsi/article/view/6287

## Biggest threat: source/time annotation
Question `as_of` is a legal-effective date; `known_at` limits when evidence was publishable. These are independent. More difficult cases can involve retroactive amendments, staggered effective dates, preserved old documents, or unknown effective intervals. Do not silently set an unknown interval to an invented date or use today's LexUZ edition for a past-version claim.

Another threat: target laws are often mentioned in question wording. A lexical model can score well by matching document titles instead of truly resolving applicability. We need deliberately ambiguous, version-confusable, human-reviewed questions.

## Minimum publishable pilot
- 5+ independent legal families with clause-level audited versions, **multiple eligible candidates per question**;
- 20+ independently reviewed base questions as a limited pilot, with held-out groups and script equivalence review;
- clearly separated `published_document` vs `operative_rule` tasks;
- paired baselines, normalization×time ablations, errors and independent question-group counts;
- actual results with cautious uncertainty and limitations; model/AI-use disclosure per venue rules;
- honest description as a **small feasibility pilot**, not definitive state of the art.

### Decision for 29 October
Conference submission is a *target, not guaranteed*. If source review and held-out evaluation remain insufficient, do not manufacture results or reclassify CI smoke tests as research accuracy. GKS-oriented expanded work can continue with audited data, an encoder model and independent validation after the conference deadline.

Official alphabet-law example: https://lex.uz/uz/docs/8548754
