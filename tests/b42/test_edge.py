import pytest

from b42.edge import (
    calculate_value_metrics,
    edge_from_probability_and_odd,
    ev_from_probability_and_odd,
    validate_market_odd,
)


def test_edge_positive():
    edge = edge_from_probability_and_odd(0.60, 1.90)
    assert edge == pytest.approx(0.0736842105)


def test_edge_zero_when_market_equals_model():
    edge = edge_from_probability_and_odd(0.50, 2.00)
    assert edge == pytest.approx(0.0)


def test_edge_negative():
    edge = edge_from_probability_and_odd(0.50, 1.80)
    assert edge == pytest.approx(-0.0555555556)


def test_ev_positive():
    ev = ev_from_probability_and_odd(0.60, 1.90)
    assert ev == pytest.approx(0.14)


def test_ev_zero_when_fair():
    ev = ev_from_probability_and_odd(0.50, 2.00)
    assert ev == pytest.approx(0.0)


def test_ev_negative():
    ev = ev_from_probability_and_odd(0.50, 1.80)
    assert ev == pytest.approx(-0.10)


def test_complete_value_metrics():
    metrics = calculate_value_metrics(0.60, 1.90)

    assert metrics.probability == pytest.approx(0.60)
    assert metrics.market_probability == pytest.approx(1 / 1.90)
    assert metrics.fair_odd == pytest.approx(1 / 0.60)
    assert metrics.market_odd == pytest.approx(1.90)
    assert metrics.edge == pytest.approx(0.0736842105)
    assert metrics.ev == pytest.approx(0.14)


def test_market_odd_validation():
    assert validate_market_odd(1.90) == pytest.approx(1.90)


@pytest.mark.parametrize(
    "odd",
    [0, 1, 0.5, float("inf"), float("nan")],
)
def test_invalid_market_odd(odd):
    with pytest.raises(ValueError):
        validate_market_odd(odd)


def test_invalid_probability():
    with pytest.raises(ValueError):
        edge_from_probability_and_odd(0, 2.00)


def test_invalid_probability_for_ev():
    with pytest.raises(ValueError):
        ev_from_probability_and_odd(1.1, 2.00)
