import pytest
from tracker_dcs_web.web_server.data import Sensor


def test_sensor():
    with pytest.raises(ValueError):
        Sensor(data="foo\nbar")
    with pytest.raises(ValueError):
        Sensor(data="foobar")
