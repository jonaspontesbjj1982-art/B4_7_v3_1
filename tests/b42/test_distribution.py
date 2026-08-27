from b42.distribution import percentile, summarize_distribution


def test_empty_distribution():
    result = summarize_distribution([])

    assert result.sample_size == 0
    assert result.mean is None
    assert result.median is None
    assert result.p25 is None
    assert result.p75 is None


def test_basic_distribution():
    result = summarize_distribution([1, 2, 3, 4, 5])

    assert result.sample_size == 5
    assert result.mean == 3
    assert result.median == 3
    assert result.p25 == 2
    assert result.p75 == 4
    assert result.minimum == 1
    assert result.maximum == 5


def test_frequencies():
    result = summarize_distribution([1, 1, 2, 3, 3, 3])

    assert result.frequencies == {
        1: 2,
        2: 1,
        3: 3,
    }


def test_percentile_interpolation():
    assert percentile([1, 2, 3, 4], 0.25) == 1.75
    assert percentile([1, 2, 3, 4], 0.75) == 3.25


def test_single_value():
    result = summarize_distribution([7])

    assert result.sample_size == 1
    assert result.mean == 7
    assert result.median == 7
    assert result.p25 == 7
    assert result.p75 == 7
    assert result.minimum == 7
    assert result.maximum == 7


def test_distribution_does_not_modify_input():
    values = [5, 1, 3]

    summarize_distribution(values)

    assert values == [5, 1, 3]
