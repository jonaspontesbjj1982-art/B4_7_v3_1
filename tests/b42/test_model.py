import pytest

from b42.model import (
    ProbabilityModel,
    build_probability_model,
    classify_divergence,
)


def test_probability_model_basic():
    result = build_probability_model(
        statistical=0.60,
        contextual=0.60,
        market=0.60,
    )

    assert isinstance(result, ProbabilityModel)
    assert result.central == pytest.approx(0.60)
    assert result.interval_min == pytest.approx(0.60)
    assert result.interval_max == pytest.approx(0.60)
    assert result.divergence == pytest.approx(0.0)
    assert result.divergence_classification == "LOW"


def test_probability_model_interval():
    result = build_probability_model(
        statistical=0.55,
        contextual=0.65,
        market=0.60,
    )

    assert result.central == pytest.approx(0.60)
    assert result.interval_min == pytest.approx(0.55)
    assert result.interval_max == pytest.approx(0.65)
    assert result.divergence == pytest.approx(0.10)
    assert result.divergence_classification == "REVIEW"


def test_divergence_low():
    assert classify_divergence(0.03) == "LOW"


def test_divergence_attention():
    assert classify_divergence(0.04) == "ATTENTION"
    assert classify_divergence(0.06) == "ATTENTION"


def test_divergence_review():
    assert classify_divergence(0.07) == "REVIEW"
    assert classify_divergence(0.10) == "REVIEW"


def test_divergence_high():
    assert classify_divergence(0.1001) == "HIGH"


def test_probability_cannot_be_below_zero():
    with pytest.raises(ValueError):
        build_probability_model(
            statistical=-0.01,
            contextual=0.50,
            market=0.50,
        )


def test_probability_cannot_be_above_one():
    with pytest.raises(ValueError):
        build_probability_model(
            statistical=1.01,
            contextual=0.50,
            market=0.50,
        )


def test_probability_one_is_valid():
    result = build_probability_model(
        statistical=1.0,
        contextual=0.5,
        market=0.5,
    )

    assert result.central == pytest.approx(2.0 / 3.0)


def test_probability_zero_is_valid():
    result = build_probability_model(
        statistical=0.0,
        contextual=0.5,
        market=0.5,
    )

    assert result.central == pytest.approx(1.0 / 3.0)


def test_fair_probability_two_way_market():
    from b42.model import fair_probability_from_odds

    result = fair_probability_from_odds([2.00, 2.00])

    assert result[0] == pytest.approx(0.50)
    assert result[1] == pytest.approx(0.50)
    assert sum(result) == pytest.approx(1.0)


def test_fair_probability_three_way_market():
    from b42.model import fair_probability_from_odds

    result = fair_probability_from_odds([2.00, 3.00, 4.00])

    assert result[0] == pytest.approx(
        0.5 / (0.5 + 1 / 3 + 0.25)
    )
    assert result[1] == pytest.approx(
        (1 / 3) / (0.5 + 1 / 3 + 0.25)
    )
    assert result[2] == pytest.approx(
        0.25 / (0.5 + 1 / 3 + 0.25)
    )

    assert sum(result) == pytest.approx(1.0)


def test_fair_probability_removes_overround():
    from b42.model import fair_probability_from_odds

    result = fair_probability_from_odds([1.90, 1.90])

    assert sum(result) == pytest.approx(1.0)
    assert result[0] == pytest.approx(0.50)
    assert result[1] == pytest.approx(0.50)


def test_fair_probability_rejects_empty_list():
    from b42.model import fair_probability_from_odds

    with pytest.raises(ValueError):
        fair_probability_from_odds([])


def test_fair_probability_rejects_invalid_odd():
    from b42.model import fair_probability_from_odds

    with pytest.raises(ValueError):
        fair_probability_from_odds([2.00, 1.00])


def test_fair_probability_supports_many_outcomes():
    from b42.model import fair_probability_from_odds

    result = fair_probability_from_odds(
        [2.00, 3.00, 4.00, 5.00]
    )

    assert len(result) == 4
    assert sum(result) == pytest.approx(1.0)
