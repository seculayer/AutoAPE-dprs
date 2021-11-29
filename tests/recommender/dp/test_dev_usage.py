import pytest
from pytest import approx

from dprs.recommender.dp.DevUsage import DevUsage


@pytest.fixture
def usage():
    return DevUsage()


def test_dev_usage(usage):
    assert usage.apply("85.4542") == [approx(0.709084)]
    assert usage.apply("") == [approx(0)]
    assert usage.apply("40") == [approx(-0.2)]
    assert usage.apply(0) == [approx(-1.0)]
