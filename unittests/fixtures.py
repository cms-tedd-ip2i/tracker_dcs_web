import pytest


@pytest.fixture
def env(monkeypatch):
    variables = {
        "MQTT_HOST": "localhost",
        "MQTT_PORT": 1883,
        "APP_USER": "candan",
        "APP_PASSWORD": "cms",
    }
    for var_name, value in variables.items():
        monkeypatch.setenv(var_name, value)
