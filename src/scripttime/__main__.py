import argparse
import json
from pathlib import Path
from .evaluate import load_data, evaluate, summary
from .retrieval import rank

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'data/seed/documents.jsonl'
QUERIES = ROOT / 'data/seed/queries.csv'


def main():
    parser = argparse.ArgumentParser(description='ScriptTime-UZ prototype, NOT legal advice')
    sub = parser.add_subparsers(dest='cmd', required=True)
    q = sub.add_parser('query')
    q.add_argument('text')
    q.add_argument('--method', choices=['bm25', 'bm25_norm', 'char3_norm', 'bm25_time', 'bm25_norm_time'], default='bm25_norm_time')
    q.add_argument('--as-of', default='2026-10-27')
    q.add_argument('--known-at', default='2026-10-27')
    sub.add_parser('evaluate')
    args = parser.parse_args()
    docs, queries = load_data(DOCS, QUERIES)
    if args.cmd == 'evaluate':
        results = evaluate(docs, queries)
        print(json.dumps({"dataset_status": "SMOKE_TEST_NOT_PUBLISHABLE_BENCHMARK", "results": summary(results)}, indent=2, ensure_ascii=False))
    else:
        for doc, score in rank(args.text, docs, args.method, as_of=args.as_of, known_at=args.known_at):
            print(f'{score:.4f}\t{doc.doc_id}\t{doc.title}\n  {doc.source_url}')


if __name__ == '__main__':
    main()
