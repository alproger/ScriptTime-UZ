"""Mixed-domain case ensures more than one eligible candidate for current dates."""
import unittest
from datetime import date
from scripttime.__main__ import DATASETS, ROOT, report_case
from scripttime.evaluate import load_data
from scripttime.retrieval import valid_at

class MixedTemporalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        a,b = DATASETS["mixed_temporal"]
        cls.docs,cls.queries=load_data(ROOT/a, ROOT/b)

    def test_8_groups_and_24_variants(self):
        self.assertEqual(len(self.docs),9)
        self.assertEqual(len(self.queries),24)
        self.assertEqual(len({q["question_id"] for q in self.queries}),8)

    def test_multiple_live_candidates_in_2026(self):
        count=sum(valid_at(d,"2026-07-03","2026-10-27") for d in self.docs)
        self.assertGreaterEqual(count,4)

    def test_labor_boundary(self):
        old=next(d for d in self.docs if d.doc_id=="labor_old")
        new=next(d for d in self.docs if d.doc_id=="labor_new")
        self.assertTrue(valid_at(old,"2023-04-29","2026-10-27"))
        self.assertFalse(valid_at(old,"2023-04-30","2026-10-27"))
        self.assertFalse(valid_at(new,"2023-04-29","2026-10-27"))
        self.assertTrue(valid_at(new,"2023-04-30","2026-10-27"))

    def test_water_boundary(self):
        old=next(d for d in self.docs if d.doc_id=="water_old")
        new=next(d for d in self.docs if d.doc_id=="water_new")
        self.assertTrue(valid_at(old,"2025-10-30","2026-10-27"))
        self.assertFalse(valid_at(new,"2025-10-30","2026-10-27"))
        self.assertFalse(valid_at(old,"2025-10-31","2026-10-27"))
        self.assertTrue(valid_at(new,"2025-10-31","2026-10-27"))

    def test_report_has_explicit_warning(self):
        r=report_case("mixed_temporal")
        self.assertIn("NOT_HELD_OUT",r["experiment_status"])
        self.assertEqual(r["n_independent_question_groups"],8)
