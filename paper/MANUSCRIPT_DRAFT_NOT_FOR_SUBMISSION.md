# ScriptTime-UZ: A Reproducible Protocol for Studying Orthographic Variation and Temporal Evidence Validity in Uzbek Document Retrieval

**Yakhyokhon Kodirov**  
Software Engineer, Presidential School in Fergana, Uzbekistan  
ORCID: https://orcid.org/0009-0003-5930-8827

**Manuscript revision:** 28 October 2026  
**Status:** *Research-in-progress manuscript. NOT approved for conference submission.*  
**Research area:** Natural language processing; information retrieval; evidence provenance; low-resource languages.

> **Publication gate.** This manuscript describes implemented infrastructure and exploratory engineering tests. Its **main empirical results are not yet available**, because the corpus and candidate questions have not undergone independent review and held-out evaluation. In particular, no trained encoder model or generalizable performance improvement is claimed. Do not replace this warning with a statement of acceptance, DOI, indexing, or model training.

## Abstract

Document retrieval may fail when a user refers to a historical version of a regulation while using a writing system different from that of the source. Uzbek presents a relevant research setting because Cyrillic, established Latin forms, and proposed revised Latin forms may coexist in queries and archived text. A second complication is temporal: the date on which a law becomes publicly discoverable can precede the date on which its provisions become legally operative. This paper proposes **ScriptTime-UZ**, a transparent protocol for jointly evaluating orthographic variation and time-dependent evidence selection in Uzbek regulatory documents. A reproducible prototype implements lexical BM25, conservative script normalization, character n-gram matching, and metadata-based temporal filtering. It also distinguishes two retrieval intents: identifying a **published document** and identifying a **currently applicable rule**. We specify version-level source provenance, independent-question grouping, cross-script equivalence review, and error analysis. Early engineering tests demonstrate the feasibility of exercising these components but are too small and author-constructed to establish domain-level accuracy or improvement. The intended contribution is an auditable evaluation protocol and, subject to independent annotation, an Uzbek cross-script temporal retrieval benchmark, rather than a new retrieval architecture.

**Keywords:** Uzbek NLP; information retrieval; orthographic variation; Cyrillic and Latin scripts; temporal validity; evidence provenance; regulatory documents.

## 1. Introduction

Search systems frequently rank passages by lexical or semantic overlap. For historical regulations, a textually relevant passage can still be the **wrong evidence** if it belongs to a version that was not applicable on the date requested. This problem is compounded when a question is written in a different script or spelling convention than the underlying documents. The relevant scientific question is therefore not simply whether a normalized word can be found: it is whether evidence remains correct under the **joint perturbation of writing system and temporal interpretation**.

Uzbek provides a motivating case. Law O‘RQ–1184 of 21 October 2026 revises the Latin-based alphabet and is listed as entering into force on 22 April 2027 [1]. A query issued in October 2026 about **when the future law will enter into force** must be able to retrieve the already published law. A different query asking **which alphabet rule was operative in October 2026** must not treat its future provisions as then effective. This distinction also prevents the mistaken implication that an existing document automatically loses legal force because of an older spelling form; Article 2 of the law contains a transitional provision on existing documents [1].

A second source example concerns Annex 3a, clause 3, of Cabinet of Ministers Resolution No. 214. The November 2025 edition describes two classes of 24 students each, whereas the edition effective in July 2026 differentiates grades 1–4 (12 students per class) and grades 5–11 (24 per class) [2,3]. The example relates to the foreign-language-specialized boarding school, **not** Presidential-school admissions. These are useful version-confusable records but do not constitute independent evidence that a retrieval method generalizes.

This work asks:

- **RQ1.** How does conservative cross-script normalization change lexical retrieval under Uzbek Cyrillic, established Latin, and proposed revised Latin queries?
- **RQ2.** How does filtering by rule applicability affect retrieval of the correct historical document version compared with lexical ranking alone?
- **RQ3.** What changes when questions about **published documents** are differentiated from questions about **operative provisions**?
- **RQ4.** Which errors remain when multiple same-time, topically similar passages compete, and what claims survive independent annotation and grouped uncertainty analysis?

