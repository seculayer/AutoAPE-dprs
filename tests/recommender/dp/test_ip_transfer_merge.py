import pytest

from dprs.recommender.dp.IPTransferMerge import IPTransferMerge


@pytest.fixture
def ip_merge():
    return IPTransferMerge()


def test_ip_transfer_merge(ip_merge):
    assert (
        ip_merge.apply(["192.168.1.110", "192.168.1.111"])
        == ["192.168.1.110.192.168.1.111"] * 6
    )
    assert ip_merge.apply([]) == ["0", "0", "0", "0", "0", "0"]
