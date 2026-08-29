import pytest

from b42.decision import (
    DecisionAssessment,
    classify_decision,
)


def test_positive_robust_value_is_entry():
    result = classify_decision(
        ev=0.10,
        edge=0.05,
        robustness="ROBUSTA",
        qi=90,
    )

    assert isinstance(result, DecisionAssessment)
    assert result.classification == "ENTRAR"


def test_positive_moderate_value_requires_review():
    result = classify_decision(
        ev=0.08,
        edge=0.04,
        robustness="MODERADA",
        qi=75,
    )

    assert result.classification == "REVISAR"


def test_fragile_value_is_not_entry():
    result = classify_decision(
        ev=0.10,
        edge=0.05,
        robustness="FRÁGIL",
        qi=90,
    )

    assert result.classification == "REVISAR"


def test_non_positive_ev_is_pass():
    result = classify_decision(
        ev=0.0,
        edge=0.00,
        robustness="ROBUSTA",
        qi=90,
    )

    assert result.classification == "PASSA"


def test_negative_ev_is_pass():
    result = classify_decision(
        ev=-0.05,
        edge=-0.02,
        robustness="ROBUSTA",
        qi=90,
    )

    assert result.classification == "PASSA"


def test_low_qi_blocks_entry():
    result = classify_decision(
        ev=0.15,
        edge=0.08,
        robustness="ROBUSTA",
        qi=60,
    )

    assert result.classification == "REVISAR"


@pytest.mark.parametrize(
    "robustness",
    ["ROBUSTA", "MODERADA", "FRÁGIL", "PASSA", "UNKNOWN"],
)
def test_supported_robustness_values(robustness):
    result = classify_decision(
        ev=0.05,
        edge=0.03,
        robustness=robustness,
        qi=80,
    )

    assert isinstance(result.classification, str)
