import pytest

from dprs.recommender.dp.DecodeBase64 import DecodeBase64


@pytest.fixture
def decoder():
    return DecodeBase64()


def test_decode_base64(decoder):
    assert decoder.apply("SGVsbG8gV29ybGQ=") == ["Hello World"]


def test_decode_base64_wrong_input(decoder):
    assert decoder.apply(0) == [""]
    assert decoder.apply([]) == [""]
    assert decoder.apply({}) == [""]
    assert decoder.apply(1.0) == [""]
    assert decoder.apply(1 + 1j) == [""]
