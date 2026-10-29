# Adversarial development diagnosis — 29 October 2026

**Status: DEVELOPMENT DIAGNOSTIC. NOT A HUMAN-REVIEWED GOLD BENCHMARK.**

## Reproduction
- Source commit: `291b22af8d9664a85d9378556e68a8924618a01b`
- [GitHub Actions run 40906336842](https://github.com/alproger/ScriptTime-UZ/actions/runs/40906336842)
- `python -m scripttime evaluate --case challenge`
- `python -m scripttime.audit`
- **101/101 automated unit tests pass** on CPython 3.10, 3.12 and 3.13.

## Controlled development sample
- 13 source-linked researcher-paraphrased records in 5+ topical families.
- **24** distinct developer-authored base question *templates*; **72 correlated old/new Latin and Cyrillic variants**.
- **7** no-evidence base question templates = **21** correlated negative variants.
- Operative-rule versus published-document retrieval intents are separately annotated.
- Time filter retains 2–13 eligible documents per variant (mean **6.583**); **zero single-eligible-document queries**. This reduces one former triviality but does not establish natural corpus realism.

## Diagnostic metrics (not validation)

| Method | Hit@1 | Recall@3 | MRR@3 | False answer when no evidence | Invalid top-1 temporal evidence |
| --- | ---: | ---: | ---: | ---: | ---: |
| Raw BM25 | 38/72 (52.78%) | 48/72 (66.67%) | 0.5903 | 20/21 (95.24%) | 20/72 (27.78%) |
| Normalized BM25 | 42/72 (58.33%) | 51/72 (70.83%) | 0.6435 | 21/21 (100%) | 18/72 (25.00%) |
| Normalized char-trigram | 42/72 (58.33%) | 51/72 (70.83%) | 0.6458 | 21/21 (100%) | 18/72 (25.00%) |
| Raw BM25 + operative-time filter | 46/72 (63.89%) | 51/72 (70.83%) | 0.6690 | 18/21 (85.71%) | 0/72 (0%) |
| Normalized BM25 + operative-time filter | 48/72 (66.67%) | 51/72 (70.83%) | 0.6852 | 21/21 (100%) | 0/72 (0%) |

The denominator **72** is not 72 independent questions, because each of 24 question groups has three correlated orthographic variants. Any standard CI computed over 72 individual rows would be overly optimistic; even grouped intervals remain untrustworthy due to developer-selected corpus and related document families.

## Falsifiable conclusions from these engineering checks

1. Under the supplied metadata, the strict time filter prevents invalid-date top-1 selection while the raw lexical baseline often chooses an inapplicable passage. This is a **fixture-specific software boundary**, not a population effect.
2. Abstention remains a major weakness: the leading normalized+time configuration returns **unsupported top-1 passages in all 21 no-evidence variants**. Date-filtering and answerability are distinct.
3. Removing retrospective information from old-source summaries reduced **future-information leakage**, but source metadata and text still require historical legal review.
4. 101 passing software tests do not constitute independent empirical legal evidence or a trained AI model.

## Incomplete research gates
- [ ] Independently verify source *clause-level* evidence and applicability intervals, not just document URLs.
- [ ] Annotate and adjudicate human-created question groups without knowing model predictions.
- [ ] Human-validate new-Latin transformations and Cyrillic equivalents.
- [ ] Freeze a **held-out** legal-document-family split; report uncertainty at family level.
- [ ] Develop and test abstention on a separate calibration/test partition; avoid threshold tuning on the evaluation set.
- [ ] Report failures even where better baselines score lower.
- [ ] Confirm the ZFTI–2026 venue accepts a preliminary methodological feasibility pilot rather than a completed empirical benchmark.

**Conference paper category, if submitted:** *Preliminary methodological pilot and reproducible failure analysis*. Do not call it a trained AI model or a validated high-performing Uzbek legal QA system.
