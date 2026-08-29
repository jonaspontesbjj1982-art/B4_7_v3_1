import pytest

from b42.analysis import analyze_market_outcome
from b42.types import MatchContext


def test_analysis_propagates_robust_entry_decision():
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

    assert result.decision.classification == "ENTRAR"
    assert result.pricing.fair_odd == pytest.approx(1 / 0.60)
    assert result.pricing.edge == pytest.approx(0.0736842105)
    assert result.pricing.ev == pytest.approx(0.14)


def test_analysis_propagates_pass_decision():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    result = analyze_market_outcome(
        event=event,
        market="Cartões",
        outcome="Over 4.5",
        probability=0.50,
        offered_odd=1.80,
        line=4.5,
    )

    assert result.decision.classification == "PASSA"


def test_analysis_propagates_review_for_low_qi():
    event = MatchContext(
        home_team="Team A",
        away_team="Team B",
    )

    result = analyze_market_outcome(
        event=event,
        market="Escanteios",
        outcome="Over 8.5",
        probability=0.60,
        offered_odd=1.90,
        line=8.5,
    )

    assert result.decision.classification in {
        "ENTRAR",
        "REVISAR",
        "PASSA",
    }


def test_analysis_uses_explicit_qi_for_entry():
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
        data_quality=90,
        relevance=90,
        freshness=90,
        consistency=90,
    )

    assert result.data_quality.qi == pytest.approx(90.0)
    assert result.decision.classification == "ENTRAR"


def test_analysis_blocks_entry_with_low_qi():
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
        data_quality=50,
        relevance=50,
        freshness=50,
        consistency=50,
    )

    assert result.data_quality.qi == pytest.approx(50.0)
    assert result.decision.classification == "REVISAR"


def test_analysis_preserves_qi_boundary():
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
        data_quality=65,
        relevance=65,
        freshness=65,
        consistency=65,
    )

    assert result.data_quality.qi == pytest.approx(65.0)
    assert result.decision.classification == "REVISAR"
