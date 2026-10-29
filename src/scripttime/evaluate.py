"""Source-aware retrieval evaluation with explicit no-answer and time-validity checks.

Author-created toy questions are *development* diagnostics, never independent
human-reviewed benchmark evidence.
"""
from __future__ import annotations
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from .retrieval import Evidence, rank, valid_at, published_by

METHODS = ("bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time")
SCRIPTS = {"old_latin", "new_latin", "cyrillic"}

def _true(value):
    return str(value).strip().lower() in {"1", "true", "yes"}

def load_data(doc_path, query_path):
    docs = [Evidence.from_dict(json.loads(s))
            for s in Path(doc_path).read_text(encoding="utf8").splitlines() if s.strip()]
    with open(query_path, encoding="utf-8", newline="") as f:
        queries = list(csv.DictReader(f))
    if not docs or not queries:
        raise ValueError("Documents and queries must not be empty")
    if len({d.doc_id for d in docs}) != len(docs):
        raise ValueError("Duplicate document IDs")
    ids = {d.doc_id for d in docs}
    for d in docs:
        for field in ("issued_on", "available_from", "study_valid_from"):
            date.fromisoformat(getattr(d, field))
        if d.study_valid_to:
            if date.fromisoformat(d.study_valid_to) <= date.fromisoformat(d.study_valid_from):
                raise ValueError("Empty or backwards study interval: " + d.doc_id)
    observed = set()
    by_group = defaultdict(set)
    for q in queries:
        for field in ("question_id", "script", "query", "as_of", "known_at"):
            if not (q.get(field) or "").strip():
                raise ValueError("Missing query field: " + field)
        if q["script"] not in SCRIPTS:
            raise ValueError("Unknown script: " + q["script"])
        date.fromisoformat(q["as_of"])
        date.fromisoformat(q["known_at"])
        key = (q["question_id"], q["script"])
        if key in observed:
            raise ValueError("Duplicate question and script: " + str(key))
        observed.add(key)
        gold = (q.get("gold_doc_id") or "").strip()
        abstain = _true(q.get("needs_abstention"))
        if abstain and gold:
            raise ValueError("Abstention question must have blank gold_doc_id")
        if not abstain and gold not in ids:
            raise ValueError("Gold ID missing from corpus: " + gold)
        mode = q.get("evidence_mode") or "operative_rule"
        if mode not in ("operative_rule", "published_document"):
            raise ValueError("Invalid evidence mode")
        by_group[q["question_id"]].add((gold, abstain, q["as_of"], q["known_at"], mode))
        q["needs_abstention"] = "1" if abstain else "0"
    if any(len(values) != 1 for values in by_group.values()):
        raise ValueError("Orthographic variants disagree on temporal target or gold")
    return docs, queries

def evaluate(docs, questions, methods=METHODS):
    rows = []
    by_id = {d.doc_id: d for d in docs}
    for q in questions:
        expected_none = _true(q.get("needs_abstention"))
        gold = (q.get("gold_doc_id") or "").strip()
        mode = q.get("evidence_mode") or "operative_rule"
        for method in methods:
            predicted = rank(q["query"], docs, method,
                             as_of=q["as_of"], known_at=q["known_at"],
                             evidence_mode=mode, k=3)
            ids = [doc.doc_id for doc, _ in predicted]
            top1 = ids[0] if ids else ""
            abstained = not ids
            correct = int(abstained if expected_none else top1 == gold)
            if expected_none:
                recall = int(abstained)
                rr = float(abstained)
            else:
                recall = int(gold in ids)
                rr = (1.0 / (ids.index(gold) + 1)) if gold in ids else 0.0
            invalid = 0
            if top1:
                record = by_id[top1]
                if not published_by(record, q["known_at"]):
                    invalid = 1
                elif mode == "operative_rule" and not valid_at(record, q["as_of"], q["known_at"]):
                    invalid = 1
            rows.append(dict(
                method=method, question_id=q["question_id"], script=q["script"],
                evidence_mode=mode, as_of=q["as_of"], known_at=q["known_at"],
                gold=gold, needs_abstention=int(expected_none), top1=top1,
                hit1=correct, recall3=recall, rr=rr,
                abstained=int(abstained), false_answer=int(expected_none and not abstained),
                invalid_top1=invalid,
            ))
    return rows

def summary(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["method"]].append(r)
    result = {}
    for method, records in by.items():
        n = len(records)
        negatives = [r for r in records if r["needs_abstention"]]
        result[method] = {
            "n_query_variants": n,
            "n_independent_question_groups": len({r["question_id"] for r in records}),
            "n_abstention_variants": len(negatives),
            "hit_at_1": round(sum(r["hit1"] for r in records)/n, 4),
            "recall_at_3": round(sum(r["recall3"] for r in records)/n, 4),
            "mrr_at_3": round(sum(r["rr"] for r in records)/n, 4),
            "false_answer_on_unanswerable": round(
                sum(r["false_answer"] for r in negatives)/len(negatives), 4) if negatives else None,
            "invalid_time_or_publication_top1_rate": round(
                sum(r["invalid_top1"] for r in records)/n, 4),
        }
    return result

def candidate_difficulty(docs, questions):
    """Audit filter triviality independently of lexical rank quality."""
    result = []
    for q in questions:
        mode = q.get("evidence_mode") or "operative_rule"
        eligible = [d for d in docs if published_by(d, q["known_at"])
                    and (mode == "published_document" or valid_at(d, q["as_of"], q["known_at"]))]
        result.append({
            "question_id": q["question_id"],
            "script": q["script"],
            "eligible_documents": len(eligible),
            "is_single_candidate": len(eligible) == 1,
            "no_eligible_documents": len(eligible) == 0,
        })
    return result
