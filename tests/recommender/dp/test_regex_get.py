from dprs.recommender.dp.RegexGet import RegexGet


def test_regex_get():
    regex = RegexGet(arg_list=[r"[a-z]+_(\d+)_[a-z]+"])

    assert regex.apply("prefix_123_suffix") == ["123"]


def test_regex_get_two_group():
    regex = RegexGet(arg_list=[r"[a-z]+_(\d+)_[a-z]+_(\d+)"])

    assert regex.apply("prefix_123_suffix_213") == ["123"]
