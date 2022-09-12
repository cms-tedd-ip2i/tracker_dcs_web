import pytest
from tracker_dcs_web.web_server.data import measurements


def test_sensor():
    with pytest.raises(ValueError):
        measurements.set("foo\nbar")
    with pytest.raises(ValueError):
        measurements.set("foobar")
