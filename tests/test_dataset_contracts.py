"""Fail-fast dataset contracts. No assertions about research effectiveness."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripttime.evaluate import load_data

def doc(**overrides):
    values=dict(doc_id="doc1", family_id="f", title="Title", text="Text",
        source_url="https://lex.uz/docs/1", issued_on="2020-01-01",
        available_from="2020-01-02", study_valid_from="2020-01-02",
        study_valid_to=None)
    values.update(overrides)
    return values

def question(**overrides):
    values=dict(question_id="q1", script="old_latin", query="A test?",
        as_of="2020-01-02", known_at="2020-01-03", gold_doc_id="doc1",
        evidence_mode="operative_rule", needs_abstention="0")
    values.update(overrides)
    return values

def load(docs, queries):
    with tempfile.TemporaryDirectory() as folder:
        dp=Path(folder)/"documents.jsonl"
        qp=Path(folder)/"queries.csv"
        dp.write_text("\n".join(json.dumps(x) for x in docs),encoding="utf8")
        fields=("question_id","script","query","as_of","known_at","gold_doc_id",
                "evidence_mode","needs_abstention")
        with qp.open("w",encoding="utf8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=fields)
            writer.writeheader()
            for q in queries:
                writer.writerow(q)
        return load_data(dp,qp)

class CorpusValidationTests(unittest.TestCase):
    def test_minimal_valid_corpus(self):
        d,q=load([doc()],[question()])
        self.assertEqual(len(d),1)
        self.assertEqual(q[0]["needs_abstention"],"0")

    def test_valid_abstention_needs_blank_gold(self):
        _,q=load([doc()],[question(gold_doc_id="",needs_abstention="1")])
        self.assertEqual(q[0]["needs_abstention"],"1")

    def test_yes_as_abstention_is_accepted(self):
        _,q=load([doc()],[question(gold_doc_id="",needs_abstention="yes")])
        self.assertEqual(q[0]["needs_abstention"],"1")

    def test_abstention_with_gold_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(needs_abstention="1")])

    def test_non_abstention_without_gold_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(gold_doc_id="")])

    def test_unknown_gold_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(gold_doc_id="invented")])

    def test_duplicate_document_ids_rejected(self):
        with self.assertRaises(ValueError):
            load([doc(),doc()],[question()])

    def test_duplicate_variant_id_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(),question()])

    def test_group_label_disagreement_rejected(self):
        with self.assertRaises(ValueError):
            load([doc(),doc(doc_id="doc2")],
                 [question(),question(script="cyrillic",gold_doc_id="doc2")])

    def test_group_asof_disagreement_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(),question(script="cyrillic",as_of="2020-01-04")])

    def test_group_intent_disagreement_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(),question(script="cyrillic",evidence_mode="published_document")])

    def test_empty_documents_rejected(self):
        with self.assertRaises(ValueError):
            load([],[question()])

    def test_empty_queries_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[])

    def test_unknown_script_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(script="latin_fantasy")])

    def test_unknown_evidence_mode_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(evidence_mode="magical")])

    def test_invalid_iso_date_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(as_of="2026-99-88")])

    def test_invalid_document_date_rejected(self):
        with self.assertRaises(ValueError):
            load([doc(issued_on="tomorrow")],[question()])

    def test_invalid_backwards_interval_rejected(self):
        with self.assertRaises(ValueError):
            load([doc(study_valid_to="2019-12-31")],[question()])

    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):
            load([doc()],[question(query="")])