Only the research protocol and engineering prototypes are presently complete. RQ1–RQ4 require a larger, human-reviewed holdout before scientific conclusions can be drawn.

## 2. Related Work and Research Gap

**Temporal retrieval.** Nam et al. introduce *TimelyRAG*, which addresses temporally relevant retrieval for overlapping-evolving documents, including regulations with amendments that override some clauses while preserving others [4]. It reports gains using temporal distance in ranking and introduces TimelyQABench. We neither implement nor replicate TimelyRAG; in particular, a simple metadata filter is **not a novel temporal retrieval algorithm**. The relevant gap worth testing is how time-dependent evidence accuracy interacts with **Uzbek cross-script variation** and explicit information intent.

**Uzbek regulatory question answering.** Adxamov describes an Uzbek regulatory RAG approach combining BM25 and multilingual dense retrieval, with preprocessing for Uzbek morphology, Latin/Cyrillic variation and apostrophes [5]. Therefore, this manuscript does not claim first use of Uzbek legal RAG, hybrid retrieval, or Cyrillic–Latin normalization. The proposed differentiator is a source-audited, version-sensitive evaluation design with explicit applicability and publication conditions.

**Data quality.** Kang et al. propose *R-GDA*, a feedback-driven augmentation method for domain-specific named-entity recognition [6]. This concerns **NER**, not retrieval, so it is not a retrieval baseline. It motivates human checks on label fidelity and on whether generated cross-script questions preserve the same proposition. We do not reproduce its architecture or report its results as our own.

These sources establish a useful methodological direction, not evidence of novelty or superiority. A full systematic novelty review and external baseline comparison remain open.

## 3. Materials and Methods

### 3.1 Evidence model

Each evidence record stores a stable identifier, document family, original title, source URL, available-from date, a studied validity interval, and provenance. It is crucial not to confuse:

- **known_at:** the latest date on which published information is available to the system;
- **as_of:** the date about which the user asks;
- **available_from:** first documented availability of an evidence record;
- **study_valid_from / study_valid_to:** the interval for which the record is treated as applicable in the *current test case*.

The latter may begin at the first historically audited snapshot rather than at a provision's true original entry into force. This limitation is documented in the dataset card; a scientifically validated dataset must replace study-window approximations with audited clause-level effectiveness ranges.

### 3.2 Two retrieval intents

We distinguish **published_document**, which retrieves records available by known_at regardless of whether their operative date has arrived, from **operative_rule**, which also enforces applicability at as_of. An explicit parameter selects the intent; this is **not an automatic or trained query-intent classifier**. Mistaken query intent can itself cause incorrect answers and should be measured independently in future work.

For an operative query about date t with knowledge cutoff k, the eligibility predicate is:

\[
Eligible_{operative}(d,t,k)=\mathbb{1}(available(d)\leq k)\,\mathbb{1}(validFrom(d)\leq t<validTo(d)).
\]

For published-document discovery:

\[
Eligible_{published}(d,k)=\mathbb{1}(available(d)\leq k).
\]

Here the terminal interval is treated as open when no end date is known in the toy implementation; **unknown is not the same as legally indefinite**. Complex transitional, retroactive, and clause-specific rules are not modeled by these predicates.

### 3.3 Retrieval baselines

The implementation exposes five configurations: (1) raw BM25, (2) normalized BM25, (3) normalized character trigrams, (4) raw BM25 with operative-time filtering, and (5) normalized BM25 with operative-time filtering. All methods can respect a shared known_at publication cutoff. BM25 uses simple lexical frequency and length normalization; normalized methods map selected Unicode apostrophe and script variants to a common representation. The normalizer is a **lossy research heuristic, not an official transliteration standard**.

The prototype ranks source-linked paraphrases; it does not run a generative LLM, dense reranker, or fine-tuned encoder. Retrieval scores are not probabilities and no calibrated abstention is implemented. Empty retrieval when lexical overlap is zero is only a basic safety guard.

### 3.4 Current data and planned annotation

There are three distinct groups of **development data**:

