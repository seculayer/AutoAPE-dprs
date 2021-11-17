from dprs.recommender.dp.ZScoreNormal import ZScoreNormal


def test_zscore_normal():
    zscore = ZScoreNormal(stat_dict={"avg": 1, "stddev": 0.1})

    assert zscore.apply(2) == [10]
    assert zscore.apply(-1) == [-20]


def test_zscore_stddev_0():
    zscore = ZScoreNormal(stat_dict={"avg": 1, "stddev": 0})

    assert zscore.apply(-1) == [-2]
    assert zscore.apply(2) == [1]


def test_zscore_str():
    zscore = ZScoreNormal(stat_dict={"avg": 1, "stddev": 0.1})

    assert zscore.apply("str") == [0]
