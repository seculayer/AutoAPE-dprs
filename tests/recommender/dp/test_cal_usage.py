import pytest

from dprs.recommender.dp.CalUsage import CalUsage


@pytest.fixture
def usage():
    return CalUsage()


def test_cal_dev_usage(usage):
    assert usage.apply("24.5753") == [0.245753]
    assert usage.apply("") == [0]
    assert usage.apply("0") == [0]
    assert usage.apply(10) == [0.1]
    assert usage.apply(100.0) == [1]
