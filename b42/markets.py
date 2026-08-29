from dataclasses import dataclass

from .integrity import check_market_integrity
from .model import fair_probability_from_odds
from .quotes import validate_quote
from .types import Market, MarketOutcome


@dataclass
class RankedOpportunity:
    market: str
    outcome: str
    line: float | None
    odd: float
    bookmaker: str | None
    implied_probability: float
    fair_market_probability: float
    rank_score: float = 0.0
    status: str = "VALID"


def validate_market(market: Market) -> None:
    if not market.name.strip():
        raise ValueError("Nome do mercado não pode estar vazio.")

    if not market.outcomes:
        raise ValueError(
            f"Mercado '{market.name}' não possui desfechos."
        )

    for outcome in market.outcomes:
        result = validate_quote(outcome)

        if not result.valid:
            raise ValueError(
                "; ".join(result.errors)
            )


def fair_market_probabilities(
    outcomes: list[MarketOutcome],
) -> dict[str, float]:
    if not outcomes:
        return {}

    valid_outcomes = []

    for outcome in outcomes:
        result = validate_quote(outcome)

        if result.valid:
            valid_outcomes.append(outcome)

    if not valid_outcomes:
        return {}

    probabilities = fair_probability_from_odds(
        [outcome.odd for outcome in valid_outcomes]
    )

    return {
        outcome.outcome: probability
        for outcome, probability in zip(
            valid_outcomes,
            probabilities,
        )
    }


def scan_market(
    market: Market,
    expected_outcomes: list[str] | None = None,
) -> list[RankedOpportunity]:
    integrity = check_market_integrity(
        market,
        expected_outcomes=expected_outcomes,
    )

    if integrity.status != "VALID":
        return []

    validate_market(market)

    fair_probs = fair_market_probabilities(
        market.outcomes
    )

    opportunities = []

    for outcome in market.outcomes:
        validation = validate_quote(outcome)

        if not validation.valid:
            continue

        implied = 1.0 / outcome.odd
        fair = fair_probs[outcome.outcome]

        opportunities.append(
            RankedOpportunity(
                market=market.name,
                outcome=outcome.outcome,
                line=outcome.line,
                odd=outcome.odd,
                bookmaker=outcome.bookmaker,
                implied_probability=implied,
                fair_market_probability=fair,
                status=validation.status,
            )
        )

    return opportunities


def scan_all_markets(
    markets: list[Market],
) -> list[RankedOpportunity]:
    opportunities = []

    for market in markets:
        opportunities.extend(
            scan_market(market)
        )

    opportunities.sort(
        key=lambda item: item.fair_market_probability,
        reverse=True,
    )

    for item in opportunities:
        item.rank_score = (
            item.fair_market_probability * 100.0
        )

    return opportunities
