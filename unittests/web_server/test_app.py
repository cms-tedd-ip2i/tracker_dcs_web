import pytest

from fastapi.testclient import TestClient
from fastapi import status
from unittests.fixtures import env

from tracker_dcs_web.web_server.data import mapping, measurements


@pytest.fixture
def app_client(env):
    from tracker_dcs_web.web_server.app import app

    client = TestClient(app)
    yield client
    mapping.save_file.unlink(missing_ok=True)
    measurements.save_file.unlink(missing_ok=True)


def test_root(app_client):
    """Test root endpoint"""
    response = app_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["message"].startswith("Tracker DCS")


def test_header_bad(app_client):

    # bad header
    the_data = "Date\tfoo"
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_header_good(app_client):
    # good header
    the_data = "Date\tH:M:S\tSensor"
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    cols = response.json()
    assert cols == ["Date", "H:M:S", "Sensor"]

    # change header
    the_data = "Date\tH:M:S\tSensor_1\tSensor_2"
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    cols = response.json()
    assert cols == ["Date", "H:M:S", "Sensor_1", "Sensor_2"]


def test_data(app_client):
    header = "Date\tH:M:S\tSensor"
    response = app_client.post("/data", params={"measurements": header})
    assert response.status_code == status.HTTP_201_CREATED

    # Bad date / time format
    the_data = "\t".join(["1", "2", "3"])
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Wrong number of values
    the_data = "\t".join(["1", "2"])
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Not a numeric
    the_data = "\t".join(["24/10/2022", "07:30:29", "foo"])
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # ok
    the_data = "\t".join(["24/10/2022", "07:30:29", "1."])
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    records = response.json()
    assert records == {"Sensor": 1.0, "Datetime_ns": 1666596629000000000}


def test_too_many_lines(app_client):
    # more than one line is not accepted
    the_data = "27.0\t51\t18.1\nfoo"
    response = app_client.post("/data", params={"measurements": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_mapping_bad(app_client):
    # not enough lines
    the_data = "foo"
    response = app_client.post("/mapping", params={"mapping": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # not a 3-column tsv
    the_data = "foo\nbar"
    response = app_client.post("/mapping", params={"mapping": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_mapping_ok(app_client):
    # 3-column tsv
    # on the first 2 lines, we have 2 pt100 on a dummy module
    the_data = """
15_10\t13_4\t42, 28
15_12\t13_5\t35,45

5_1\t9_4\t0
5_3\t1_2\t9
"""
    response = app_client.post("/mapping", params={"mapping": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    mapping = response.json()
    assert set(mapping.keys()) == {"42", "28", "35", "45", "0", "9"}
