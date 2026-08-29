import pytest

from b42.fragility import (
    analyze_fragility,
    classify_fragility,
    stress_probabilities,
)


def test_stress_probabilities():
    result = stress_probabilities(0.60)

    assert result == pytest.approx(
        (0.55, 0.57, 0.60, 0.63, 0.65)
    )


def test_stress_probability_bounds():
    result = stress_probabilities(
        0.02,
        shocks=(-0.05, 0.0, 0.05),
    )

    assert result[0] > 0
    assert result[1] == pytest.approx(0.02)
    assert result[2] == pytest.approx(0.07)


def test_robust_opportunity():
    result = analyze_fragility(0.60, 1.90)

    assert result.base_ev == pytest.approx(0.14)
    assert result.worst_probability == pytest.approx(0.55)
    assert result.worst_ev == pytest.approx(0.045)
    assert result.classification == "ROBUSTA"
    assert result.robust is True


def test_pass_when_base_ev_is_negative():
    result = analyze_fragility(0.50, 1.80)

    assert result.base_ev == pytest.approx(-0.10)
    assert result.classification == "PASSA"
    assert result.robust is False


def test_moderate_classification():
    assert classify_fragility(0.10, -0.02) == "MODERADA"


def test_fragile_classification():
    assert classify_fragility(0.05, -0.10) == "FRÁGIL"


def test_scenarios_have_ev():
    result = analyze_fragility(0.60, 1.90)

    assert len(result.scenarios) == 5

    for scenario in result.scenarios:
        assert scenario.probability > 0
        assert isinstance(scenario.ev, float)


def test_custom_shocks():
    result = analyze_fragility(
        0.60,
        2.00,
        shocks=(-0.02, 0.0, 0.02),
    )

    assert len(result.scenarios) == 3
    assert result.scenarios[0].probability == pytest.approx(0.58)
    assert result.scenarios[1].probability == pytest.approx(0.60)
    assert result.scenarios[2].probability == pytest.approx(0.62)


@pytest.mark.parametrize(
    "probability",
    [0, -0.1, 1.1],
)
def test_invalid_probability(probability):
    with pytest.raises(ValueError):
        analyze_fragility(probability, 2.00)


@pytest.mark.parametrize(
    "odd",
    [0, 1, 0.9],
)
def test_invalid_odd(odd):
    with pytest.raises(ValueError):
        analyze_fragility(0.60, odd)
