import pytest

from dprs.recommender.dp.IPTransferDivide import IPTransferDivide


@pytest.fixture
def ip_divide():
    return IPTransferDivide()


def test_ip_transfer_divide(ip_divide):
    assert ip_divide.apply([]) == ["0", "0", "0", "0"]
    assert ip_divide.apply("10.10.10.10") == ["10", "10", "10", "10"]
    assert ip_divide.apply("192.168.0.1") == ["192", "168", "0", "1"]
    assert ip_divide.apply({}) == ["0", "0", "0", "0"]
    assert ip_divide.apply(1) == ["0", "0", "0", "0"]
