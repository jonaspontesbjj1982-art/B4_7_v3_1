from dataclasses import dataclass

from .types import MarketOutcome


@dataclass
class QuoteValidation:
    valid: bool
    status: str
    errors: list[str]


def validate_quote(quote: MarketOutcome) -> QuoteValidation:
    errors: list[str] = []

    if not quote.market.strip():
        errors.append("Mercado não informado.")

    if not quote.outcome.strip():
        errors.append("Desfecho não informado.")

    if quote.odd <= 1.0:
        errors.append(f"Odd inválida: {quote.odd}.")

    if quote.line is not None and quote.line < 0:
        errors.append(f"Linha inválida: {quote.line}.")

    if errors:
        return QuoteValidation(
            valid=False,
            status="BLOCKED",
            errors=errors,
        )

    return QuoteValidation(
        valid=True,
        status="VALID",
        errors=[],
    )
