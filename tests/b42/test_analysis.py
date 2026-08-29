import pytest

from b42.analysis import analyze_market_outcome
from b42.types import MatchContext


def test_analysis_integrates_pricing_and_risk():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    result = analyze_market_outcome(
        event=event,
        market="Total de Gols",
        outcome="Over 2.5",
        probability=0.60,
        offered_odd=1.90,
        line=2.5,
    )

    assert result.event == event
    assert result.selected_outcome is not None

    assert result.selected_outcome.market == "Total de Gols"
    assert result.selected_outcome.outcome == "Over 2.5"
    assert result.selected_outcome.odd == pytest.approx(1.90)
    assert result.selected_outcome.line == pytest.approx(2.5)

    assert result.probability.central == pytest.approx(0.60)

    assert result.pricing.fair_odd == pytest.approx(1 / 0.60)
    assert result.pricing.offered_odd == pytest.approx(1.90)
    assert result.pricing.edge == pytest.approx(0.0736842105)
    assert result.pricing.ev == pytest.approx(0.14)

    assert result.risk.robustness == "ROBUSTA"
    assert len(result.risk.stress_tests) == 5

    assert result.decision.classification == "ENTRAR"


def test_analysis_can_evaluate_corners():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    result = analyze_market_outcome(
        event=event,
        market="Escanteios",
        outcome="Over 9.5",
        probability=0.58,
        offered_odd=1.90,
        line=9.5,
    )

    assert result.selected_outcome.market == "Escanteios"
    assert result.selected_outcome.line == pytest.approx(9.5)
    assert result.pricing.fair_odd == pytest.approx(1 / 0.58)


def test_analysis_can_evaluate_cards():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    result = analyze_market_outcome(
        event=event,
        market="Cartões",
        outcome="Over 4.5",
        probability=0.56,
        offered_odd=2.00,
        line=4.5,
    )

    assert result.selected_outcome.market == "Cartões"
    assert result.pricing.fair_odd == pytest.approx(1 / 0.56)


def test_analysis_rejects_invalid_probability():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    with pytest.raises(ValueError):
        analyze_market_outcome(
            event=event,
            market="Resultado",
            outcome="Casa",
            probability=1.10,
            offered_odd=2.00,
        )


def test_analysis_rejects_invalid_odd():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    with pytest.raises(ValueError):
        analyze_market_outcome(
            event=event,
            market="Resultado",
            outcome="Casa",
            probability=0.60,
            offered_odd=1.00,
        )
