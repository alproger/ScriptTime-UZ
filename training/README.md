# Small encoder training — planned, NOT done

Aim: a lightweight retrieval encoder that improves cross-script query-to-passage matching under strict train/dev/test family separation.

Preparation: verify 60+ independent queries and many time-labelled clause versions before augmentation; collect positives and carefully selected negative clauses of similar topical wording but different effective intervals.

Potential methods: frozen multilingual sentence embeddings vs parameter-efficient fine-tuning of an appropriately sized encoder with contrastive loss. Version-effective date may require an explicit symbolic filter rather than a model-only shortcut.

Evaluation: document-family-held-out Hit@1, Recall@3, latency and GPU memory; ablate normalization and filtering. Report independent question counts, confidence intervals and negative results.

**There is currently no trained model, checkpoint or fine-tuning metric.** Avoid presenting this as completed research.
