from dataclasses import dataclass

from .types import MatchContext


VALID_STATUSES = {"PRE", "LIVE", "FT", "POSTPONED", "CANCELLED"}


@dataclass
class ValidationResult:
    valid: bool
    status: str
    errors: list[str]
    warnings: list[str]


def validate_event(event: MatchContext) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not event.home_team.strip():
        errors.append("Mandante não informado.")

    if not event.away_team.strip():
        errors.append("Visitante não informado.")

    if event.home_team.strip().lower() == event.away_team.strip().lower():
        errors.append("Mandante e visitante não podem ser iguais.")

    if event.status not in VALID_STATUSES:
        errors.append(
            f"Status inválido: {event.status}. "
            f"Permitidos: {', '.join(sorted(VALID_STATUSES))}."
        )

    if not event.competition or not event.competition.strip():
        warnings.append("Competição não informada.")

    if not event.fixture_id:
        warnings.append("ID do evento não informado.")

    if not event.start_time:
        warnings.append("Horário de início não informado.")

    if event.status == "LIVE":
        if event.minute < 0:
            errors.append("Minuto da partida não pode ser negativo.")

        if event.home_goals < 0 or event.away_goals < 0:
            errors.append("Placar não pode ser negativo.")

    valid = len(errors) == 0

    if not valid:
        result_status = "BLOCKED"
    elif warnings:
        result_status = "REVIEW"
    else:
        result_status = "VALIDATED"

    return ValidationResult(
        valid=valid,
        status=result_status,
        errors=errors,
        warnings=warnings,
    )
