from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class MatchData:
    """
    Dados normalizados de uma partida.

    Os campos podem ser preenchidos pela API-Football
    ou manualmente durante os testes.
    """

    home_team: str
    away_team: str

    home_goals: int = 0
    away_goals: int = 0

    minute: int = 0
    status: str = "PRE"

    home_xg: Optional[float] = None
    away_xg: Optional[float] = None

    home_shots: int = 0
    away_shots: int = 0

    home_shots_on_target: int = 0
    away_shots_on_target: int = 0

    home_corners: int = 0
    away_corners: int = 0


@dataclass
class B47Result:
    """
    Resultado produzido pelo motor B4.7.
    """

    home_team: str
    away_team: str

    score_home: int
    score_away: int

    minute: int
    mode: str

    confidence: float
    signal: str

    details: dict


def validate_match(data: MatchData) -> None:
    """Valida os dados básicos da partida."""

    if not data.home_team.strip():
        raise ValueError("home_team não pode estar vazio.")

    if not data.away_team.strip():
        raise ValueError("away_team não pode estar vazio.")

    if data.home_goals < 0 or data.away_goals < 0:
        raise ValueError("Gols não podem ser negativos.")

    if data.minute < 0:
        raise ValueError("Minuto não pode ser negativo.")

    if data.minute > 130:
        raise ValueError("Minuto inválido.")

    numeric_fields = (
        "home_shots",
        "away_shots",
        "home_shots_on_target",
        "away_shots_on_target",
        "home_corners",
        "away_corners",
    )

    for field in numeric_fields:
        value = getattr(data, field)

        if value < 0:
            raise ValueError(f"{field} não pode ser negativo.")

    if data.home_xg is not None and data.home_xg < 0:
        raise ValueError("home_xg não pode ser negativo.")

    if data.away_xg is not None and data.away_xg < 0:
        raise ValueError("away_xg não pode ser negativo.")


def detect_mode(data: MatchData) -> str:
    """
    Determina se a análise é Pré ou Live.

    PRE  -> partida ainda não começou.
    LIVE -> partida em andamento.
    """

    status = data.status.upper().strip()

    if status in {"PRE", "NS", "NOT_STARTED"}:
        return "PRE"

    if status in {
        "LIVE",
        "1H",
        "2H",
        "HT",
        "ET",
        "P",
        "INT",
    }:
        return "LIVE"

    return "PRE" if data.minute == 0 else "LIVE"


def calculate_b47(data: MatchData) -> B47Result:
    """
    Ponto único de entrada do motor B4.7.

    A fórmula definitiva do B4.7 será conectada aqui.
    Esta versão NÃO inventa pesos ou sinais.
    """

    validate_match(data)

    mode = detect_mode(data)

    return B47Result(
        home_team=data.home_team,
        away_team=data.away_team,
        score_home=data.home_goals,
        score_away=data.away_goals,
        minute=data.minute,
        mode=mode,
        confidence=0.0,
        signal="PENDING",
        details={
            "engine": "B4.7",
            "version": "v3.1",
            "mode": mode,
            "formula": "pending",
        },
    )


def analyze_pre_match(
    home_team: str,
    away_team: str,
    **kwargs,
) -> B47Result:
    """Interface específica para análise Pré-jogo."""

    data = MatchData(
        home_team=home_team,
        away_team=away_team,
        status="PRE",
        **kwargs,
    )

    return calculate_b47(data)


def analyze_live(
    home_team: str,
    away_team: str,
    minute: int,
    home_goals: int = 0,
    away_goals: int = 0,
    **kwargs,
) -> B47Result:
    """Interface específica para análise Live."""

    data = MatchData(
        home_team=home_team,
        away_team=away_team,
        minute=minute,
        home_goals=home_goals,
        away_goals=away_goals,
        status="LIVE",
        **kwargs,
    )

    return calculate_b47(data)