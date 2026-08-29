from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .edge import ev_from_probability_and_odd


@dataclass(frozen=True)
class StressScenario:
    probability: float
    ev: float


@dataclass(frozen=True)
class FragilityResult:
    base_probability: float
    market_odd: float
    base_ev: float
    scenarios: Tuple[StressScenario, ...]
    worst_probability: float
    worst_ev: float
    classification: str
    robust: bool


def _validate_probability(probability: float) -> float:
    try:
        value = float(probability)
    except (TypeError, ValueError) as exc:
        raise ValueError("probability must be numeric") from exc

    if not 0.0 < value <= 1.0:
        raise ValueError("probability must be greater than 0 and at most 1")

    return value


def _validate_odd(odd: float) -> float:
    try:
        value = float(odd)
    except (TypeError, ValueError) as exc:
        raise ValueError("odd must be numeric") from exc

    if value <= 1.0:
        raise ValueError("odd must be greater than 1")

    return value


def stress_probabilities(
    probability: float,
    shocks: tuple[float, ...] = (-0.05, -0.03, 0.0, 0.03, 0.05),
) -> Tuple[float, ...]:
    """
    Gera cenários de estresse em torno da probabilidade central.

    Os shocks são absolutos:
        -0.05 = -5 pontos percentuais
        +0.05 = +5 pontos percentuais
    """
    probability = _validate_probability(probability)

    scenarios = []

    for shock in shocks:
        value = probability + float(shock)

        # Mantém a probabilidade dentro do domínio válido.
        value = max(0.000001, min(1.0, value))

        scenarios.append(value)

    return tuple(scenarios)


def classify_fragility(
    base_ev: float,
    worst_ev: float,
) -> str:
    """
    Classifica a estabilidade do valor.

    ROBUSTA:
        EV continua positivo no pior cenário.

    MODERADA:
        EV positivo no cenário central, mas negativo sob
        estresse relevante.

    FRÁGIL:
        EV central positivo, porém o valor desaparece com
        pequeno estresse.

    PASSA:
        EV central não é positivo.
    """
    if base_ev <= 0.0:
        return "PASSA"

    if worst_ev > 0.0:
        return "ROBUSTA"

    # Diferença entre o EV central e o pior cenário.
    deterioration = base_ev - worst_ev

    if deterioration <= base_ev * 1.50:
        return "MODERADA"

    return "FRÁGIL"


def analyze_fragility(
    probability: float,
    odd: float,
    shocks: tuple[float, ...] = (-0.05, -0.03, 0.0, 0.03, 0.05),
) -> FragilityResult:
    """
    Executa o stress test completo de uma seleção.
    """
    probability = _validate_probability(probability)
    odd = _validate_odd(odd)

    base_ev = ev_from_probability_and_odd(probability, odd)

    probabilities = stress_probabilities(
        probability,
        shocks=shocks,
    )

    scenarios = tuple(
        StressScenario(
            probability=p,
            ev=ev_from_probability_and_odd(p, odd),
        )
        for p in probabilities
    )

    worst_scenario = min(
        scenarios,
        key=lambda scenario: scenario.ev,
    )

    classification = classify_fragility(
        base_ev=base_ev,
        worst_ev=worst_scenario.ev,
    )

    return FragilityResult(
        base_probability=probability,
        market_odd=odd,
        base_ev=base_ev,
        scenarios=scenarios,
        worst_probability=worst_scenario.probability,
        worst_ev=worst_scenario.ev,
        classification=classification,
        robust=classification == "ROBUSTA",
    )
