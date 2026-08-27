import pytest

from b42.markets import (
    fair_market_probabilities,
    scan_all_markets,
    scan_market,
    validate_market,
)
from b42.types import Market, MarketOutcome


def test_validate_market():
    market = Market(
        name="Total de Gols",
        outcomes=[
            MarketOutcome("goals", "over", 2.00, line=2.5),
            MarketOutcome("goals", "under", 1.80, line=2.5),
        ],
    )

    validate_market(market)


def test_invalid_odd():
    market = Market(
        name="Total de Gols",
        outcomes=[
            MarketOutcome("goals", "over", 1.00, line=2.5),
        ],
    )

    with pytest.raises(ValueError):
        validate_market(market)


def test_fair_probabilities_sum_to_one():
    outcomes = [
        MarketOutcome("result", "home", 2.00),
        MarketOutcome("result", "draw", 3.00),
        MarketOutcome("result", "away", 4.00),
    ]

    probabilities = fair_market_probabilities(outcomes)

    assert sum(probabilities.values()) == pytest.approx(1.0)


def test_scan_market():
    market = Market(
        name="Total de Gols",
        outcomes=[
            MarketOutcome("goals", "over", 2.00, line=2.5),
            MarketOutcome("goals", "under", 1.80, line=2.5),
        ],
    )

    result = scan_market(market)

    assert len(result) == 2
    assert all(item.fair_market_probability > 0 for item in result)


def test_universal_scan_accepts_multiple_markets_and_lines():
    markets = [
        Market(
            name="Total de Gols",
            outcomes=[
                MarketOutcome("goals", "over", 2.00, line=1.5),
                MarketOutcome("goals", "under", 1.90, line=1.5),
            ],
        ),
        Market(
            name="Total de Gols",
            outcomes=[
                MarketOutcome("goals", "over", 2.10, line=2.5),
                MarketOutcome("goals", "under", 1.75, line=2.5),
            ],
        ),
        Market(
            name="Escanteios",
            outcomes=[
                MarketOutcome("corners", "over", 1.90, line=8.5),
                MarketOutcome("corners", "under", 1.90, line=8.5),
            ],
        ),
        Market(
            name="Resultado",
            outcomes=[
                MarketOutcome("result", "home", 2.10),
                MarketOutcome("result", "draw", 3.20),
                MarketOutcome("result", "away", 3.50),
            ],
        ),
    ]

    result = scan_all_markets(markets)

    assert len(result) == 9

    market_names = {item.market for item in result}

    assert "Total de Gols" in market_names
    assert "Escanteios" in market_names
    assert "Resultado" in market_names

    lines = {
        item.line
        for item in result
        if item.market == "Total de Gols"
    }

    assert 1.5 in lines
    assert 2.5 in lines


def test_ranking_score_is_generated():
    market = Market(
        name="Resultado",
        outcomes=[
            MarketOutcome("result", "home", 2.00),
            MarketOutcome("result", "draw", 3.00),
            MarketOutcome("result", "away", 4.00),
        ],
    )

    result = scan_all_markets([market])

    assert all(item.rank_score > 0 for item in result)
