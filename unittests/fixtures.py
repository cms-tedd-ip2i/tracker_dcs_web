import pytest


@pytest.fixture
def env(monkeypatch):
    variables = {"MQTT_HOST": "localhost", "APP_USER": "candan", "APP_PASSWORD": "cms"}
    for var_name, value in variables.items():
        monkeypatch.setenv(var_name, value)
