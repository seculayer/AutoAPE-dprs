from dprs.recommender.dp.SignEncode import SignEncode


def test_sign_encode():
    sign = SignEncode()

    assert sign.apply("aht") is None
    assert sign.apply(0) == [-1]
    assert sign.apply(1) == [1]
    # assert sign.apply(123) == [1]
