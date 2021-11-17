import pytest

from dprs.recommender.dp.ToLowerCase import ToLowerCase


@pytest.fixture
def lower():
    return ToLowerCase()


def test_to_lower_case_correct(lower):
    assert lower.apply("lower") == ["lower"]
    assert lower.apply("UPPERCASE") == ["uppercase"]
    assert lower.apply("♞") == ["♞"]
    assert lower.apply("😀") == ["😀"]


def test_to_lower_case_wrong_arg(lower):
    assert lower.apply(0) == [""]
    assert lower.apply(()) == [""]
    assert lower.apply({}) == [""]
    assert lower.apply([]) == [""]
    assert lower.apply(True) == [""]
    assert lower.apply(False) == [""]
    assert lower.apply(None) == [""]
