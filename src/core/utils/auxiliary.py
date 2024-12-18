from math import copysign


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sgn_round(val: float) -> int:
    return int(copysign(round(abs(val)), val))
