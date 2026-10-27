# Related work: professors and scientific differentiation

Prepared: 2026-10-27. These papers inform the research design; their authors are not collaborators or endorsers.

## Hwanjun Song — KAIST
Nam et al. (2026), **TimelyRAG: Semantic-Temporal Hybrid Retrieval for Time-Critical Question Answering in Overlapping-Evolving Documents**, Findings of EMNLP 2026.
https://aclanthology.org/2026.findings-emnlp.398/

This work tackles relevant evidence under overlapping, changing document versions and uses richer clause-level temporal logic. **Our prototype does not implement TimelyRAG.** We implement elementary metadata filtering as a transparent baseline. Its findings motivate separating evidence availability from normative applicability. A future Uzbek benchmark may test whether script variation interacts with these temporal constraints. No claims of algorithmic novelty have been established.

## Sangkeun Jung — Chungnam National University
Kang et al. (2026), **R-GDA: Reflective Guidance Data Augmentation with Multi-Agent Feedback for Domain-Specific Named Entity Recognition**, Findings of EACL 2026.
https://aclanthology.org/2026.findings-eacl.259/

The target task is *named-entity recognition*, not regulatory retrieval. The relevant lesson is careful evaluation of synthetic data fidelity and annotation errors. We are NOT reproducing R-GDA or attributing its model to our project.

## Overlapping Uzbek research
Adxamov (2026), **A Hybrid Search-Based RAG Approach for a Question-Answering System on Regulatory Documents in Uzbek**.
https://innovativepublication.uz/index.php/jelsi/article/view/6287

This prior work already considers Uzbek regulatory retrieval and cross-script challenges. Therefore we cannot claim the invention of Uzbek RAG, hybrid retrieval, or Uzbek orthographic normalization. Proposed incremental empirical contribution: independent, human-reviewed tests that combine **script shifts with the effective-time validity of individual rules**.

## Potential professor outreach
Only after peer-checking sources and evaluating on held-out questions:
1. Explain the precise professor paper and how it motivated an experiment.
2. Describe one independently reproduced baseline with genuine numerical result and its uncertainty.
3. Link public code, dataset card and reproducible setup.
4. Ask one focused research-fit question; do not promise affiliation or a positive admissions outcome.
