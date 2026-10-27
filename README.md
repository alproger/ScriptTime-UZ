# ScriptTime-UZ

**Cross-script and time-aware retrieval of Uzbek regulatory evidence.**

[![Python tests](https://github.com/alproger/ScriptTime-UZ/actions/workflows/tests.yml/badge.svg)](https://github.com/alproger/ScriptTime-UZ/actions/workflows/tests.yml)

> **Status: early research prototype (27 October 2026).** Not peer reviewed, not legal advice, not a trained AI model. The three-record seed corpus is demonstration data, **not** a publishable benchmark.

## Research problem

Can orthographic normalization and validity-time constraints **jointly** improve the retrieval of historically applicable evidence in low-resource Uzbek? We distinguish the time a rule was **published**, the time a question **asks about**, and the interval in which an individual clause **applies**.

A motivating example is [Uzbekistan's 2026 alphabet law, O‘RQ-1184](https://lex.uz/docs/8548754), published on 2026-10-21 but effective 2027-04-22. The old and new Latin alphabets, Cyrillic and variant apostrophes can all appear in user questions and documents.

## Implemented baselines

| Baseline | Script normalization | Time-aware metadata filter |
| --- | --- | --- |
| BM25 | No | No |
| Normalized BM25 | Yes | No |
| Character trigram | Yes | No |
| BM25 + time | No | Yes |
| Normalized BM25 + time | Yes | Yes |

The time-aware methods currently filter metadata, **not** TimelyRAG-style clause-level temporal reranking. Dense encoder training, abstention, and a larger audited dataset are future work.

## Run

Python 3.10+:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m scripttime evaluate
python -m scripttime query "2027-yil aprelida yangi alifbo" --as-of 2027-04-23 --known-at 2026-10-27
```

**Do not interpret smoke-test accuracy as scientific evidence.** The seed dataset has only 3 source-linked researcher paraphrases, 3 independent questions and 9 script variants.

## Research integrity and next steps

- Create a clause-level, human-audited benchmark from official versioned sources and document annotation decisions.
- Separate base questions and document families across training, development and test sets.
- Evaluate orthographic normalization × temporal validity in paired experiments and report failure cases, confidence intervals and dataset coverage.
- Validate citations and source rights. Do not use Toolbase customer uploads or private data.
- Add a small trained retrieval encoder only if a sufficient source-grounded dataset and honest holdout evaluation exist.

## Papers informing the protocol

- Nam et al. (2026), [TimelyRAG](https://aclanthology.org/2026.findings-emnlp.398/), including Hwanjun Song (KAIST). Temporal relevance in overlapping evolving documents.
- Kang et al. (2026), [R-GDA](https://aclanthology.org/2026.findings-eacl.259/), including Sangkeun Jung (CNU). Human/structured validation of synthetic augmentation. **Its main task is NER, not retrieval.**
- Adxamov (2026), [Hybrid Uzbek regulatory RAG](https://innovativepublication.uz/index.php/jelsi/article/view/6287). Existing overlapping work; Uzbek RAG or Latin–Cyrillic normalization alone is **not** claimed as new.

## Author and independence

Research prototype by **Yakhyokhon Kodirov**, [ORCID 0009-0003-5930-8827](https://orcid.org/0009-0003-5930-8827). Independent research; not affiliated with LexUZ and not an official government information service.

**Caution:** GitHub publication is not conference acceptance. The paper under `paper/` is a draft that must not be submitted until independently verified evidence and results exist.


## Temporal intent correction (2026-10-27)

A law may be **published now but not yet legally in force**. Two different information requests must not use the same filter:

| Request intent | Metadata condition | Example |
| --- | --- | --- |
| `published_document` | `available_from <= known_at` | When will the October 2026 alphabet amendment enter into force? |
| `operative_rule` | `available_from <= known_at` AND `valid_from <= as_of < valid_to` | Which alphabet rule was operative in October 2026? |

This is a baseline **rule-based query-intent parameter**, not a trained classifier. All lexical baselines now respect the same `known_at` availability cutoff when provided. No-positive-match lexical rankings abstain instead of returning arbitrary zero-score evidence; this is **not calibrated confidence**.

```bash
python -m scripttime query "O'RQ-1184 28 harf" --method bm25_norm_time --case seed --as-of 2026-10-27 --known-at 2026-10-27 --evidence-mode published_document
python -m scripttime query "amaldagi o'zbek alifbosi" --method bm25_norm_time --case seed --as-of 2026-10-27 --known-at 2026-10-27 --evidence-mode operative_rule
python -m scripttime evaluate --case intent_boundary
```

Our new `src/scripttime/analysis.py` offers **question-group paired bootstrap diagnostics**. All related script variants stay together; the current small author-prepared samples are still **not a publishable inference dataset**.

See:
- [Temporal intent design](docs/TEMPORAL_INTENT_DESIGN.md)
- [Factorial experiment design and statistical risks](docs/EXPERIMENT_DESIGN_FACTORS.md)
- [Source and research audit, 27 October 2026](docs/RESEARCH_AUDIT_2026-10-27.md)
- [Human-review question pool and issues](docs/REVIEW_GUIDE_UZ.md)
