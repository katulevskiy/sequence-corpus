#!/usr/bin/env python3
"""Verify all shared cases against Python, Rust, and C++ implementations."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'python'))
from sequence_tools import evaluate


def validate_python(text):
    count = 0
    for line in text.splitlines():
        operation, argument, raw_values, raw_expected = line.split('\t')
        values = [int(v) for v in raw_values.split(',')] if raw_values else []
        expected = [int(v) for v in raw_expected.split(',')] if raw_expected else []
        actual = evaluate(operation, values, int(argument))
        if actual != expected:
            raise ValueError(f'Corpus row {count + 1}: {actual} != {expected}')
        count += 1
    return count


def main():
    text = ''.join(path.read_text() for path in sorted((ROOT / 'corpus').rglob('*.tsv')))
    print(f'Python: {validate_python(text)} corpus cases passed', flush=True)
    subprocess.run(['cargo', 'run', '--quiet', '--manifest-path', str(ROOT / 'rust/Cargo.toml'),
                    '--bin', 'corpus'], input=text, text=True, check=True)
    with tempfile.TemporaryDirectory() as directory:
        binary = str(Path(directory) / 'corpus')
        subprocess.run(['c++', '-std=c++17', '-O1', '-Wall', '-Wextra', '-Werror',
                        str(ROOT / 'cpp/corpus.cpp'), '-o', binary], check=True)
        subprocess.run([binary], input=text, text=True, check=True)


if __name__ == '__main__':
    main()
