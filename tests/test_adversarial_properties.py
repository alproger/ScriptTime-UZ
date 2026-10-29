"""Counterfactual time boundaries and deterministic ranker properties."""
import unittest
from scripttime.__main__ import DATASETS, ROOT
from scripttime.evaluate import load_data, candidate_difficulty, evaluate, summary
from scripttime.retrieval import rank, valid_at, published_by

class AdversarialPropertiesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        a,b=DATASETS["challenge"]
        cls.docs,cls.queries=load_data(ROOT/a,ROOT/b)
        cls.by_id={d.doc_id:d for d in cls.docs}

    def test_challenge_has_13_source_records(self):
        self.assertEqual(len(self.docs),13)

    def test_challenge_24_distinct_group_ids(self):
        self.assertEqual(len({q["question_id"] for q in self.queries}),24)

    def test_challenge_has_three_variants_per_group(self):
        from collections import Counter
        counts=Counter(q["question_id"] for q in self.queries)
        self.assertEqual(set(counts.values()),{3})

    def test_challenge_has_seven_abstention_groups(self):
        self.assertEqual(len({q["question_id"] for q in self.queries
                         if q["needs_abstention"]=="1"}),7)

    def test_labor_inclusive_exclusive_boundary(self):
        old,new=self.by_id["labor_old"],self.by_id["labor_new"]
        self.assertTrue(valid_at(old,"2023-04-29","2026-10-29"))
        self.assertFalse(valid_at(old,"2023-04-30","2026-10-29"))
        self.assertFalse(valid_at(new,"2023-04-29","2026-10-29"))
        self.assertTrue(valid_at(new,"2023-04-30","2026-10-29"))

    def test_water_inclusive_exclusive_boundary(self):
        old,new=self.by_id["water_old"],self.by_id["water_new"]
        self.assertTrue(valid_at(old,"2025-10-30","2026-10-29"))
        self.assertFalse(valid_at(old,"2025-10-31","2026-10-29"))
        self.assertTrue(valid_at(new,"2025-10-31","2026-10-29"))

    def test_quota_inclusive_exclusive_boundary(self):
        old,new=self.by_id["quota_old_mixed"],self.by_id["quota_new_mixed"]
        self.assertTrue(valid_at(old,"2026-07-02","2026-10-29"))
        self.assertFalse(valid_at(old,"2026-07-03","2026-10-29"))
        self.assertTrue(valid_at(new,"2026-07-03","2026-10-29"))

    def test_alphabet_publication_is_not_effectiveness(self):
        new=self.by_id["alphabet_new_mixed"]
        self.assertTrue(published_by(new,"2026-10-21"))
        self.assertFalse(valid_at(new,"2026-10-21","2026-10-21"))

    def test_alphabet_effective_day_is_inclusive(self):
        self.assertTrue(valid_at(self.by_id["alphabet_new_mixed"],
                                 "2027-04-22","2026-10-29"))

    def test_prepublication_alphabet_is_hidden(self):
        self.assertFalse(published_by(self.by_id["alphabet_new_mixed"],"2026-10-20"))

    def test_future_law_accessible_in_publication_mode(self):
        got=rank("1184 alifbo 28",self.docs,"bm25_norm_time",
                 as_of="2026-10-27",known_at="2026-10-27",evidence_mode="published_document")
        self.assertIn("alphabet_new_mixed",[d.doc_id for d,_ in got])

    def test_published_before_known_at_is_enforced_for_raw_bm25(self):
        got=rank("1184 alifbo 28",self.docs,"bm25",
                 known_at="2026-10-20",evidence_mode="published_document")
        ids=[d.doc_id for d,_ in got]
        self.assertNotIn("alphabet_new_mixed",ids)
        self.assertNotIn("alphabet_entry_art4",ids)

    def test_rank_deterministic_under_input_reversal(self):
        a=rank("suv kodeksi",self.docs,"bm25_norm_time",
               as_of="2025-10-31",known_at="2026-10-29")
        b=rank("suv kodeksi",list(reversed(self.docs)),"bm25_norm_time",
               as_of="2025-10-31",known_at="2026-10-29")
        self.assertEqual([x.doc_id for x,_ in a],[x.doc_id for x,_ in b])

    def test_rank_all_scores_positive_and_sorted(self):
        out=rank("alifbo",self.docs,"char3_norm",
                 known_at="2026-10-29",evidence_mode="published_document")
        self.assertTrue(all(v>0 for _,v in out))
        self.assertEqual([v for _,v in out], sorted((v for _,v in out),reverse=True))

    def test_rank_no_keyword_overlap_abstains(self):
        self.assertEqual(rank("zzzzxxxyyy",self.docs,"bm25_norm",
                          known_at="2026-10-29",evidence_mode="published_document"),[])

    def test_zero_k_rejected(self):
        with self.assertRaises(ValueError):
            rank("q",self.docs,k=0)

    def test_no_unpublished_future_retrieval_in_time_aware(self):
        out=rank("2027 alifbo",self.docs,"bm25_norm_time",
                 as_of="2027-04-23",known_at="2026-10-20",
                 evidence_mode="published_document")
        self.assertFalse(any(d.doc_id in {"alphabet_new_mixed","alphabet_entry_art4"}
                             for d,_ in out))

    def test_candidate_difficulty_reports_eligible_counts(self):
        details=candidate_difficulty(self.docs,self.queries)
        self.assertEqual(len(details),72)
        self.assertTrue(any(r["eligible_documents"]>=2 for r in details))

    def test_all_5_methods_make_72_rows_each(self):
        rows=evaluate(self.docs,self.queries)
        self.assertEqual(len(rows),360)
        self.assertEqual(set(summary(rows)),{"bm25","bm25_norm","char3_norm",
                                             "bm25_time","bm25_norm_time"})

    def test_summary_stratifies_abstention(self):
        s=summary(evaluate(self.docs,self.queries))
        self.assertEqual(s["bm25_norm_time"]["n_abstention_variants"],21)
        self.assertIsNotNone(s["bm25_norm_time"]["false_answer_on_unanswerable"])

    def test_all_time_aware_top1_are_eligible(self):
        rows=evaluate(self.docs,self.queries)
        for r in rows:
            if r["method"] in {"bm25_time","bm25_norm_time"}:
                self.assertEqual(r["invalid_top1"],0)

    def test_date_filter_does_not_claim_triviality_was_solved(self):
        detail=candidate_difficulty(self.docs,self.queries)
        self.assertTrue(any(r["is_single_candidate"] for r in detail))
