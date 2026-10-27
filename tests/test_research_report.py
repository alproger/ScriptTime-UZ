"""The CLI must label demonstration scores and keep independent-group counts honest."""
import unittest
from scripttime.__main__ import report_case


class ResearchReportTests(unittest.TestCase):
    def test_annex3a_sample_groups_not_rows(self):
        report = report_case("annex3a")
        self.assertEqual(report["n_evidence_records"], 2)
        self.assertEqual(report["n_independent_question_groups"], 4)
        self.assertEqual(report["n_correlated_script_variants"], 12)
        self.assertIn("NOT_HELD_OUT", report["experiment_status"])

    def test_all_five_baselines_evaluated(self):
        methods = report_case("annex3a")["method_scores_for_debugging_only"]
        self.assertEqual(set(methods), {"bm25", "bm25_norm", "char3_norm", "bm25_time", "bm25_norm_time"})

    def test_report_disclaims_trivial_single_candidate_case(self):
        report = report_case("annex3a")
        self.assertIn("only one candidate", report["disclaimer"])

    def test_seed_dataset_is_separately_counted(self):
        report = report_case("seed")
        self.assertEqual(report["n_independent_question_groups"], 3)
        self.assertEqual(report["n_correlated_script_variants"], 9)
