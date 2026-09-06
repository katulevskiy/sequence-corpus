"""Standard-library sequence exercises using an integer-vector interface."""

from itertools import accumulate, groupby


def evaluate(operation, values, argument=0):
    """Return a list of integers for the requested sequence operation.

    Window widths, rotation counts and clamp limits are nonnegative. Values in
    the shared examples stay within the signed 64-bit arithmetic contract used
    by the Rust and C++ implementations.
    """
    if operation == "sum":
        return [sum(values)]
    if operation == "prefix":
        return list(accumulate(values))
    if operation == "diff":
        return [right - left for left, right in zip(values, values[1:])]
    if operation == "unique":
        return sorted(set(values))
    if operation == "runs":
        result = []
        for value, group in groupby(values):
            result.extend((value, sum(1 for _ in group)))
        return result
    if operation == "rotate":
        if argument < 0:
            raise ValueError("rotation must be nonnegative")
        if not values:
            return []
        shift = argument % len(values)
        return list(values[shift:]) + list(values[:shift])
    if operation == "windows":
        if argument < 0:
            raise ValueError("window must be nonnegative")
        if not argument or argument > len(values):
            return []
        return [sum(values[start:start + argument])
                for start in range(len(values) - argument + 1)]
    if operation == "bound":
        return [sum(value < argument for value in values)]
    if operation == "clamp":
        if argument < 0:
            raise ValueError("clamp limit must be nonnegative")
        return [min(argument, max(-argument, value)) for value in values]
    if operation == "reverse":
        return list(reversed(values))
    raise ValueError("unknown operation: " + operation)
