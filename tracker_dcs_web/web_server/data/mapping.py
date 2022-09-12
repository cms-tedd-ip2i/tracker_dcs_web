import pathlib

from pydantic import BaseModel, validator
import pickle
import re
from typing import Dict

from tracker_dcs_web.utils.locate import abspath_root
from tracker_dcs_web.utils.logger import logger


def skip(line):
    """Should the line be skipped?"""
    if line == "":
        return True
    else:
        return False


class Mapping(BaseModel):
    """Mapping input"""

    data: str

    @validator("data")
    def validate_data(cls, v: str):
        lines = v.splitlines()
        n_lines_min = 2
        mapping_dict = {}
        if len(lines) < n_lines_min:
            msg = f"Mapping must have at least {n_lines_min} lines"
            logger.error(msg)
            raise ValueError(f"Mapping must have at least {n_lines_min} lines")
        for line in lines:
            if skip(line):
                continue
            fields = re.split("\t", line)
            if len(fields) != 3:
                msg = f"Mapping file must be a tab separated file with 3 columns"
                logger.error(msg)
                raise ValueError(msg)
        return v


class SensorMapping(BaseModel):
    slot: str
    dummy_module: str


class MappingDict(BaseModel):
    data: Dict[int, SensorMapping]


class MappingHelper:

    mapping_save_file = abspath_root() / "mapping.pck"

    @staticmethod
    def parse_mapping(mapping: Mapping) -> MappingDict:
        """Turn the original mapping string into a dictionary data structure"""
        lines = mapping.data.splitlines()
        mapping_dict = {}
        for line in lines:
            if skip(line):
                continue
            fields = re.split("\t", line)
            assert len(fields) == 3
            slot, dummy_module, sensor_id = fields
            # several sensors can be attached to the same dummy module,
            # in which case they are specified as a comma separated list
            sensor_ids = re.split("\s*,\s*", sensor_id)
            for sensor_id in sensor_ids:
                sensor_id = int(sensor_id)
                mapping_dict[sensor_id] = SensorMapping(
                    slot=slot, dummy_module=dummy_module
                )
        return MappingDict(data=mapping_dict)

    @classmethod
    def save_mapping(cls, mapping: MappingDict) -> pathlib.Path:
        with open(cls.mapping_save_file, "wb") as ifile:
            pickle.dump(mapping, ifile)
        return cls.mapping_save_file

    @classmethod
    def load_mapping(cls) -> MappingDict:
        with open(cls.mapping_save_file, "rb") as ifile:
            mapping = pickle.load(ifile)
        return mapping
