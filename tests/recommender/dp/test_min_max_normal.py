from dprs.recommender.dp.MinMaxNormal import MinMaxNormal


def test_minmax_8bit():
    minmax = MinMaxNormal(stat_dict={"min": 0, "max": 255})
    assert minmax.apply(255) == [1.0]
    assert minmax.apply(0) == [0.0]
    assert minmax.apply(128) == [(128 / 255)]
