#!/usr/bin/env python3
"""Verify all shared cases against Python, Rust, and C++ implementations."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'python'))
from sequence_tools import evaluate


def integer(raw):
    if not re.fullmatch(r'[+-]?[0-9]+', raw):
        raise ValueError('invalid integer token')
    value = int(raw)
    if not -(1 << 63) <= value < (1 << 63):
        raise ValueError('integer outside signed 64-bit range')
    return value


def validate_python(text):
    count = 0
    for line in text.splitlines():
        operation, argument, raw_values, raw_expected = line.split('\t')
        values = [integer(v) for v in raw_values.split(',')] if raw_values else []
        expected = [integer(v) for v in raw_expected.split(',')] if raw_expected else []
        actual = evaluate(operation, values, integer(argument))
        if actual != expected:
            raise ValueError(f'Corpus row {count + 1}: {actual} != {expected}')
        count += 1
    return count


def load_corpus(directory):
    """Keep each shard's last record separate from the next shard's first."""
    parts = []
    for path in sorted(directory.rglob('*.tsv')):
        text = path.read_text()
        if text:
            parts.append(text if text.endswith('\n') else text + '\n')
    if not parts:
        raise ValueError(f'No corpus examples found in {directory}')
    return ''.join(parts)


def main():
    text = load_corpus(ROOT / 'corpus')
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
