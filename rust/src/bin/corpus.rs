use std::io::{self, BufRead};
use sequence_notebook::evaluate;

fn numbers(text: &str) -> Result<Vec<i64>, std::num::ParseIntError> {
    if text.is_empty() { return Ok(Vec::new()); }
    text.split(',').map(str::parse).collect()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut count = 0;
    for line in io::stdin().lock().lines() {
        let line = line?;
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 { return Err("expected four tab-separated fields".into()); }
        let actual = evaluate(fields[0], &numbers(fields[2])?, fields[1].parse()?);
        let expected = numbers(fields[3])?;
        if actual != expected {
            return Err(format!("corpus row {}: {:?} != {:?}", count + 1, actual, expected).into());
        }
        count += 1;
    }
    println!("Rust: {} corpus cases passed", count);
    Ok(())
}
