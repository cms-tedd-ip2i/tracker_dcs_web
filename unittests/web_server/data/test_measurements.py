import pytest
from tracker_dcs_web.web_server.data import measurements


def test_bad_measurements_line():
    with pytest.raises(ValueError):
        measurements.set("foo\nbar")
    with pytest.raises(ValueError):
        measurements.set("foobar")


def test_measured_values():
    assert measurements.values is None
    measurements.set("1.\t2.\t3.")
    assert measurements.values == [1., 2., 3.]
    assert measurements._data is None


def test_header():
    measurements.set("A\tB\tC")
    assert measurements._data == ["A", "B", "C"]

