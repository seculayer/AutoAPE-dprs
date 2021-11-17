from dprs.recommender.dp.String2ASCII import String2ASCII


def test_string_to_ascii():
    str2ascii = String2ASCII(arg_list=[5, 3])

    assert str2ascii.apply(["0", "53018000", "20140523173202"]) == [
        [48, 0, 0, 0, 0],
        [53, 51, 48, 49, 56],
        [50, 48, 49, 52, 48],
    ]
    assert str2ascii.apply(["hjg yjhg 6ug679t g6guy g321%!#% $^$Fgsdfha"]) == [
        [104, 106, 103, 32, 121],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
