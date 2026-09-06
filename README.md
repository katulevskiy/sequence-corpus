# Sequence corpus

Small integer-sequence implementations in Rust, Python, and C++17, checked against a shared regression corpus. Operations include prefix sums, adjacent differences, sorted deduplication, run-length encoding, rotation, sliding-window sums, bounds, and clamping.

Run the same examples through all three implementations:

```sh
python3 tools/check_corpus.py
cargo test --manifest-path rust/Cargo.toml
```

The TSV format is operation, integer argument, comma-separated input, and comma-separated expected output. Empty vector fields are allowed. Values and intermediate arithmetic must fit signed 64-bit integers; rotation counts, window sizes, and clamp limits are nonnegative.

This project uses automation to propose additional generated regression examples, with reviews and maintenance recorded in issues and pull requests.
