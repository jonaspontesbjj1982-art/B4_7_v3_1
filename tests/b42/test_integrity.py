from b42.integrity import check_market_integrity
from b42.types import Market, MarketOutcome


def test_complete_three_way_market_is_valid():
    market = Market(
        name="Resultado",
        outcomes=[
            MarketOutcome("result", "home", 2.00),
            MarketOutcome("result", "draw", 3.20),
            MarketOutcome("result", "away", 3.50),
        ],
    )

    result = check_market_integrity(
        market,
        expected_outcomes=["home", "draw", "away"],
    )

    assert result.valid is True
    assert result.status == "VALID"
    assert result.missing_outcomes == []


def test_missing_outcome_requires_review():
    market = Market(
        name="Resultado",
        outcomes=[
            MarketOutcome("result", "home", 2.00),
            MarketOutcome("result", "draw", 3.20),
        ],
    )

    result = check_market_integrity(
        market,
        expected_outcomes=["home", "draw", "away"],
    )

    assert result.valid is False
    assert result.status == "REVIEW"
    assert result.missing_outcomes == ["away"]


def test_duplicate_outcome_is_blocked():
    market = Market(
        name="Resultado",
        outcomes=[
            MarketOutcome("result", "home", 2.00),
            MarketOutcome("result", "home", 2.10),
            MarketOutcome("result", "away", 3.50),
        ],
    )

    result = check_market_integrity(market)

    assert result.valid is False
    assert result.status == "BLOCKED"
    assert "home" in result.duplicate_outcomes


def test_empty_market_is_blocked():
    market = Market(
        name="Resultado",
        outcomes=[],
    )

    result = check_market_integrity(market)

    assert result.valid is False
    assert result.status == "BLOCKED"


def test_without_expected_outcomes_market_can_be_valid():
    market = Market(
        name="Mercado Aberto",
        outcomes=[
            MarketOutcome("custom", "option_a", 2.00),
            MarketOutcome("custom", "option_b", 2.00),
        ],
    )

    result = check_market_integrity(market)

    assert result.valid is True
    assert result.status == "VALID"
    assert result.expected_outcomes is None


def test_actual_outcome_count_is_preserved():
    market = Market(
        name="Escanteios",
        outcomes=[
            MarketOutcome("corners", "over", 1.90, line=8.5),
            MarketOutcome("corners", "under", 1.90, line=8.5),
        ],
    )

    result = check_market_integrity(market)

    assert result.actual_outcomes == 2
