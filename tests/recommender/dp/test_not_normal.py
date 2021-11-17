import pytest

from dprs.recommender.dp.NotNormal import NotNormal


@pytest.fixture
def not_normal():
    return NotNormal()


def test_not_normal_int(not_normal):
    assert not_normal.apply(1) == [1.0]


def test_not_normal_float(not_normal):
    assert not_normal.apply(0.1) == [0.1]
    assert not_normal.apply(1e-10) == [1e-10]


def test_not_normal_str(not_normal):
    assert not_normal.apply("string") == ["string"]
    assert not_normal.apply("[\r\n]+") == ["#CRLF#"]
    assert not_normal.apply("\\,") == ["#COMMA#"]
    assert not_normal.apply("\r") != ["#CRLF#"]
