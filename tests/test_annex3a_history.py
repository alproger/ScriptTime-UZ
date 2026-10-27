"""Version-boundary engineering checks for two source-verified editions.

These tests establish code behavior ONLY. They are not held-out research results.
"""
import unittest
from pathlib import Path
from scripttime.evaluate import load_data
from scripttime.retrieval import rank, valid_at

BASE = Path(__file__).resolve().parents[1] / "data" / "experiments"

class Annex3AHistoricalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, cls.questions = load_data(BASE / "annex3a_versions.jsonl", BASE / "annex3a_candidate_questions.csv")
        cls.old = next(d for d in cls.docs if d.doc_id.endswith("2025_snapshot"))
        cls.new = next(d for d in cls.docs if d.doc_id.endswith("2026_amended"))

    def test_two_versions_same_clausal_family(self):
        self.assertEqual(len(self.docs), 2)
        self.assertEqual(len({d.family_id for d in self.docs}), 1)

    def test_interval_boundary(self):
        self.assertTrue(valid_at(self.old, "2026-07-02", "2026-10-27"))
        self.assertFalse(valid_at(self.new, "2026-07-02", "2026-10-27"))
        self.assertFalse(valid_at(self.old, "2026-07-03", "2026-10-27"))
        self.assertTrue(valid_at(self.new, "2026-07-03", "2026-10-27"))

    def test_future_amendment_not_available_early(self):
        self.assertFalse(valid_at(self.new, "2026-07-03", "2026-07-02"))

    def test_version_filter_ignores_query_spelling(self):
        for as_of, gold in (("2026-07-02", self.old.doc_id), ("2026-07-03", self.new.doc_id)):
            ranked = rank("kvota 3a maktab o'quvchi", self.docs, "bm25_norm_time", as_of=as_of, known_at="2026-10-27")
            self.assertEqual([doc.doc_id for doc, _ in ranked], [gold])

    def test_candidate_question_group_count(self):
        self.assertEqual(len(self.questions), 12)
        self.assertEqual(len({q["question_id"] for q in self.questions}), 4)
