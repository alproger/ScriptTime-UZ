# ScriptTime-UZ review & experiment freeze protocol, 27–29 October 2026

## Deliverables and decision gates

**27 October** — 30 author-review candidate questions in five domains; compile cited source registry; establish machine-readable status tracking; no invented gold. Author reviews issue comments.

**28 October** — adjudicate disputed questions; verify dated legal snapshots at paragraph/clause level; gather multiple *hard negative* documents simultaneously valid so filtering does not trivially leave one answer; freeze evaluation configuration; generate script variants and review semantic equivalence.

**29 October** — run five baselines and report top-1 retrieval, Recall@3, MRR@3, temporal-invalid selection rate, corpus size, independent question count, uncertainty, and explicit failures; draft results and IMRAD only from true reproducible runs; verify references and consent; **submit only if venue accepts and honest evidence is sufficient**.

### Minimum defensible pilot gate
- >= 5 independent document families represented
- >= 20 human-reviewed base questions, with several genuinely ambiguous temporal boundaries
- >= 10 validated evidence spans/versions rather than document titles alone
- >= 1 held-out independent question cluster, explicit confidence caveat (tiny n)
- >= 5 baseline methods including *no* time filter and *with* time filter
- clear ablations normalizing vs not, time constraint vs not
- no unsupported trained-model claim or invented improvement
- source provenance, AI-use disclosure as required by venue

### What is NOT ready yet
- 30 candidate questions are NOT human approved
- model fine-tuning not performed
- paper's Results section has no real held-out metrics
- no independent peer review, DOI or acceptance
- Toolbase production deployment not performed

**Key ethical constraint:** training data and authored evaluation must not leak exact questions into test. This initial question pool is a reviewer exercise; it is not held-out.
