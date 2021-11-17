from dprs.recommender.dp.Substr import Substr


def test_substr():
    sub = Substr(arg_list=[0, 1])

    assert sub.apply("Korea") == ["K"]
    assert sub.apply(123) == [""]
