"""Real issue: publishing an act is not the same as legal entry into force."""
import unittest
from scripttime.evaluate import load_data
from scripttime.__main__ import DOCS, QUERIES
from scripttime.retrieval import rank, published_by, valid_at

class TemporalIntentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, _ = load_data(DOCS, QUERIES)
        cls.new = next(d for d in cls.docs if d.doc_id == "alphabet_new")

    def test_published_law_exists_before_entry_into_force(self):
        self.assertTrue(published_by(self.new, "2026-10-27"))
        self.assertFalse(valid_at(self.new, "2026-10-27", "2026-10-27"))

    def test_operative_mode_excludes_new_law_before_entry(self):
        result = rank("yangi alifbo 28 harf", self.docs, "bm25_norm_time",
                      as_of="2026-10-27", known_at="2026-10-27",
                      evidence_mode="operative_rule")
        self.assertNotIn("alphabet_new", [r.doc_id for r, _ in result])

    def test_discovery_mode_finds_announced_law(self):
        result = rank("O‘RQ-1184 yangi alifbo 28 harf", self.docs, "bm25_norm_time",
                      as_of="2026-10-27", known_at="2026-10-27",
                      evidence_mode="published_document")
        self.assertIn("alphabet_new", [r.doc_id for r, _ in result])

    def test_no_future_information_leak_to_discovery_mode(self):
        result = rank("O‘RQ-1184 28 harf", self.docs, "bm25_norm_time",
                      known_at="2026-10-20", evidence_mode="published_document")
        self.assertNotIn("alphabet_new", [r.doc_id for r, _ in result])

    def test_all_baselines_apply_known_at(self):
        for method in ("bm25", "bm25_norm", "char3_norm"):
            with self.subTest(method=method):
                result = rank("O‘RQ-1184 28 harf", self.docs, method,
                              known_at="2026-10-20", evidence_mode="published_document")
                self.assertNotIn("alphabet_new", [r.doc_id for r, _ in result])

    def test_discovery_needs_known_at_but_not_as_of(self):
        result = rank("O‘RQ-1184", self.docs, "bm25_norm_time",
                      known_at="2026-10-27", evidence_mode="published_document")
        self.assertIn("alphabet_new", [r.doc_id for r, _ in result])

    def test_no_zero_score_false_evidence(self):
        result = rank("zzzxxyy impossible", self.docs, "bm25_norm_time",
                      known_at="2026-10-27", evidence_mode="published_document")
        self.assertEqual(result, [])

    def test_operative_dates_required(self):
        with self.assertRaises(ValueError):
            rank("test", self.docs, "bm25_norm_time", known_at="2026-10-27")

    def test_invalid_intent_rejected(self):
        with self.assertRaises(ValueError):
            rank("test", self.docs, evidence_mode="guess")
