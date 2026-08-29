import pytest

from b42.opportunity import (
    classify_opportunity,
    evaluate_opportunity,
)


def test_robust_value_opportunity():
    result = evaluate_opportunity(
        market="Over/Under 2.5",
        outcome="Over 2.5",
        probability=0.60,
        offered_odd=1.90,
        line=2.5,
    )

    assert result.market == "Over/Under 2.5"
    assert result.outcome == "Over 2.5"
    assert result.line == pytest.approx(2.5)

    assert result.probability == pytest.approx(0.60)
    assert result.market_probability == pytest.approx(1 / 1.90)
    assert result.fair_odd == pytest.approx(1 / 0.60)
    assert result.offered_odd == pytest.approx(1.90)

    assert result.edge == pytest.approx(0.0736842105)
    assert result.ev == pytest.approx(0.14)

    assert result.worst_probability == pytest.approx(0.55)
    assert result.worst_ev == pytest.approx(0.045)

    assert result.robustness == "ROBUSTA"
    assert result.status == "VALOR_ROBUSTO"

    assert len(result.stress_tests) == 5


def test_pass_when_ev_is_negative():
    result = evaluate_opportunity(
        market="Resultado",
        outcome="Casa",
        probability=0.50,
        offered_odd=1.80,
    )

    assert result.ev == pytest.approx(-0.10)
    assert result.status == "PASSA"


def test_moderate_value_classification():
    assert classify_opportunity(
        ev=0.05,
        robustness="MODERADA",
    ) == "VALOR_MODERADO"


def test_fragile_value_classification():
    assert classify_opportunity(
        ev=0.05,
        robustness="FRÁGIL",
    ) == "VALOR_FRAGIL"


def test_zero_ev_is_pass():
    assert classify_opportunity(
        ev=0.0,
        robustness="ROBUSTA",
    ) == "PASSA"


def test_universal_corner_market():
    result = evaluate_opportunity(
        market="Escanteios",
        outcome="Over 9.5",
        probability=0.58,
        offered_odd=1.90,
        line=9.5,
    )

    assert result.market == "Escanteios"
    assert result.outcome == "Over 9.5"
    assert result.line == pytest.approx(9.5)
    assert result.fair_odd == pytest.approx(1 / 0.58)


def test_universal_cards_market():
    result = evaluate_opportunity(
        market="Cartões",
        outcome="Over 4.5",
        probability=0.56,
        offered_odd=2.00,
        line=4.5,
    )

    assert result.market == "Cartões"
    assert result.outcome == "Over 4.5"
    assert result.line == pytest.approx(4.5)


def test_universal_player_market():
    result = evaluate_opportunity(
        market="Jogadores",
        outcome="Jogador marcar",
        probability=0.42,
        offered_odd=2.60,
    )

    assert result.market == "Jogadores"
    assert result.outcome == "Jogador marcar"
    assert result.line is None
    assert result.fair_odd == pytest.approx(1 / 0.42)
