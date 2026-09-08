"""Exercise file boundaries when loading independently valid TSV shards."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_corpus import load_corpus, validate_python


class CorpusFileTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_missing_final_newlines_do_not_join_records(self):
        self.put('a.tsv', 'sum\t0\t1\t1')
        self.put('nested/b.tsv', 'sum\t0\t2\t2')
        self.assertEqual(validate_python(load_corpus(self.root)), 2)

    def test_empty_shards_and_empty_vector_fields_are_preserved(self):
        self.put('a.tsv', '')
        self.put('b.tsv', 'prefix\t0\t\t')
        self.put('c.tsv', 'sum\t0\t\t0\n')
        self.assertEqual(validate_python(load_corpus(self.root)), 2)

    def test_malformed_and_blank_records_are_not_silently_repaired(self):
        self.put('b.tsv', 'sum\t0\t2\t2\n')
        for invalid in ['sum\t0\t1', '\n']:
            with self.subTest(invalid=invalid):
                self.put('a.tsv', invalid)
                with self.assertRaises(ValueError):
                    validate_python(load_corpus(self.root))
