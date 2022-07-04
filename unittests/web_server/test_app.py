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
    assert json["message"] == "Hello World"
    # assert json["user"] == os.environ["APP_USER"]
    assert json["user"] == "candan"
    assert json["password"] == "cms"


def test_data(app_client):
    the_data = [27.0, 51, 18.1, 40.0]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == the_data


def test_wrong_data(app_client):
    the_data = [27.0, 51, 18.1]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
