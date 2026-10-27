import unittest
from scripttime.evaluate import load_data, evaluate, summary
from scripttime.retrieval import valid_at, rank
from scripttime.__main__ import DOCS, QUERIES

class TemporalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, cls.queries = load_data(DOCS, QUERIES)
        cls.old = next(x for x in cls.docs if x.doc_id == 'alphabet_old')
        cls.new = next(x for x in cls.docs if x.doc_id == 'alphabet_new')

    def test_effective_day_exclusive_boundary(self):
        self.assertTrue(valid_at(self.old, '2027-04-21', '2026-10-27'))
        self.assertFalse(valid_at(self.old, '2027-04-22', '2026-10-27'))
        self.assertFalse(valid_at(self.new, '2027-04-21', '2026-10-27'))
        self.assertTrue(valid_at(self.new, '2027-04-22', '2026-10-27'))

    def test_not_known_before_publication(self):
        self.assertFalse(valid_at(self.new, '2027-04-23', '2026-10-20'))

    def test_filter_excludes_future_rule(self):
        results = rank('yangi o‘zbek alifbosi 28 harf', self.docs, 'bm25_norm_time', as_of='2026-10-27', known_at='2026-10-27')
        self.assertNotIn('alphabet_new', [doc.doc_id for doc, _ in results])

    def test_requires_explicit_dates(self):
        with self.assertRaises(ValueError):
            rank('test', self.docs, 'bm25_norm_time')

    def test_dataset_group_sizes(self):
        rows = evaluate(self.docs, self.queries)
        assert summary(rows)['bm25']['n_independent_question_groups'] == 3
        assert summary(rows)['bm25']['n_query_variants'] == 9
