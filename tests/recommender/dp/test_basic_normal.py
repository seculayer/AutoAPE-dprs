from dprs.recommender.dp.BasicNormal import BasicNormal


def test_basic_normal():
    basic = BasicNormal()
    assert basic.apply("abc") == [(3 / 32767)]
    assert basic.apply(None) == [0]
    assert basic.apply(32767) == [1]
    assert basic.apply("asht14234") == [""]
