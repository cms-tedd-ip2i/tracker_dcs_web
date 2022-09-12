from dataclasses import dataclass
import pathlib
import re
from typing import Dict
from tracker_dcs_web.utils.logger import logger
from .metadata import Metadata


def skip(line):
    """Should the line be skipped?"""
    if line == "":
        return True
    else:
        return False


@dataclass
class Sensor:
    slot: str           # sensor slot (true module position)
    dummy_module: str   # heating device identifier
    id: int             # pt100 id


class Mapping(Metadata):
    """Mapping information

    It is saved to disk and loaded back automatically at startup
    """

    def __init__(self, save_file: pathlib.Path = None):
        super().__init__("mapping.pck", save_file)

    def to_dict(self) -> Dict[int, Sensor]:
        """Returns mapping as a dictionary"""
        return self._data

    @staticmethod
    def parse(mapping_str: str) -> Dict[int, Sensor]:
        lines = mapping_str.splitlines()
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
            slot, dummy_module, sensor_id = fields
            sensor_ids = re.split(r"\s*,\s*", sensor_id)
            for sensor_id in sensor_ids:
                sensor_id = int(sensor_id)
                mapping_dict[sensor_id] = Sensor(
                    id=sensor_id, slot=slot, dummy_module=dummy_module
                )
        return mapping_dict


mapping = Mapping()
