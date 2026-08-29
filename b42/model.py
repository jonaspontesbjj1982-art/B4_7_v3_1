from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProbabilityModel:
    statistical: float
    contextual: float
    market: float

    central: float
    interval_min: float
    interval_max: float

    divergence: float
    divergence_classification: str


def _validate_probability(value: float, name: str) -> None:
    if value < 0 or value > 1:
        raise ValueError(
            f"{name} deve estar entre 0 e 1."
        )


def classify_divergence(divergence: float) -> str:
    if divergence <= 0.03:
        return "LOW"

    if divergence <= 0.06:
        return "ATTENTION"

    if divergence <= 0.10:
        return "REVIEW"

    return "HIGH"


def build_probability_model(
    statistical: float,
    contextual: float,
    market: float,
) -> ProbabilityModel:
    _validate_probability(statistical, "Probabilidade estatística")
    _validate_probability(contextual, "Probabilidade contextual")
    _validate_probability(market, "Probabilidade de mercado")

    values = (
        statistical,
        contextual,
        market,
    )

    central = sum(values) / 3.0

    interval_min = min(values)
    interval_max = max(values)

    divergence = max(values) - min(values)

    return ProbabilityModel(
        statistical=statistical,
        contextual=contextual,
        market=market,
        central=central,
        interval_min=interval_min,
        interval_max=interval_max,
        divergence=divergence,
        divergence_classification=classify_divergence(
            divergence
        ),
    )


def fair_probability_from_odds(odds: list[float]) -> list[float]:
    """
    Converte odds de todos os desfechos de um mercado
    em probabilidades implícitas justas, removendo o overround.

    Fórmula:
        P_i = (1 / odd_i) / sum(1 / odd_j)
    """

    if not odds:
        raise ValueError("A lista de odds não pode ser vazia.")

    if any(odd <= 1.0 for odd in odds):
        raise ValueError("Todas as odds devem ser superiores a 1.0.")

    inverse = [1.0 / odd for odd in odds]
    total = sum(inverse)

    if total <= 0:
        raise ValueError(
            "Soma das probabilidades implícitas inválida."
        )

    return [
        value / total
        for value in inverse
    ]
