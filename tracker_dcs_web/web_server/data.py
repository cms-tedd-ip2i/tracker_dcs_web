from pydantic import BaseModel, validator
from typing import List
import re
from tracker_dcs_web.utils.logger import logger


class Sensor(BaseModel):
    data: List[float]

    @validator("data")
    def ext(cls, v):
        data_len = 4
        if not len(v) == data_len:
            msg = f"Send exactly {data_len} values"
            logger.error(msg)
            raise ValueError(msg)
        return v


class Mapping(BaseModel):
    data: str

    @validator("data")
    def validate_data(cls, v: str):
        lines = v.splitlines()
        n_lines_min = 2
        if len(lines) < n_lines_min:
            msg = f"Mapping must have at least {n_lines_min} lines"
            logger.error(msg)
            raise ValueError(f"Mapping must have at least {n_lines_min} lines")
        for line in lines:
            print(line)
            if line == "":
                continue
            fields = re.split("\t", line)
            if len(fields) != 3:
                msg = f"Mapping file must be a tab separated file with 3 columns"
                logger.error(msg)
                raise ValueError(msg)
        return v
