from dprs.recommender.dp.SpecialCharExtract import SpecialCharExtract


def test_special_char_extract_simple():
    max_len = 4
    special_char = SpecialCharExtract(stat_dict=None, arg_list=[max_len])

    assert special_char.apply("example.com?param=1") == [46, 63, 61, 255.0]


def test_special_char_extract_long():
    max_len = 1000
    special_char = SpecialCharExtract(stat_dict=None, arg_list=[max_len])

    expected = [58, 47, 47, 46, 47, 47, 47, 45, 45, 45, 45, 45]
    expected.extend([255.0] * (max_len - len(expected)))
    assert (
        special_char.apply(
            "https://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python白萬基"
        )
        == expected
    )