1. A minimal three-record seed corpus with three independent base questions and nine script variants.
2. A two-edition Annex 3a quota corpus, four base questions and twelve script variants.
3. A mixed-domain corpus, nine source-linked researcher-paraphrased records covering five document families, eight base questions and twenty-four script variants.

These sets are **not additive independent samples**; questions and underlying documents can overlap. The project also contains a pool of **30 candidate questions** spanning five areas (alphabet, labor, water, school admissions and school governance), stored with official source links and review status. As checked on 28 October 2026, **zero of the 30 questions have been marked author-verified**. Their expected answers cannot yet be treated as independently established gold labels.

For a defensible pilot, the intended workflow is to locate and verify the actual relevant legal version and clause, annotate original excerpts or limited rights-compliant evidence spans, validate historical dates, have a second person resolve disagreements when possible, and produce a separate unseen question group set. Related orthographic variants must never be split across training and test as if independent observations. Where feasible, a document-family-held-out split is preferable.

### 3.5 Evaluation plan

Predeclared primary outcomes are Hit@1 for exact verified evidence, Recall@3, MRR@3 and the proportion of top-ranked answers that refer to an inapplicable version. Results should be stratified by script and by retrieval intent.

Uncertainty estimation should resample **original question groups**, keeping all three script variants together. The repository implements exploratory paired percentile bootstrap diagnostics with a fixed pseudorandom seed. Small group counts and correlation between questions from the same legal family make such intervals unreliable as evidence of population-level improvement. A broader study should use family-aware resampling and error taxonomies, including wrong version, wrong document family, publication leakage, premature effectiveness, script normalization failure, and inadequate evidence.

## 4. Engineering Verification (Not Empirical Research Findings)

The Python implementation and automation are operational. At the recorded source revision, continuous integration ran **40 automated software tests successfully on Python 3.10, 3.12 and 3.13**. These tests establish reproducible code behavior under specified fixtures; they do not establish real-world retrieval validity.

A deliberately constructed mixed-domain smoke test produced the following **development diagnostics**:

| Baseline | Hit@1 across 24 correlated script variants | Recall@3 | MRR@3 |
| --- | ---: | ---: | ---: |
| BM25 | 0.7083 | 0.9583 | 0.8333 |
| Normalized BM25 | 0.7500 | 1.0000 | 0.8750 |
| Normalized character trigram | 0.6250 | 1.0000 | 0.8125 |
| BM25 + operative-time filter | 0.9583 | 1.0000 | 0.9722 |
| Normalized BM25 + operative-time filter | 1.0000 | 1.0000 | 1.0000 |

**These are not independent scientific results.** They cover only eight developer-authored base questions, with three correlated writing variants per group. The evidence corpus was chosen while constructing the questions, and some filtered candidate sets are small. Reporting these values as an unbiased accuracy comparison, or using a naive confidence interval over 24 variants, would be misleading. The recorded diagnostics are retained in the repository for transparent development and debugging only.

A separate two-intent test shows that the published-document and operative-rule predicates behave differently on an announced future law. That proves a specific software boundary condition in the test fixture, not a generalizable improvement in retrieval or automatic intent understanding.

## 5. Discussion

Three lessons emerge from code inspection and development verification, **without assuming external validity**.

First, orthographic normalization is useful to test but risks conflating distinct lexical tokens and can introduce errors. It therefore requires balanced script-specific analysis against raw lexical baselines.

Second, temporal appropriateness is not a single label. A law's publication date, a clause's operational validity and the historical date referred to in a user question are logically distinct. Strict filtering alone may provide a misleading success score on a tiny set, or incorrectly exclude a published but future-effective law if the request is about discovery rather than applicability.

Third, dataset provenance is likely to determine the scientific quality of the work. Real amendments can affect only certain provisions; a single document-level validity interval may be inadequate. Validity labels must be traced to authoritative historical versions, and question sets must include genuine hard negatives that remain plausible after basic filtering.

A larger next phase may study a small multilingual embedding encoder, but **no training has been performed**. A fine-tuned model can only support an empirical claim after a separately reviewed training set, leakage-free split, held-out comparison and reproducible training configuration are available.

