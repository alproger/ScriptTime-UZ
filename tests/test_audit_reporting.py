"""Reproducibility and coverage checks for research audit output."""
import unittest
from scripttime.audit import report

class AuditReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=report("challenge")

    def test_diagnostic_not_gold(self):
        self.assertIn("NOT_SCIENTIFIC_GOLD",self.report["STATUS"])

    def test_correct_base_count(self):
        self.assertEqual(self.report["n_base_question_groups"],24)

    def test_number_of_variants_not_misreported_as_independents(self):
        self.assertEqual(self.report["n_correlated_script_variants"],72)

    def test_negative_groups_separately_counted(self):
        self.assertEqual(self.report["n_unanswerable_groups"],7)

    def test_strata_show_both_intents(self):
        keys=self.report["stratified_errors"]
        self.assertTrue(any("/published_document/" in k for k in keys))
        self.assertTrue(any("/operative_rule/" in k for k in keys))

    def test_each_method_has_three_script_strata(self):
        ks=self.report["stratified_errors"]
        for name in ("bm25","bm25_norm","char3_norm","bm25_time","bm25_norm_time"):
            got=[k for k in ks if k.startswith(name+"/")]
            self.assertEqual(len(got),6)

    def test_bootstrap_is_flagged_as_diagnostic(self):
        self.assertIn("DIAGNOSTIC",self.report["paired_group_bootstrap_exploratory_only"]["status"])

    def test_eligible_candidates_have_multiple_choices(self):
        self.assertGreaterEqual(self.report["eligible_candidate_summary"]["min"],2)

    def test_top1_error_buckets_are_numerically_consistent(self):
        for stat in self.report["stratified_errors"].values():
            self.assertEqual(stat["correct_top1"]+stat["errors"],stat["n_variants"])
            self.assertLessEqual(stat["false_answers"],stat["unanswerable"])
