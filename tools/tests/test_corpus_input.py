"""Check the same input contract through all three language runners."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from check_corpus import validate_python


class CorpusInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        subprocess.run(['cargo', 'build', '--quiet', '--manifest-path', str(ROOT / 'rust/Cargo.toml'),
                        '--bin', 'corpus'], check=True)
        cls.cpp = str(Path(cls.temp.name) / 'corpus')
        subprocess.run(['c++', '-std=c++17', '-O1', '-Wall', '-Wextra', '-Werror',
                        str(ROOT / 'cpp/corpus.cpp'), '-o', cls.cpp], check=True)

    def assert_accepted(self, row, expected):
        try:
            validate_python(row)
            accepted = True
        except (ValueError, OverflowError):
            accepted = False
        with self.subTest(language='Python', row=row):
            self.assertEqual(accepted, expected)
        for name, command in [('Rust', str(ROOT / 'rust/target/debug/corpus')), ('C++', self.cpp)]:
            result = subprocess.run([command], input=row, capture_output=True, text=True)
            with self.subTest(language=name, row=row):
                self.assertEqual(result.returncode == 0, expected, result.stderr)

    def test_valid_signed_integers_and_empty_vectors(self):
        for row in ['sum\t0\t\t0\n', 'reverse\t+0\t-1,+2,0\t0,2,-1\n',
                    'reverse\t0\t-9223372036854775808,9223372036854775807\t9223372036854775807,-9223372036854775808\n']:
            self.assert_accepted(row, True)

    def test_malformed_integer_tokens_are_rejected_in_every_field(self):
        for token in ['0junk', ' 0', '0 ', '0_0', '０', '+', '--0', '9223372036854775808', '-9223372036854775809']:
            for field in (1, 2, 3):
                parts = ['reverse', '0', '0', '0']
                parts[field] = token
                self.assert_accepted('\t'.join(parts) + '\n', False)

    def test_empty_list_elements_are_rejected(self):
        for raw in ['0,', ',0', '0,,0']:
            for field in (2, 3):
                parts = ['reverse', '0', '0', '0']
                parts[field] = raw
                self.assert_accepted('\t'.join(parts) + '\n', False)


if __name__ == '__main__':
    unittest.main()
