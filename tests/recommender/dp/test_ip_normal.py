from dprs.recommender.dp.IPNormal import IPNormal


def test_ipnormal():
    ip = IPNormal()

    default = [0, 0, 0, 0]

    assert ip.apply("127.0.0.1") == [(127 / 255), 0, 0, (1 / 255)]
    assert ip.apply("::1") == default
    assert ip.apply(1123094) == default
    assert ip.apply(123.0) == default
    assert ip.apply("10.0.0.1") == [(10 / 255), 0, 0, (1 / 255)]
