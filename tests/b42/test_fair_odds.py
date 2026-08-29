import pytest

from b42.fair_odds import (
    fair_odd_from_probability,
    fair_probability_from_odd,
    validate_probability,
)


def test_fair_odd_from_probability():
    assert fair_odd_from_probability(0.50) == pytest.approx(2.00)


def test_fair_odd_from_probability_60_percent():
    assert fair_odd_from_probability(0.60) == pytest.approx(1.6666666667)


def test_fair_odd_from_probability_25_percent():
    assert fair_odd_from_probability(0.25) == pytest.approx(4.00)


def test_fair_probability_from_odd():
    assert fair_probability_from_odd(2.00) == pytest.approx(0.50)


def test_probability_validation():
    assert validate_probability(0.75) == pytest.approx(0.75)


@pytest.mark.parametrize(
    "probability",
    [0, -0.1, 1.1, float("inf"), float("nan")],
)
def test_invalid_probability(probability):
    with pytest.raises(ValueError):
        validate_probability(probability)


@pytest.mark.parametrize(
    "odd",
    [0, 1, 0.5, float("inf"), float("nan")],
)
def test_invalid_odd(odd):
    with pytest.raises(ValueError):
        fair_probability_from_odd(odd)
