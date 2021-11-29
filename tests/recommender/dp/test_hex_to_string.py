import pytest

from dprs.recommender.dp.HexToString import HexToString


def test_hex_to_string_hello():
    hex2str = HexToString(arg_list=["utf-8"])

    assert hex2str.apply("68656c6c6f") == ["hello"]
