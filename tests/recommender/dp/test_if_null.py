from dprs.recommender.dp.IfNull import IfNull


def test_if_null():
    null = IfNull(arg_list=["A"])

    assert null.apply("") == ["A"]
    assert null.apply("str") == ["str"]
    assert null.apply(True) == ["A"]
    assert null.apply({}) == ["A"]
    assert null.apply([1]) == ["A"]
    assert null.apply(" \t") == ["A"]
