import pytest

from b42.quotes import validate_quote
from b42.types import MarketOutcome


def test_valid_quote():
    quote = MarketOutcome(
        market="goals",
        outcome="over",
        odd=2.00,
        line=2.5,
    )

    result = validate_quote(quote)

    assert result.valid is True
    assert result.status == "VALID"
    assert result.errors == []


def test_invalid_odd():
    quote = MarketOutcome(
        market="goals",
        outcome="over",
        odd=1.00,
        line=2.5,
    )

    result = validate_quote(quote)

    assert result.valid is False
    assert result.status == "BLOCKED"


def test_empty_market():
    quote = MarketOutcome(
        market="",
        outcome="over",
        odd=2.00,
        line=2.5,
    )

    result = validate_quote(quote)

    assert result.valid is False
    assert "Mercado não informado." in result.errors


def test_empty_outcome():
    quote = MarketOutcome(
        market="goals",
        outcome="",
        odd=2.00,
        line=2.5,
    )

    result = validate_quote(quote)

    assert result.valid is False
    assert "Desfecho não informado." in result.errors


def test_negative_line():
    quote = MarketOutcome(
        market="goals",
        outcome="over",
        odd=2.00,
        line=-0.5,
    )

    result = validate_quote(quote)

    assert result.valid is False
    assert result.status == "BLOCKED"


def test_line_can_be_none():
    quote = MarketOutcome(
        market="result",
        outcome="home",
        odd=2.10,
        line=None,
    )

    result = validate_quote(quote)

    assert result.valid is True
