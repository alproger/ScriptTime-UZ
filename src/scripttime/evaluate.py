"""Evaluate manually reviewed corpora; demo data is only for smoke tests."""
import csv
import json
from collections import defaultdict
from pathlib import Path
from .retrieval import Evidence, rank

METHODS = ("bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time")


def load_data(doc_path, query_path):
    docs = [Evidence.from_dict(json.loads(s)) for s in Path(doc_path).read_text(encoding="utf8").splitlines() if s.strip()]
    with open(query_path, encoding="utf-8", newline="") as f:
        queries = list(csv.DictReader(f))
    if len({d.doc_id for d in docs}) != len(docs):
        raise ValueError("Duplicate document IDs")
    for q in queries:
        if not q.get("gold_doc_id") or not q.get("question_id"):
            raise ValueError("Missing gold ID or question-group ID")
        if q['gold_doc_id'] not in {d.doc_id for d in docs}:
            raise ValueError("Gold ID not present in corpus: " + q['gold_doc_id'])
    return docs, queries


def evaluate(docs, questions, methods=METHODS):
    rows = []
    for q in questions:
        for method in methods:
            predicted = rank(q['query'], docs, method, as_of=q['as_of'], known_at=q['known_at'], k=3)
            ids = [doc.doc_id for doc, _ in predicted]
            gold = q['gold_doc_id']
            rows.append(dict(method=method, question_id=q['question_id'], script=q['script'],
                gold=gold, top1=ids[0] if ids else "",
                hit1=int(bool(ids) and ids[0] == gold),
                recall3=int(gold in ids),
                rr=(1.0/(ids.index(gold)+1) if gold in ids else 0.0)))
    return rows


def summary(rows):
    by = defaultdict(list)
    for row in rows:
        by[row['method']].append(row)
    return {method: {"n_query_variants": len(records),
        "n_independent_question_groups": len(set(r['question_id'] for r in records)),
        "hit_at_1": round(sum(r['hit1'] for r in records)/len(records), 4),
        "recall_at_3": round(sum(r['recall3'] for r in records)/len(records), 4),
        "mrr_at_3": round(sum(r['rr'] for r in records)/len(records), 4)}
        for method, records in by.items()}
