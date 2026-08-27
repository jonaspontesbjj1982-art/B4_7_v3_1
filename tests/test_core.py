from b47.core import (
    MatchData,
    analyze_live,
    analyze_pre_match,
    calculate_b47,
    detect_mode,
    validate_match,
)


def test_match_data():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
    )

    assert data.home_team == "Flamengo"
    assert data.away_team == "Palmeiras"
    assert data.home_goals == 0
    assert data.away_goals == 0


def test_validate_match():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
    )

    validate_match(data)


def test_invalid_goals():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
        home_goals=-1,
    )

    try:
        validate_match(data)
        assert False
    except ValueError:
        assert True


def test_detect_pre_mode():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
        status="PRE",
    )

    assert detect_mode(data) == "PRE"


def test_detect_live_mode():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
        minute=35,
        status="LIVE",
    )

    assert detect_mode(data) == "LIVE"


def test_calculate_b47():
    data = MatchData(
        home_team="Flamengo",
        away_team="Palmeiras",
    )

    result = calculate_b47(data)

    assert result.home_team == "Flamengo"
    assert result.away_team == "Palmeiras"
    assert result.mode == "PRE"
    assert result.signal == "PENDING"


def test_analyze_pre_match():
    result = analyze_pre_match(
        "Flamengo",
        "Palmeiras",
    )

    assert result.mode == "PRE"


def test_analyze_live():
    result = analyze_live(
        "Flamengo",
        "Palmeiras",
        minute=60,
        home_goals=1,
        away_goals=0,
    )

    assert result.mode == "LIVE"
    assert result.minute == 60
    assert result.score_home == 1
    assert result.score_away == 0