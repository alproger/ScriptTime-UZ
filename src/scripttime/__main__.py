"""Command-line interface for prototype experiments, NOT legal advice."""
import argparse
import json
from pathlib import Path
from .evaluate import load_data, evaluate, summary
from .retrieval import rank

ROOT = Path(__file__).resolve().parents[2]
DATASETS = {
    "seed": ("data/seed/documents.jsonl", "data/seed/queries.csv"),
    "annex3a": ("data/experiments/annex3a_versions.jsonl", "data/experiments/annex3a_candidate_questions.csv"),
    "mixed_temporal": ("data/experiments/mixed_temporal_records.jsonl", "data/experiments/mixed_temporal_queries.csv"),
    "intent_boundary": ("data/seed/documents.jsonl", "data/experiments/intent_boundary_queries.csv"),
    "challenge": ("data/experiments/challenge_records.jsonl", "data/experiments/challenge_queries.csv"),
}
# Backward-compatible paths for original test modules.
DOCS = ROOT / DATASETS["seed"][0]
QUERIES = ROOT / DATASETS["seed"][1]
METHODS = ("bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time")


def report_case(case: str) -> dict:
    docs_path, query_path = DATASETS[case]
    docs, queries = load_data(ROOT / docs_path, ROOT / query_path)
    rows = evaluate(docs, queries)
    errors = [
        {"method": r["method"], "question_id": r["question_id"],
         "script": r["script"], "expected": r["gold"], "retrieved": r["top1"]}
        for r in rows if not r["hit1"]
    ]
    return {
        "case": case,
        "experiment_status": "DEVELOPMENT_SMOKE_TEST_NOT_PEER_REVIEWED_NOT_HELD_OUT",
        "n_evidence_records": len(docs),
        "n_independent_question_groups": len({q["question_id"] for q in queries}),
        "n_correlated_script_variants": len(queries),
        "method_scores_for_debugging_only": summary(rows),
        "top1_failures": errors,
        "disclaimer": (
            "This tiny author-drafted dataset is unsuitable for research inference. "
            "The date-filtered ranker may face only one candidate at a time. "
            "Do not cite these percentages in a submitted paper."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="ScriptTime-UZ prototype, NOT legal advice")
    sub = parser.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query")
    q.add_argument("text")
    q.add_argument("--method", choices=METHODS, default="bm25_norm_time")
    q.add_argument("--as-of", default="2026-10-27")
    q.add_argument("--known-at", default="2026-10-27")
    q.add_argument("--case", choices=DATASETS, default="seed")
    q.add_argument("--evidence-mode", choices=["operative_rule", "published_document"], default="operative_rule")
    e = sub.add_parser("evaluate")
    e.add_argument("--case", choices=DATASETS, default="seed")
    args = parser.parse_args()

    if args.cmd == "evaluate":
        print(json.dumps(report_case(args.case), ensure_ascii=False, indent=2))
        return

    docs_path, query_path = DATASETS[args.case]
    docs, _ = load_data(ROOT / docs_path, ROOT / query_path)
    for record, score in rank(
        args.text, docs, args.method, as_of=args.as_of, known_at=args.known_at,
        evidence_mode=args.evidence_mode
    ):
        print(f"{score:.4f}\t{record.doc_id}\t{record.title}\n  {record.source_url}")


if __name__ == "__main__":
    main()
