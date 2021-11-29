import pytest

from dprs.recommender.dp.ToUpperCase import ToUpperCase


@pytest.fixture
def upper():
    return ToUpperCase()


def test_to_lower_case_correct(upper):
    assert upper.apply("lowercase") == ["LOWERCASE"]
    assert upper.apply("UPPERCASE") == ["UPPERCASE"]
    assert upper.apply("♞") == ["♞"]
    assert upper.apply("😀") == ["😀"]


def test_to_lower_case_wrong_arg(upper):
    assert upper.apply(0) == [""]
    assert upper.apply(()) == [""]
    assert upper.apply({}) == [""]
    assert upper.apply([]) == [""]
    assert upper.apply(True) == [""]
    assert upper.apply(False) == [""]
    assert upper.apply(None) == [""]
