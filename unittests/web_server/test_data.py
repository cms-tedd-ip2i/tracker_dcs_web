import pytest

from pydantic import ValidationError

import tracker_dcs_web.web_server.data as data

user = "candan"
password = "cms"


def test_sensor_data():
    the_data = [27.0, 51, 18.1, 40.0]
    _ = data.Sensor(data=the_data)
    the_data = [27.0, 51, 18.1, 40.0, 33]
    with pytest.raises(ValidationError):
        _ = data.Sensor(data=the_data)
