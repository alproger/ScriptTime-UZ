import unittest
from scripttime.__main__ import ROOT
from scripttime.evaluate import load_data,evaluate
from scripttime.retrieval import rank

class IntentDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, cls.queries = load_data(ROOT/"data/seed/documents.jsonl",
            ROOT/"data/experiments/intent_boundary_queries.csv")

    def test_two_question_groups_and_two_intents(self):
        self.assertEqual(len(self.queries), 6)
        self.assertEqual({q["evidence_mode"] for q in self.queries},
                         {"published_document","operative_rule"})

    def test_future_law_retrieval_uses_intent(self):
        published=next(q for q in self.queries if q["question_id"]=="published_1184" and q["script"]=="old_latin")
        operative=next(q for q in self.queries if q["question_id"]=="operative_oct26" and q["script"]=="old_latin")
        for q in (published,operative):
            result=rank(q["query"],self.docs,"bm25_norm_time",as_of=q["as_of"],
                        known_at=q["known_at"],evidence_mode=q["evidence_mode"])
            self.assertTrue(result)
            self.assertEqual(result[0][0].doc_id,q["gold_doc_id"])

    def test_evaluate_passes_intent_through(self):
        rows=evaluate(self.docs,self.queries)
        self.assertEqual(len(rows),30)
        self.assertIn("published_document",{r["evidence_mode"] for r in rows})
