"""Candidate pool validation does not imply human verification."""
import unittest
from scripttime.review import validate_candidate_questions


class CandidateReviewTests(unittest.TestCase):
    def test_candidate_pool_is_not_gold(self):
        report = validate_candidate_questions()
        self.assertEqual(report["dataset_status"], "CANDIDATES_NOT_GOLD")
        self.assertEqual(report["candidate_question_groups"], 30)
        self.assertEqual(report["human_verified"], 0)
        self.assertEqual(report["unreviewed"], 30)
        self.assertEqual(len(report["domains"]), 5)
