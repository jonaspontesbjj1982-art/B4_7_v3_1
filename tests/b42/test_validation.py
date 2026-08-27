from b42.types import MatchContext
from b42.validation import validate_event


def test_valid_pre_event():
    event = MatchContext(
        home_team="Time A",
        away_team="Time B",
        competition="Competição",
        fixture_id="123",
        start_time="2026-08-27T20:00:00",
        status="PRE",
    )

    result = validate_event(event)

    assert result.valid is True
    assert result.status == "VALIDATED"
    assert result.errors == []
    assert result.warnings == []


def test_missing_teams_blocks_event():
    event = MatchContext(
        home_team="",
        away_team="Time B",
        status="PRE",
    )

    result = validate_event(event)

    assert result.valid is False
    assert result.status == "BLOCKED"
    assert "Mandante não informado." in result.errors


def test_same_teams_blocks_event():
    event = MatchContext(
        home_team="Time A",
        away_team="Time A",
        status="PRE",
    )

    result = validate_event(event)

    assert result.valid is False
    assert result.status == "BLOCKED"


def test_missing_optional_information_requires_review():
    event = MatchContext(
        home_team="Time A",
        away_team="Time B",
        status="PRE",
    )

    result = validate_event(event)

    assert result.valid is True
    assert result.status == "REVIEW"
    assert len(result.warnings) == 3


def test_live_event_accepts_score_and_minute():
    event = MatchContext(
        home_team="Time A",
        away_team="Time B",
        status="LIVE",
        minute=63,
        home_goals=1,
        away_goals=0,
    )

    result = validate_event(event)

    assert result.valid is True
    assert result.status == "REVIEW"


def test_invalid_live_minute_blocks_event():
    event = MatchContext(
        home_team="Time A",
        away_team="Time B",
        status="LIVE",
        minute=-1,
    )

    result = validate_event(event)

    assert result.valid is False
    assert result.status == "BLOCKED"
