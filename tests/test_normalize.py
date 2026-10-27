import unittest
from scripttime.normalize import normalize

class NormalizationTests(unittest.TestCase):
    def test_new_latin(self):
        self.assertEqual(normalize("Özbekçe şahar, ğalla"), normalize("O'zbekche shahar, g'alla"))

    def test_unicode_apostrophes(self):
        for word in ("O‘ZBEK", "OʻZBEK", "O'ZBEK", "OʼZBEK"):
            self.assertEqual(normalize(word), "o'zbek")

    def test_cyrillic(self):
        self.assertEqual(normalize("Ўзбекистон шaҳар"), "o'zbekiston shahar")

    def test_idempotent(self):
        sample = "Özbekistonning Şahri!"
        self.assertEqual(normalize(normalize(sample)), normalize(sample))
