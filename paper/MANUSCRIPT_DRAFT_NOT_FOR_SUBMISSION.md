# ScriptTime-UZ: A Controlled Study of Orthographic and Temporal Reliability in Uzbek Regulatory Retrieval

**Yakhyokhon Kodirov** — Software Engineer, Presidential School in Fergana, Uzbekistan  
ORCID: https://orcid.org/0009-0003-5930-8827

> WORKING DRAFT. NOT A COMPLETED CONFERENCE PAPER. No empirical finding is claimed below.

## Abstract (proposed study)
Retrieving legally applicable evidence is challenging when both the written form of a question and the effective status of a regulation change over time. Uzbekistan's 2026 Latin-alphabet reform provides a case in which enactment precedes entry into force. We propose ScriptTime-UZ, an audit-oriented evaluation protocol that separates orthographic mismatch from legal time-validity mismatch in Uzbek regulatory retrieval. The planned comparisons include BM25, normalized BM25, normalized character n-grams and metadata-aware validity filtering. Future source-traceable evaluation will link original legal versions to clause-level effective dates and independent human-reviewed question groups with controlled script variants. We propose time-valid Hit@1, Recall@3, MRR@3 and clustered confidence intervals. The current implementation contains only a tiny development corpus and nine software tests; it cannot support publishable generalization. This is a proposed empirical evaluation setting, not a newly invented general-purpose AI model.

**Keywords:** Uzbek NLP, orthographic normalization, temporal validity, regulatory retrieval, low-resource languages.

## Introduction
A regulation can be discoverable before it enters into force. Overlapping amendments can look semantically similar, while users may ask about different historical dates. In Uzbek, an additional difficulty is the coexistence of old Latin, new Latin and Cyrillic writing. The question is not whether transliteration works, but whether it helps retrieve the **correct historically applicable evidence**, and whether a time filter changes the result.

## Related work
Nam et al. (2026) propose TimelyRAG for version-evolving documents, motivating effective-time reasoning. Kang et al. (2026) present R-GDA for domain-specific named-entity recognition, motivating controlled quality checks on automatically generated text; our method is NOT R-GDA. Adxamov (2026) already studies hybrid Uzbek regulatory RAG; we do not claim first use of Uzbek RAG, BM25, normalization or hybrid search. The proposed gap is an independently audited interaction study of script conditions and validity dates.

## Methods (planned)
Build source-grounded, human-reviewed gold clause records from 10+ independent legal document families; 30+ clause versions; 60+ independently authored questions, then validated script variants. Distinguish as-of date, evidence known-at date and clause effective interval. Compare raw and normalized BM25, normalized character trigrams and with/without a validity filter. Keep entire question families and document-amendment families in the same data partition. Use confidence intervals clustered by question or legal family.

## Preliminary implementation
Three researcher-written source-linked summaries, three independent questions and nine script variants exist for smoke testing. The baseline CLI and nine unit tests run locally. These records are not a validated legal benchmark and cannot establish accuracy claims for the application domain.

## Ethics and limitations
Legal validity cannot always be modeled with one time interval: some rules are conditional, retroactive, or clause-specific. Orthographic normalization is lossy. Official legal quotations and bulk redistributions require rights verification. A future Toolbase research demo must present citations and uncertainty, not legal advice.

## Conclusion (provisional)
The contribution so far is a transparent research protocol and reproducible prototype. Empirical research claims require independent source annotation and held-out experiments.

## References
1. Uzbekistan, Law No. 931-XII (1993). https://lex.uz/docs/-112286
2. Uzbekistan, Law O‘RQ-1184 (2026). https://lex.uz/docs/8548754
3. Nam et al. (2026). *TimelyRAG*. Findings of EMNLP. https://aclanthology.org/2026.findings-emnlp.398/
4. Kang et al. (2026). *R-GDA*. Findings of EACL. https://aclanthology.org/2026.findings-eacl.259/
5. Adxamov (2026). *A Hybrid Search-Based RAG Approach for a Question-Answering System on Regulatory Documents in Uzbek*. https://innovativepublication.uz/index.php/jelsi/article/view/6287
