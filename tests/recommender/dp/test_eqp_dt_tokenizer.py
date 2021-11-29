import pytest

from dprs.recommender.dp.EqpDtTokenizer import EqpDtTokenizer


@pytest.fixture
def token():
    return EqpDtTokenizer()


def test_eqp_dt_tokenizer(token):
    assert token.apply("201812062106001") == [21, 6]


def test_eqp_dt_tokenizer_wrong_args(token):
    assert token.apply("2020") == [99.0, 99.0]
    assert token.apply([]) == [99.0, 99.0]
