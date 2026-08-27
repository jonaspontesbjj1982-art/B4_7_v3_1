from dataclasses import dataclass

from .types import Market


@dataclass
class MarketIntegrity:
    valid: bool
    status: str
    expected_outcomes: int | None
    actual_outcomes: int
    missing_outcomes: list[str]
    duplicate_outcomes: list[str]
    errors: list[str]
    warnings: list[str]


def check_market_integrity(
    market: Market,
    expected_outcomes: list[str] | None = None,
) -> MarketIntegrity:
    errors: list[str] = []
    warnings: list[str] = []

    if not market.name.strip():
        errors.append("Nome do mercado não informado.")

    actual_names = [
        outcome.outcome.strip()
        for outcome in market.outcomes
        if outcome.outcome.strip()
    ]

    duplicates = sorted(
        {
            name
            for name in actual_names
            if actual_names.count(name) > 1
        }
    )

    if duplicates:
        errors.append(
            "Desfechos duplicados: "
            + ", ".join(duplicates)
        )

    missing: list[str] = []

    if expected_outcomes is not None:
        expected = [
            name.strip()
            for name in expected_outcomes
            if name.strip()
        ]

        actual_set = set(actual_names)

        missing = [
            name
            for name in expected
            if name not in actual_set
        ]

        if missing:
            warnings.append(
                "Desfechos esperados ausentes: "
                + ", ".join(missing)
            )

    if not market.outcomes:
        errors.append(
            f"Mercado '{market.name}' não possui desfechos."
        )

    if errors:
        status = "BLOCKED"
    elif missing:
        status = "REVIEW"
    else:
        status = "VALID"

    return MarketIntegrity(
        valid=len(errors) == 0 and not missing,
        status=status,
        expected_outcomes=(
            len(expected_outcomes)
            if expected_outcomes is not None
            else None
        ),
        actual_outcomes=len(actual_names),
        missing_outcomes=missing,
        duplicate_outcomes=duplicates,
        errors=errors,
        warnings=warnings,
    )
