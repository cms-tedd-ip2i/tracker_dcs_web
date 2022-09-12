import pytest

from fastapi.testclient import TestClient
from fastapi import status
from unittests.fixtures import env


@pytest.fixture
def app_client(env):
    from tracker_dcs_web.web_server.app import app

    client = TestClient(app)
    yield client


def test_root(app_client):
    """Test root endpoint"""
    response = app_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["message"].startswith("Tracker DCS")


def test_data(app_client):
    the_data = "27.0\t51\t18.1"
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == the_data


def test_wrong_data(app_client):
    # more than one line is not accepted
    the_data = "27.0\t51\t18.1\nfoo"
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_mapping_bad(app_client):
    # not enough lines
    the_data = "foo"
    response = app_client.post("/mapping", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # not a 3-column tsv
    the_data = "foo\nbar"
    response = app_client.post("/mapping", json={"data": the_data})
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