## 6. Threats to Validity and Ethics

The dominant threats are author-generated question bias, small and dependent samples, incomplete source-version audit, lossy normalizers, easy distractors, assumed publication dates, and optimistic evaluation after method development. There is also a risk of confusing document discoverability with legal applicability. This research prototype must not be offered as professional legal advice. If deployed as a Toolbase research demo, it should display authoritative links, temporal qualifiers, uncertainty and an explicit non-legal-advice notice.

Only rights-compatible public source excerpts or researcher paraphrases should be distributed. School/student private records and user-uploaded Toolbase documents should not be incorporated without a legitimate basis and explicit authorization. Any significant AI assistance in drafting, annotation or analysis must be disclosed according to venue policy.

## 7. Conclusion and Required Next Evidence

ScriptTime-UZ currently provides a reproducible open-source **engineering prototype and evaluation protocol** for distinguishing script mismatch from temporal mismatches in Uzbek regulatory retrieval. Its source-linked development cases motivate a meaningful research question, but **do not yet support a publishable claim of better retrieval accuracy**. The immediate scientific priority is independent verification of dated clause versions and answers, creation of a genuinely held-out test set with several simultaneously plausible documents, and transparent error analysis. Only after that audit should an empirical conference Results section and quantitative conclusions be finalized.

## References

[1] Republic of Uzbekistan. (2026). *Law O‘RQ–1184, 21 October 2026: Amendment to the law on adoption of the Uzbek Latin alphabet*. Official legislative database. https://lex.uz/uz/docs/8548754

[2] Cabinet of Ministers of Uzbekistan. (2023, with amendments). *Resolution No. 214, 27 May 2023, Annex 3a*, historical versions dated 26 November 2025 and 3 July 2026. https://lex.uz/uz/docs/-6479366?ONDATE=26.11.2025 ; https://lex.uz/uz/docs/-6479366?ONDATE=03.07.2026

[3] Cabinet of Ministers of Uzbekistan. (2026). *Resolution No. 353, 30 June 2026, concerning amendments including Annex 3a clause 3*. https://lex.uz/uz/docs/-8306415?ONDATE=03.07.2026

[4] Nam, Y., Kim, J., Song, H., Yoon, S., Lee, J.-G., & Lee, B. S. (2026). *TimelyRAG: Semantic-Temporal Hybrid Retrieval for Time-Critical Question Answering in Overlapping-Evolving Documents*. Findings of ACL: EMNLP 2026, 8414–8430. https://aclanthology.org/2026.findings-emnlp.398/

[5] Adxamov, D. (2026). *A hybrid search-based RAG approach for a question-answering system on regulatory documents in Uzbek*. Samarali Ta’lim va Barqaror Innovatsiyalar Jurnali, 4(10), 175–182. https://innovativepublication.uz/index.php/jelsi/article/view/6287

[6] Kang, H., Namgoong, H., Pyeon, G., & Jung, S. (2026). *R-GDA: Reflective Guidance Data Augmentation with Multi-Agent Feedback for Domain-Specific Named Entity Recognition*. Findings of ACL: EACL 2026, 4938–4953. https://doi.org/10.18653/v1/2026.findings-eacl.259

---

### Internal pre-submission checklist (remove from final paper)

- [ ] Replace development-only diagnostics with **independent human-reviewed** test outcomes, or obtain permission to submit an explicitly methodological feasibility report.
- [ ] Confirm 30 review questions with the author in GitHub issues #2–#6 and resolve domain/time ambiguities.
- [ ] Validate at least ten legal clause-version evidence spans and enough concurrent hard negatives to prevent trivial filtering.
- [ ] Freeze source Git commit, code, metrics, annotation log and any admissible source excerpts.
- [ ] Format document according to the actual ZFTI–2026 author instructions; add author email and validated affiliation as required.
- [ ] Author personally approves every research claim and any policy-required AI disclosure.
- [ ] Ensure the 29 October target is respected **only if quality conditions are met**. Conference deadlines do not justify fictional results or unverifiable acceptance claims.
