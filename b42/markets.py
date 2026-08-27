from dataclasses import dataclass

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


def validate_market(market: Market) -> None:
    if not market.name.strip():
        raise ValueError("Nome do mercado não pode estar vazio.")

    if not market.outcomes:
        raise ValueError(
            f"Mercado '{market.name}' não possui desfechos."
        )

    for outcome in market.outcomes:
        if not outcome.outcome.strip():
            raise ValueError("Desfecho não pode estar vazio.")

        if outcome.odd <= 1.0:
            raise ValueError(
                f"Odd inválida: {outcome.odd}"
            )


def fair_market_probabilities(
    outcomes: list[MarketOutcome],
) -> dict[str, float]:
    if not outcomes:
        return {}

    inverse = {
        outcome.outcome: 1.0 / outcome.odd
        for outcome in outcomes
    }

    total = sum(inverse.values())

    if total <= 0:
        raise ValueError("Soma das probabilidades inválida.")

    return {
        name: value / total
        for name, value in inverse.items()
    }


def scan_market(
    market: Market,
) -> list[RankedOpportunity]:
    validate_market(market)

    fair_probs = fair_market_probabilities(
        market.outcomes
    )

    opportunities = []

    for outcome in market.outcomes:
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
