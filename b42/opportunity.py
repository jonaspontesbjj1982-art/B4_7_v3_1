from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .edge import calculate_value_metrics
from .fragility import analyze_fragility


@dataclass(frozen=True)
class OpportunityResult:
    market: str
    outcome: str
    line: float | None

    probability: float
    market_probability: float

    fair_odd: float
    offered_odd: float

    edge: float
    ev: float

    worst_probability: float
    worst_ev: float

    robustness: str
    status: str

    stress_tests: tuple[dict[str, Any], ...]


def classify_opportunity(
    ev: float,
    robustness: str,
) -> str:
    """
    Classifica uma oportunidade sem impor odds mínimas fixas.

    O valor é determinado pela relação entre:
        - probabilidade do modelo
        - odd oferecida
        - EV
        - robustez

    Não existe uma odd mínima universal.
    """
    if ev <= 0.0:
        return "PASSA"

    if robustness == "ROBUSTA":
        return "VALOR_ROBUSTO"

    if robustness == "MODERADA":
        return "VALOR_MODERADO"

    if robustness == "FRÁGIL":
        return "VALOR_FRAGIL"

    return "REVISAR"


def evaluate_opportunity(
    market: str,
    outcome: str,
    probability: float,
    offered_odd: float,
    line: float | None = None,
    shocks: tuple[float, ...] = (
        -0.05,
        -0.03,
        0.0,
        0.03,
        0.05,
    ),
) -> OpportunityResult:
    """
    Avalia uma seleção de qualquer mercado.

    O motor não conhece regras específicas de futebol.
    Ele apenas avalia a relação matemática entre:

        probabilidade do modelo
        odd oferecida
        valor esperado
        robustez
    """

    metrics = calculate_value_metrics(
        probability=probability,
        odd=offered_odd,
    )

    fragility = analyze_fragility(
        probability=probability,
        odd=offered_odd,
        shocks=shocks,
    )

    stress_tests = tuple(
        {
            "probability": scenario.probability,
            "ev": scenario.ev,
        }
        for scenario in fragility.scenarios
    )

    status = classify_opportunity(
        ev=metrics.ev,
        robustness=fragility.classification,
    )

    return OpportunityResult(
        market=market,
        outcome=outcome,
        line=line,
        probability=metrics.probability,
        market_probability=metrics.market_probability,
        fair_odd=metrics.fair_odd,
        offered_odd=metrics.market_odd,
        edge=metrics.edge,
        ev=metrics.ev,
        worst_probability=fragility.worst_probability,
        worst_ev=fragility.worst_ev,
        robustness=fragility.classification,
        status=status,
        stress_tests=stress_tests,
    )
