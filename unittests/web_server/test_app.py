import mimetypes
import pprint

import pytest

from fastapi.testclient import TestClient
from fastapi import status
from unittests.fixtures import env

from tracker_dcs_web.web_server.data import mapping, measurements
from tracker_dcs_web.utils.locate import abspath_data


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
    def post(data):
        response = app_client.post(
            "/mapping",
            files={"upload_file": ("foo.txt", data.encode("utf8"), ".txt")},
        )
        return response.status_code

    data = """
11_4\t15_7\t53
15_4\t11_5\t41
"""

    assert post(data) == status.HTTP_201_CREATED

    # missing a column
    data = """
11_4\t15_7
"""
    assert post(data) == status.HTTP_422_UNPROCESSABLE_ENTITY

    # last column is an integer
    data = """
11_4\t15_7\tfoo
"""
    assert post(data) == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_mapping_ok(app_client):
    # 3-column tsv
    # on the first 2 lines, we have 2 pt100 on a dummy module
    test_mapping = abspath_data("labview/mapping.txt")
    assert test_mapping.exists()

    with open(test_mapping) as file:
        response = app_client.post(
            "/mapping",
            files={
                "upload_file": (
                    test_mapping.name,
                    file,
                    mimetypes.guess_type(test_mapping)[0],
                )
            },
        )
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    channel = result.get("1")
    assert channel["dummy_module"] == "15_25"
    assert channel["slot"] == "11_3"
