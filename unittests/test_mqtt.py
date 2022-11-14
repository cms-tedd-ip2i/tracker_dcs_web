import json
import pytest

from .fixtures import env


@pytest.fixture
def mqtt(env):
    import tracker_dcs_web.mqtt as mqtt_mod

    return mqtt_mod


def test_connect(mqtt):
    mqtt.client.publish("/test", json.dumps({"a": 1}))
    assert True
