import pytest
from tracker_dcs_web.web_server.data.measurements import Measurements


@pytest.fixture()
def measurements():
    new = Measurements()
    return new


def test_bad_measurements_line(measurements):
    with pytest.raises(ValueError):
        measurements.set("foo\nbar")
    with pytest.raises(ValueError):
        measurements.set("foobar")


def test_measured_values(measurements):
    assert measurements.values is None
    measurements.set("1.\t2.\t3.")
    assert measurements.values == [1.0, 2.0, 3.0]
    assert measurements._data is None


def test_header(measurements):
    measurements.set("A\tB\tC")
    assert measurements._data == ["A", "B", "C"]
