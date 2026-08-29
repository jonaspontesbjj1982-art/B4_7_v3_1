from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .fair_odds import (
    fair_odd_from_probability,
    fair_probability_from_odd,
)


@dataclass(frozen=True)
class ValueMetrics:
    probability: float
    market_probability: float
    fair_odd: float
    market_odd: float
    edge: float
    ev: float


def validate_market_odd(odd: float) -> float:
    try:
        value = float(odd)
    except (TypeError, ValueError) as exc:
        raise ValueError("odd must be numeric") from exc

    if not isfinite(value):
        raise ValueError("odd must be finite")

    if value <= 1.0:
        raise ValueError("odd must be greater than 1")

    return value


def edge_from_probability_and_odd(
    probability: float,
    odd: float,
) -> float:
    """
    Calcula o Edge de uma seleção individual.

    Edge = probabilidade do modelo
           - probabilidade implícita da odd.

    A probabilidade implícita individual é:

        1 / odd
    """
    odd = validate_market_odd(odd)

    fair_odd = fair_odd_from_probability(probability)
    _ = fair_odd

    market_probability = fair_probability_from_odd(odd)

    return probability - market_probability


def ev_from_probability_and_odd(
    probability: float,
    odd: float,
) -> float:
    """
    Calcula o EV esperado por unidade apostada.

    EV = (probabilidade × odd) - 1
    """
    odd = validate_market_odd(odd)

    fair_odd = fair_odd_from_probability(probability)
    _ = fair_odd

    return (probability * odd) - 1.0


def calculate_value_metrics(
    probability: float,
    odd: float,
) -> ValueMetrics:
    """
    Calcula todas as métricas de valor de uma seleção individual.
    """
    odd = validate_market_odd(odd)

    fair_odd = fair_odd_from_probability(probability)
    market_probability = fair_probability_from_odd(odd)

    edge = probability - market_probability
    ev = (probability * odd) - 1.0

    return ValueMetrics(
        probability=float(probability),
        market_probability=float(market_probability),
        fair_odd=float(fair_odd),
        market_odd=float(odd),
        edge=float(edge),
        ev=float(ev),
    )
