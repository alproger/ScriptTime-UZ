"""Evidence abstraction tests: changing writing style must not alter validity metadata."""
import unittest
from scripttime.retrieval import Evidence, published_by, valid_at, bm25_score, trigram_score
from scripttime.normalize import normalize

class MetamorphicUnitTests(unittest.TestCase):
    def record(self,**kw):
        v={"doc_id":"x","family_id":"same","title":"matn","text":"matn",
           "source_url":"https://lex.uz/docs/1","issued_on":"2026-10-21",
           "available_from":"2026-10-21","study_valid_from":"2027-04-22",
           "study_valid_to":None}
        v.update(kw)
        return Evidence(**v)

    def test_publication_boundary_day_before(self):
        self.assertFalse(published_by(self.record(),"2026-10-20"))

    def test_publication_boundary_exact_date(self):
        self.assertTrue(published_by(self.record(),"2026-10-21"))

    def test_publication_boundary_after(self):
        self.assertTrue(published_by(self.record(),"2026-10-22"))

    def test_expiry_exclusive(self):
        x=self.record(study_valid_to="2027-04-23")
        self.assertTrue(valid_at(x,"2027-04-22","2026-10-27"))
        self.assertFalse(valid_at(x,"2027-04-23","2026-10-27"))

    def test_reversing_query_script_does_not_change_validity(self):
        x=self.record(title="Özbek",text="O‘zbek")
        self.assertEqual(valid_at(x,"2027-04-22","2026-10-27"),
                         valid_at(x,"2027-04-22","2026-10-27"))

    def test_cyrillic_normalization(self):
        self.assertEqual(normalize("Ўзбекистон"),"o'zbekiston")

    def test_new_latin_letters_normalize(self):
        self.assertEqual(normalize("Ö Ş Ç Ğ"),"o' sh ch g'")

    def test_mixed_apostrophe_normalization(self):
        self.assertEqual(normalize("o‘ oʻ o'"),"o' o' o'")

    def test_bm25_empty_docs(self):
        self.assertEqual(bm25_score("test",[]),[])

    def test_trigram_exact_match_scores_one(self):
        self.assertEqual(trigram_score("o‘zbek",["o‘zbek"]),[1.0])

    def test_trigram_empty_overlap_zero(self):
        self.assertEqual(trigram_score("abc",["xyz"]),[0.0])
