from __future__ import annotations

from .opportunity import evaluate_opportunity
from .decision import classify_decision
from .quality import calculate_qi
from .types import (
    B42Analysis,
    Market,
    MarketOutcome,
    MatchContext,
)


def analyze_market_outcome(
    event: MatchContext,
    market: str,
    outcome: str,
    probability: float,
    offered_odd: float,
    line: float | None = None,
    mode: str | None = None,
    data_quality: float = 80.0,
    relevance: float = 80.0,
    freshness: float = 80.0,
    consistency: float = 80.0,
) -> B42Analysis:
    """
    Integra uma avaliação completa de mercado ao B42Analysis.

    Fluxo:

        probabilidade
        fair odd
        edge
        EV
        fragilidade
        qualidade dos dados (QI)
        decisão

    O motor não utiliza odd mínima fixa.

    Os componentes de qualidade são explícitos e podem ser
    substituídos por dados reais posteriormente.
    """

    opportunity = evaluate_opportunity(
        market=market,
        outcome=outcome,
        probability=probability,
        offered_odd=offered_odd,
        line=line,
    )

    qi_assessment = calculate_qi(
        data_quality=data_quality,
        relevance=relevance,
        freshness=freshness,
        consistency=consistency,
    )

    selected_outcome = MarketOutcome(
        market=market,
        outcome=outcome,
        odd=offered_odd,
        line=line,
    )

    selected_market = Market(
        name=market,
        outcomes=[selected_outcome],
    )

    analysis = B42Analysis(
        event=event,
        selected_market=selected_market,
        selected_outcome=selected_outcome,
        mode=mode or event.status,
    )

    analysis.data_quality.qi = qi_assessment.score
    analysis.data_quality.sample_status = (
        qi_assessment.classification
    )

    analysis.probability.central = probability
    analysis.probability.interval_low = opportunity.worst_probability
    analysis.probability.interval_high = probability

    analysis.pricing.fair_odd = opportunity.fair_odd
    analysis.pricing.offered_odd = opportunity.offered_odd
    analysis.pricing.market_fair_probability = (
        opportunity.market_probability
    )
    analysis.pricing.conservative_probability = (
        opportunity.worst_probability
    )
    analysis.pricing.edge = opportunity.edge
    analysis.pricing.ev = opportunity.ev

    analysis.risk.robustness = opportunity.robustness
    analysis.risk.stress_tests = list(
        opportunity.stress_tests
    )

    decision = classify_decision(
        ev=opportunity.ev,
        edge=opportunity.edge,
        robustness=opportunity.robustness,
        qi=qi_assessment.score,
    )

    analysis.decision.classification = decision.classification
    analysis.decision.reason = decision.reason

    analysis.ranking_score = opportunity.ev

    return analysis
