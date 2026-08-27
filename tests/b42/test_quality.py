import pytest

from b42.quality import (
    DEFAULT_TEMPORAL_WEIGHTS,
    TemporalWeights,
    assess_sample,
    validate_temporal_weights,
)


def test_sample_below_ten_is_insufficient():
    result = assess_sample(9)

    assert result.size == 9
    assert result.classification == "INSUFFICIENT"


def test_sample_between_ten_and_twenty_nine_is_limited():
    result = assess_sample(10)

    assert result.classification == "LIMITED"

    result = assess_sample(29)

    assert result.classification == "LIMITED"


def test_sample_of_thirty_or_more_is_adequate():
    result = assess_sample(30)

    assert result.classification == "ADEQUATE"




def test_qi_premium():
    from b42.quality import calculate_qi

    result = calculate_qi(90, 85, 90, 95)

    assert result.score == 90
    assert result.classification == "PREMIUM"


def test_qi_normal():
    from b42.quality import calculate_qi

    result = calculate_qi(75, 75, 70, 78)

    assert result.classification == "NORMAL"


def test_qi_borderline():
    from b42.quality import calculate_qi

    result = calculate_qi(65, 65, 65, 65)

    assert result.score == 65
    assert result.classification == "BORDERLINE"


def test_qi_skip():
    from b42.quality import calculate_qi

    result = calculate_qi(60, 60, 60, 60)

    assert result.score == 60
    assert result.classification == "SKIP"


def test_qi_rejects_invalid_component():
    import pytest
    from b42.quality import calculate_qi

    with pytest.raises(ValueError):
        calculate_qi(101, 80, 80, 80)


def test_qi_rejects_invalid_score():
    import pytest
    from b42.quality import classify_qi

    with pytest.raises(ValueError):
        classify_qi(-1)

    with pytest.raises(ValueError):
        classify_qi(101)


def test_negative_sample_is_rejected():
    with pytest.raises(ValueError):
        assess_sample(-1)


def test_default_temporal_weights():
    weights = DEFAULT_TEMPORAL_WEIGHTS

    assert weights.long_term == 0.50
    assert weights.medium_term == 0.30
    assert weights.short_term == 0.20

    validate_temporal_weights(weights)


def test_invalid_temporal_weights_are_rejected():
    weights = TemporalWeights(
        long_term=0.50,
        medium_term=0.30,
        short_term=0.30,
    )

    with pytest.raises(ValueError):
        validate_temporal_weights(weights)


def test_temporal_score_uses_default_weights():
    from b42.quality import calculate_temporal_score

    result = calculate_temporal_score(
        long_term=100,
        medium_term=50,
        short_term=0,
    )

    assert result.score == 65


def test_temporal_score_with_custom_weights():
    from b42.quality import calculate_temporal_score

    weights = TemporalWeights(
        long_term=0.20,
        medium_term=0.30,
        short_term=0.50,
    )

    result = calculate_temporal_score(
        long_term=100,
        medium_term=50,
        short_term=0,
        weights=weights,
    )

    assert result.score == 35


def test_temporal_score_rejects_invalid_component():
    from b42.quality import calculate_temporal_score

    with pytest.raises(ValueError):
        calculate_temporal_score(
            long_term=101,
            medium_term=50,
            short_term=50,
        )


def test_temporal_score_rejects_negative_component():
    from b42.quality import calculate_temporal_score

    with pytest.raises(ValueError):
        calculate_temporal_score(
            long_term=50,
            medium_term=-1,
            short_term=50,
        )


def test_temporal_score_preserves_components():
    from b42.quality import calculate_temporal_score

    result = calculate_temporal_score(
        long_term=80,
        medium_term=70,
        short_term=60,
    )

    assert result.long_term == 80
    assert result.medium_term == 70
    assert result.short_term == 60


def test_temporal_score_all_maximum_is_100():
    from b42.quality import calculate_temporal_score

    result = calculate_temporal_score(100, 100, 100)

    assert result.score == 100
