"""Cluster-aware exploratory analysis; NEVER interpret demo bootstrap as generalization.

Resampling *question groups* (all orthographic variants together) avoids the
most obvious pseudoreplication. It does not fix small sample sizes, source-family
correlation, author-created labels, training leakage or selection bias.
"""
from __future__ import annotations

from collections import defaultdict
from random import Random


def grouped_accuracy(rows: list[dict], *, metric: str = "hit1") -> dict[str, dict[str, float]]:
    """Method -> question_id -> average across correlated script variants.

    Raises on duplicate (method, question_id, script) tuples to avoid silently
    counting duplicated trials. Every question group contributes one value.
    """
    if metric not in {"hit1", "recall3", "rr"}:
        raise ValueError("Unknown metric")
    cells = defaultdict(list)
    seen = set()
    for row in rows:
        key = (row["method"], row["question_id"], row["script"])
        if key in seen:
            raise ValueError(f"Duplicate method/question/script: {key}")
        seen.add(key)
        cells[(row["method"], row["question_id"])].append(float(row[metric]))
    result: dict[str, dict[str, float]] = defaultdict(dict)
    for (method, group), values in cells.items():
        result[method][group] = sum(values) / len(values)
    return dict(result)


def _percentile(sorted_values, p):
    if not sorted_values:
        raise ValueError("Empty bootstrap")
    idx = (len(sorted_values) - 1) * p
    low = int(idx)
    high = min(low + 1, len(sorted_values) - 1)
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * (idx - low)


def paired_question_bootstrap(rows: list[dict], *, baseline: str, candidate: str,
                              metric: str = "hit1", resamples: int = 2000,
                              seed: int = 2026) -> dict:
    """Exploratory, paired percentile bootstrap over independent question groups.

    The confidence interval is NOT a publication-grade inferential guarantee:
    shared document families make even question groups correlated. Validate
    independence and account for document-family nesting in a larger dataset.
    """
    if resamples < 100:
        raise ValueError("Use >= 100 bootstrap resamples")
    grouped = grouped_accuracy(rows, metric=metric)
    if baseline not in grouped or candidate not in grouped:
        raise ValueError("Both methods must be present")
    base, cand = grouped[baseline], grouped[candidate]
    if set(base) != set(cand):
        raise ValueError("Paired methods must be evaluated on identical question groups")
    groups = sorted(base)
    if len(groups) < 2:
        raise ValueError("Need at least two question groups")
    differences = [cand[g] - base[g] for g in groups]
    rng = Random(seed)
    samples = []
    for _ in range(resamples):
        samples.append(sum(differences[rng.randrange(len(differences))] for _ in groups) / len(groups))
    samples.sort()
    return {
        "metric": metric,
        "baseline": baseline,
        "candidate": candidate,
        "n_question_groups": len(groups),
        "mean_paired_difference": round(sum(differences)/len(differences), 6),
        "percentile_ci_95": [round(_percentile(samples, .025), 6),
                             round(_percentile(samples, .975), 6)],
        "seed": seed,
        "resamples": resamples,
        "status": "DEVELOPMENT_DIAGNOSTIC_NOT_INDEPENDENT_SCIENTIFIC_RESULT",
        "limitations": "Question-family bootstrap only; source-family dependence, tiny n, author drafted queries, unverified labels and training leakage remain.",
    }
