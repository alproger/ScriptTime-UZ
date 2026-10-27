"""Simple validation for candidate research questions awaiting author approval."""
import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW_FILE = ROOT / "data/annotation/candidate_questions_v1.csv"


def validate_candidate_questions(path=REVIEW_FILE):
    with open(path, encoding="utf8", newline="") as f:
        rows = list(csv.DictReader(f))
    required = ("question_id", "domain", "question", "expected_answer", "as_of",
                "known_at", "reference_url", "issue_url", "review_status")
    for row in rows:
        if not all(row.get(k) for k in required):
            raise ValueError("Missing required candidate field")
        date.fromisoformat(row["as_of"])
        date.fromisoformat(row["known_at"])
        if not row["reference_url"].startswith("https://lex.uz/"):
            raise ValueError("Expected official LexUZ evidence reference")
        if row["review_status"] not in ("pending_author_review","author_verified","rejected","ambiguous"):
            raise ValueError("Unexpected review status")
    ids = [r["question_id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate question IDs")
    return {
       "dataset_status": "CANDIDATES_NOT_GOLD",
       "candidate_question_groups": len(rows),
       "human_verified": sum(r["review_status"] == "author_verified" for r in rows),
       "unreviewed": sum(r["review_status"] == "pending_author_review" for r in rows),
       "domains": dict(Counter(r["domain"] for r in rows)),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(validate_candidate_questions(), indent=2, ensure_ascii=False))
