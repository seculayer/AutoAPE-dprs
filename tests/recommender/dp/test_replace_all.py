from dprs.recommender.dp.ReplaceAll import ReplaceAll


def test_replace_regex():
    regex = ReplaceAll(arg_list=[r"[a-z]", ""])

    assert regex.apply("Korea") == ["K"]
    assert regex.apply("ATM") == ["ATM"]
    assert regex.apply(1) == [""]
    assert regex.apply("abc") == [""]
    assert regex.apply(1.0) == [""]
    assert regex.apply("") == [""]
