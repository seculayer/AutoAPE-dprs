import pytest

from dprs.recommender.dp.LongToIP import LongToIP


@pytest.fixture
def long2ip():
    return LongToIP()


def test_long_to_ip(long2ip):
    assert long2ip.apply(16909060) == ["1.2.3.4"]
    assert long2ip.apply(0x7F000001) == ["127.0.0.1"]
    assert long2ip.apply(0x0A0A0A00) == ["10.10.10.0"]
