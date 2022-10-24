import json
import pytest
from tracker_dcs_web.utils.locate import abspath_data
from tracker_dcs_web.web_server.data.measurements import Measurements


@pytest.fixture()
def measurements():
    new = Measurements()
    yield new
    new.save_file.unlink(missing_ok=True)


def test_measurements_no_header(measurements):
    assert measurements._header is None


def test_measurements_set_header(measurements):
    # Date and H:M:S must be provided:
    with pytest.raises(ValueError):
        measurements.set("Date\tbar")
    with pytest.raises(ValueError):
        measurements.set("H:M:S\tbar")


@pytest.fixture
def mheader(measurements):
    with open(abspath_data("labview/header.txt")) as ifile:
        measurements.set(ifile.read())
    return measurements


@pytest.fixture
def dataline():
    with open(abspath_data("labview/measure_line.txt")) as ifile:
        return ifile.read()


def test_header_good(mheader):
    assert len(mheader._header.columns) == 69
    assert mheader.save_file.exists()
    assert mheader._data is None
    assert mheader.records() == {}


def test_header_reload(mheader):
    m2 = Measurements()
    assert len(m2._header.columns) == 69


def test_bad_data(mheader, dataline):
    dataline = "\t".join(dataline.split("\t")[1:])
    with pytest.raises(ValueError):
        mheader.set(dataline)


def test_good_data(mheader, dataline):
    mheader.set(dataline)
    assert mheader._data["Datetime_ns"][0] == 1652951162000000000
    assert "Date" not in mheader._data.columns
    assert "H:M:S" not in mheader._data.columns

    data = mheader.records()
    assert len(data) == 1
    data = data[0]
    assert len(data) == 67  # 69 - 3 (time - Data - H:M:S) + 1 (Datetime_ns)
    assert "0 (PS)" in data
    assert data["0 (PS)"] == 25.220262
