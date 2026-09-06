"""Generate bounded integer regression examples in the notebook languages."""

from itertools import accumulate, groupby

def expected(operation, values, argument):
    if operation == "sum": return [sum(values)]
    if operation == "prefix": return list(accumulate(values))
    if operation == "diff": return [values[i] - values[i - 1] for i in range(1, len(values))]
    if operation == "unique": return sorted(set(values))
    if operation == "runs":
        return [item for value, group in groupby(values) for item in (value, len(list(group)))]
    if operation == "rotate":
        shift = argument % len(values) if values else 0
        return values[shift:] + values[:shift]
    if operation == "windows":
        return [sum(values[i:i + argument]) for i in range(len(values) - argument + 1)] if argument else []
    if operation == "bound": return [sum(value < argument for value in values)]
    if operation == "clamp": return [min(argument, max(-argument, value)) for value in values]
    if operation == "reverse": return values[::-1]
    raise ValueError(operation)


def new_case(rng, seen):
    while True:
        operation = rng.choice(["sum", "prefix", "diff", "unique", "runs", "rotate", "windows", "bound", "clamp", "reverse"])
        scenario = rng.choice(["mixed signs", "ascending values", "descending values", "duplicate values",
                               "alternating signs", "sparse values", "constant input", "wide values", "short input"])
        n = rng.randint(2, 22)
        values = [rng.randint(-80, 80) for _ in range(n)]
        if scenario == "ascending values": values.sort()
        elif scenario == "descending values": values.sort(reverse=True)
        elif scenario == "duplicate values": values = [rng.choice(values[:3]) for _ in values]
        elif scenario == "alternating signs": values = [abs(v) * (1 if i % 2 else -1) for i, v in enumerate(values)]
        elif scenario == "sparse values": values = [v if rng.random() < .2 else 0 for v in values]
        elif scenario == "constant input": values = [values[0]] * n
        elif scenario == "wide values": values = [v * rng.randint(10000, 1000000) for v in values]
        elif scenario == "short input": values = values[:rng.randint(0, 3)]
        argument = 0
        if operation in ("rotate", "windows"): argument = rng.randint(0, len(values) + 8)
        if operation == "bound": argument = rng.randint(-90, 90)
        if operation == "clamp": argument = rng.randint(0, 90)
        signature = (operation, tuple(values), argument)
        if signature not in seen:
            seen.add(signature)
            return operation, values, argument, expected(operation, values, argument), scenario

