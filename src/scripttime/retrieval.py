"""Transparent, dependency-free baselines for version-aware retrieval.

Two retrieval questions MUST NOT be conflated:
- operative_rule: evidence legally applicable at as_of AND published by known_at
- published_document: evidence already published by known_at, whether or not effective

These are simple metadata predicates, NOT TimelyRAG or legal semantic reasoning.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import log
from collections import Counter
from .normalize import normalize, tokens

METHODS = frozenset({"bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time"})
EVIDENCE_MODES = frozenset({"operative_rule", "published_document"})

@dataclass(frozen=True)
class Evidence:
    doc_id: str
    family_id: str
    title: str
    text: str
    source_url: str
    issued_on: str
    available_from: str
    study_valid_from: str
    study_valid_to: str | None = None
    provenance: str = "researcher_paraphrase_of_official_record"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


def published_by(record: Evidence, known_at: str) -> bool:
    """Information availability, independent of the law's entry into force."""
    return date.fromisoformat(record.available_from) <= date.fromisoformat(known_at)


def valid_at(record: Evidence, as_of: str, known_at: str) -> bool:
    """Operative rule at a date, with a separate evidence-availability cutoff.

    Important: study_valid_from may be the *first audited snapshot*, not a
    historically complete beginning of a regulation. This is NOT legal advice.
    """
    when = date.fromisoformat(as_of)
    start = date.fromisoformat(record.study_valid_from)
    end = date.fromisoformat(record.study_valid_to) if record.study_valid_to else None
    return published_by(record, known_at) and start <= when and (end is None or when < end)


def bm25_score(query: str, documents: list[str], *, normal: bool = False) -> list[float]:
    if not documents:
        return []
    q = set(tokens(query, normalize_first=normal))
    d_toks = [tokens(doc, normalize_first=normal) for doc in documents]
    n = len(documents)
    df = Counter(term for doc in d_toks for term in set(doc))
    avgdl = sum(len(doc) for doc in d_toks) / n or 1.0
    k1, b = 1.5, 0.75
    scores = []
    for dt in d_toks:
        tf = Counter(dt)
        score = 0.0
        for term in q:
            if not tf[term]:
                continue
            idf = log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + k1 * (1 - b + b * len(dt) / avgdl)
            score += idf * tf[term] * (k1 + 1) / denom
        scores.append(score)
    return scores


def trigram_score(query: str, documents: list[str]) -> list[float]:
    def ngrams(s):
        s = normalize(s).replace(" ", "_")
        return set(s[i:i+3] for i in range(max(0, len(s)-2)))
    qg = ngrams(query)
    results = []
    for doc in documents:
        dg = ngrams(doc)
        results.append(len(qg & dg) / max(len(qg | dg), 1))
    return results


def rank(query: str, records: list[Evidence], method: str = "bm25", *,
         as_of: str | None = None, known_at: str | None = None, k: int = 5,
         evidence_mode: str = "operative_rule", min_score: float = 0.0):
    """Rank relevant evidence under an explicit temporal intent.

    For fair comparison, **every** method respects known_at when supplied.
    Only *_time methods enforce legal operative-time validity, and only for
    operative_rule queries. published_document explicitly permits finding
    announced but not-yet-effective laws.

    A nonpositive lexical score is not evidence: no match => empty list.
    This still is not confidence-calibrated legal abstention.
    """
    if method not in METHODS:
        raise ValueError(f"Unknown method: {method}")
    if evidence_mode not in EVIDENCE_MODES:
        raise ValueError(f"Unknown evidence mode: {evidence_mode}")
    if k < 1:
        raise ValueError("k must be >= 1")
    time_aware = method in {"bm25_time", "bm25_norm_time"}
    if time_aware and known_at is None:
        raise ValueError("Time-aware method requires known_at")
    if time_aware and evidence_mode == "operative_rule" and as_of is None:
        raise ValueError("Operative-rule retrieval requires as_of AND known_at")
    if known_at is not None:
        records = [r for r in records if published_by(r, known_at)]
    if time_aware and evidence_mode == "operative_rule":
        records = [r for r in records if valid_at(r, as_of, known_at)]
    texts = [r.title + " " + r.text for r in records]
    if method in {"bm25", "bm25_time"}:
        scores = bm25_score(query, texts)
    elif method == "char3_norm":
        scores = trigram_score(query, texts)
    else:
        scores = bm25_score(query, texts, normal=True)
    matched = [(record, score) for record, score in zip(records, scores) if score > min_score]
    return sorted(matched, key=lambda p: (-p[1], p[0].doc_id))[:k]
