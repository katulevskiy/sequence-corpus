# Sequence corpus

Small integer-sequence implementations in Rust, Python, and C++17, checked against a shared regression corpus. Operations include prefix sums, adjacent differences, sorted deduplication, run-length encoding, rotation, sliding-window sums, bounds, and clamping.

Run the same examples through all three implementations:

```sh
python3 tools/check_corpus.py
cargo test --manifest-path rust/Cargo.toml
```

The TSV format is operation, integer argument, comma-separated input, and comma-separated expected output. Empty vector fields are allowed; empty elements inside a nonempty list are rejected. Integer tokens contain an optional ASCII sign followed by ASCII digits, with no whitespace or trailing characters. Values and intermediate arithmetic must fit signed 64-bit integers; rotation counts, window sizes, and clamp limits are nonnegative.

This project uses automation to propose additional generated regression examples, with reviews and maintenance recorded in issues and pull requests.

The Corpus proposals workflow checks every six hours. It can open 1–4 proposals on an active day, with weekend variation and quiet periods. Its queue is capped at six open proposals. Every new shard is checked by all three implementations before opening a PR. Reviews identify their automated origin and describe the validation performed; merging is a separate action after review.

Run the input-contract regression tests with `python3 -m unittest discover -s tools/tests -v`.
