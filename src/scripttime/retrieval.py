"""Transparent, dependency-free baselines for version-aware passage retrieval."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import log
from collections import Counter
from .normalize import normalize, tokens

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


def valid_at(record: Evidence, as_of: str, known_at: str) -> bool:
    """Metadata validity filter. Study intervals may be clipped to study window."""
    for value in (as_of, known_at, record.study_valid_from, record.available_from):
        date.fromisoformat(value)
    if record.study_valid_to:
        date.fromisoformat(record.study_valid_to)
    return (record.available_from <= known_at and
            record.study_valid_from <= as_of and
            (record.study_valid_to is None or as_of < record.study_valid_to))


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
        s = normalize(s).replace(' ', '_')
        return set(s[i:i+3] for i in range(max(0, len(s)-2)))
    qg = ngrams(query)
    result = []
    for doc in documents:
        dg = ngrams(doc)
        result.append(len(qg & dg) / max(len(qg | dg), 1))
    return result


def rank(query: str, records: list[Evidence], method: str = "bm25", *,
         as_of: str | None = None, known_at: str | None = None, k: int = 5):
    """Rank with optional time filter. This is NOT TimelyRAG."""
    if method not in {"bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time"}:
        raise ValueError(f"Unknown method: {method}")
    if method in {"bm25_time", "bm25_norm_time"}:
        if not (as_of and known_at):
            raise ValueError("Time-aware method requires as_of AND known_at")
        records = [r for r in records if valid_at(r, as_of, known_at)]
    texts = [r.title + " " + r.text for r in records]
    if method in {"bm25", "bm25_time"}:
        scores = bm25_score(query, texts)
    elif method == "char3_norm":
        scores = trigram_score(query, texts)
    else:
        scores = bm25_score(query, texts, normal=True)
    return sorted(zip(records, scores), key=lambda p: (-p[1], p[0].doc_id))[:k]
