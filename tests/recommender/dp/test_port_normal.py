from dprs.recommender.dp.PortNormal import PortNormal


def test_port_normal():
    port = PortNormal()

    assert port.apply("ashtr") == [0]
    assert port.apply("8080") == [8080 / 65535]
    assert port.apply(0) == [0]
