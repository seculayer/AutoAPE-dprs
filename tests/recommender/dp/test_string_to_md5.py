import pytest

from dprs.recommender.dp.StringToMD5 import StringToMD5


@pytest.fixture
def str2md5():
    return StringToMD5()


def test_string_to_md5_correct(str2md5):
    assert str2md5.apply("문자열") == ["80f8890171473def78045551c4eb2490"]
    assert str2md5.apply("Korea") == ["a8f809c99c4a996780c3046b9b594195"]


def test_string_to_md5_wrong_input(str2md5):
    assert str2md5.apply(0) == [""]
    assert str2md5.apply(()) == [""]
    assert str2md5.apply({}) == [""]
    assert str2md5.apply([]) == [""]
