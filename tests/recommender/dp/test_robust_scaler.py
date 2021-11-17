from dprs.recommender.dp.RobustScaler import RobustScaler


def test_robust_scaler():
    rs = RobustScaler(stat_dict={"median": 128, "quantile_1": 64, "quantile_3": 192})

    assert rs.apply(192) == [0.5]
    assert rs.apply(168) == [0.3125]
    assert rs.apply(0) == [-1]
    assert rs.apply(256) == [1]
    assert rs.apply(-128) == [-2]
