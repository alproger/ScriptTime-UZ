import unittest
from scripttime.analysis import grouped_accuracy, paired_question_bootstrap
from scripttime.__main__ import DATASETS, ROOT
from scripttime.evaluate import load_data, evaluate


class GroupedStatisticsTests(unittest.TestCase):
    def test_example_has_two_question_groups_not_six_samples(self):
        rows = []
        for method in ("bm25", "bm25_norm_time"):
            for group in ("q1", "q2"):
                for script in ("old_latin", "new_latin", "cyrillic"):
                    good = 1 if method == "bm25_norm_time" or group == "q2" else 0
                    rows.append({"method":method,"question_id":group,"script":script,
                                 "hit1":good,"recall3":good,"rr":float(good)})
        grouped = grouped_accuracy(rows)
        self.assertEqual(len(grouped["bm25"]),2)
        stats = paired_question_bootstrap(rows,baseline="bm25",candidate="bm25_norm_time")
        self.assertEqual(stats["n_question_groups"],2)
        self.assertEqual(stats["mean_paired_difference"],0.5)
        self.assertIn("NOT_INDEPENDENT",stats["status"])

    def test_duplicate_rows_fail_loudly(self):
        row={"method":"bm25","question_id":"q","script":"cyrillic","hit1":1}
        with self.assertRaises(ValueError):
            grouped_accuracy([row,row])

    def test_unpaired_method_groups_fail(self):
        rows=[
            {"method":"bm25","question_id":"q1","script":"old_latin","hit1":1},
            {"method":"bm25","question_id":"q2","script":"old_latin","hit1":1},
            {"method":"bm25_norm_time","question_id":"q1","script":"old_latin","hit1":1},
        ]
        with self.assertRaises(ValueError):
            paired_question_bootstrap(rows,baseline="bm25",candidate="bm25_norm_time")

    def test_real_development_data_is_labeled_diagnostic(self):
        a,b=DATASETS["mixed_temporal"]
        docs,queries=load_data(ROOT/a,ROOT/b)
        rows=evaluate(docs,queries)
        stats=paired_question_bootstrap(rows,baseline="bm25",candidate="bm25_norm_time",
                                        resamples=100)
        self.assertEqual(stats["n_question_groups"],8)
        self.assertIn("DIAGNOSTIC",stats["status"])
