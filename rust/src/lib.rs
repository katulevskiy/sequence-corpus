//! Integer sequence exercises with a common, allocation-based interface.

/// Compute an operation on a sequence of signed integers.
///
/// Arithmetic assumes intermediate values fit in `i64`. Window sizes and
/// rotation counts must be nonnegative. An unknown operation is a caller error.
pub fn evaluate(operation: &str, values: &[i64], argument: i64) -> Vec<i64> {
    match operation {
        "sum" => vec![values.iter().sum()],
        "prefix" => {
            let mut total = 0;
            values.iter().map(|value| {
                total += value;
                total
            }).collect()
        }
        "diff" => values.windows(2).map(|pair| pair[1] - pair[0]).collect(),
        "unique" => {
            let mut result = values.to_vec();
            result.sort_unstable();
            result.dedup();
            result
        }
        "runs" => {
            let mut result = Vec::new();
            for &value in values {
                let size = result.len();
                if size > 0 && result[size - 2] == value {
                    result[size - 1] += 1;
                } else {
                    result.push(value);
                    result.push(1);
                }
            }
            result
        }
        "rotate" => {
            assert!(argument >= 0, "rotation must be nonnegative");
            let mut result = values.to_vec();
            if !result.is_empty() {
                let shift = argument as usize % result.len();
                result.rotate_left(shift);
            }
            result
        }
        "windows" => {
            assert!(argument >= 0, "window must be nonnegative");
            let width = argument as usize;
            if width == 0 || width > values.len() {
                return Vec::new();
            }
            let mut total: i64 = values[..width].iter().sum();
            let mut result = vec![total];
            for index in width..values.len() {
                total += values[index] - values[index - width];
                result.push(total);
            }
            result
        }
        "bound" => vec![values.iter().filter(|&&value| value < argument).count() as i64],
        "clamp" => {
            assert!(argument >= 0, "clamp limit must be nonnegative");
            values.iter().map(|&value| value.max(-argument).min(argument)).collect()
        }
        "reverse" => values.iter().rev().copied().collect(),
        _ => panic!("unknown operation: {}", operation),
    }
}

#[cfg(test)]
mod tests {
    use super::evaluate;

    #[test]
    fn empty_sequences_have_defined_results() {
        assert_eq!(evaluate("sum", &[], 0), vec![0]);
        assert_eq!(evaluate("bound", &[], 8), vec![0]);
        for operation in &["prefix", "diff", "unique", "runs", "rotate", "windows", "clamp", "reverse"] {
            assert!(evaluate(operation, &[], 0).is_empty());
        }
    }

    #[test]
    fn rotation_and_differences_preserve_expected_relations() {
        let input = [3, -2, 9, 9];
        assert_eq!(evaluate("rotate", &input, 4), input);
        let prefix = evaluate("prefix", &input, 0);
        assert_eq!(evaluate("diff", &prefix, 0), input[1..]);
    }

    #[test]
    fn windows_include_both_endpoints() {
        assert_eq!(evaluate("windows", &[2, 4, 6, 8], 2), vec![6, 10, 14]);
        assert_eq!(evaluate("windows", &[2, 4, 6, 8], 4), vec![20]);
        assert!(evaluate("windows", &[2, 4], 3).is_empty());
    }
}
