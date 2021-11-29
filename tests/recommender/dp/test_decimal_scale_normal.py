import pytest

from dprs.recommender.dp.DecimalScaleNormal import DecimalScaleNormal


def test_decimal_scale():
    decimal_scale = DecimalScaleNormal()

    assert decimal_scale.apply(0) == [0]
    assert decimal_scale.apply(192) == [0.00192]
    assert decimal_scale.apply(-1) == [-1e-5]
    assert decimal_scale.apply("str") == [0]
