from pydantic import BaseModel, validator
import re

from tracker_dcs_web.utils.logger import logger


class Sensor(BaseModel):
    data: str

    @validator("data")
    def ext(cls, v):
        lines = v.splitlines()
        if len(lines) != 1:
            msg = f"Send exactly one line of values"
            logger.error(msg)
            raise ValueError(msg)
        fields = re.split("\t", lines[0])
        if len(fields) < 2:
            msg = f"send a tab-separated line"
            logger.error(msg)
            raise ValueError(msg)
        return v
