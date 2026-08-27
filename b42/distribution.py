from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median
from typing import Sequence


@dataclass
class DistributionSummary:
    sample_size: int
    mean: float | None
    median: float | None
    p25: float | None
    p75: float | None
    minimum: float | None
    maximum: float | None
    frequencies: dict[float, int]


def percentile(values: Sequence[float], percentage: float) -> float | None:
    if not values:
        return None

    ordered = sorted(values)

    if len(ordered) == 1:
        return ordered[0]

    position = (len(ordered) - 1) * percentage
    lower = int(position)
    upper = lower + 1

    if upper >= len(ordered):
        return ordered[lower]

    weight = position - lower

    return (
        ordered[lower]
        + (ordered[upper] - ordered[lower]) * weight
    )


def summarize_distribution(
    values: Sequence[float],
) -> DistributionSummary:
    data = list(values)

    if not data:
        return DistributionSummary(
            sample_size=0,
            mean=None,
            median=None,
            p25=None,
            p75=None,
            minimum=None,
            maximum=None,
            frequencies={},
        )

    frequencies: dict[float, int] = {}

    for value in data:
        frequencies[value] = frequencies.get(value, 0) + 1

    return DistributionSummary(
        sample_size=len(data),
        mean=mean(data),
        median=median(data),
        p25=percentile(data, 0.25),
        p75=percentile(data, 0.75),
        minimum=min(data),
        maximum=max(data),
        frequencies=frequencies,
    )
