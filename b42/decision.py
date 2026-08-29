from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionAssessment:
    classification: str
    reason: str


def classify_decision(
    ev: float,
    edge: float,
    robustness: str,
    qi: float,
) -> DecisionAssessment:
    """
    Camada de decisão do B4.2.

    A decisão considera conjuntamente:

        EV
        Edge
        robustez
        qualidade dos dados (QI)

    Não utiliza odd mínima fixa.
    """

    if ev <= 0.0:
        return DecisionAssessment(
            classification="PASSA",
            reason="EV não positivo.",
        )

    if edge <= 0.0:
        return DecisionAssessment(
            classification="PASSA",
            reason="Edge não positivo.",
        )

    if qi < 65:
        return DecisionAssessment(
            classification="REVISAR",
            reason="Qualidade dos dados insuficiente.",
        )

    if robustness == "ROBUSTA" and qi >= 80:
        return DecisionAssessment(
            classification="ENTRAR",
            reason="Valor positivo, robustez alta e QI premium.",
        )

    return DecisionAssessment(
        classification="REVISAR",
        reason="Existe valor matemático, mas há fatores que exigem revisão.",
    )
