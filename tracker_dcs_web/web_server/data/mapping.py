from dataclasses import dataclass
import pathlib
import pickle
import re
from typing import Dict
from tracker_dcs_web.utils.logger import logger
from tracker_dcs_web.utils.locate import abspath_root


def skip(line):
    """Should the line be skipped?"""
    if line == "":
        return True
    else:
        return False


@dataclass
class Sensor:
    slot: str
    dummy_module: str
    id: int


class Mapping:
    def __init__(self, mapping_save_file: pathlib.Path = None):
        if mapping_save_file is None:
            mapping_save_file = abspath_root() / "mapping.pck"
        self.mapping_save_file = mapping_save_file
        self._data = self.load()

    def set(self, mapping_str: str):
        try:
            self._data = self.parse_mapping(mapping_str)
        except ValueError:
            raise

    def __getitem__(self, sensor_id):
        sensor = self._data.get(sensor_id)
        if sensor is None:
            msg = f"no such sensor: {sensor_id}"
            logger.warning(msg)
            raise KeyError(msg)
        return sensor

    def __eq__(self, other):
        return self._data == other._data

    @staticmethod
    def parse_mapping(mapping_str: str) -> Dict[int, Sensor]:
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

    def save(self):
        """Save mapping dictionary to pickle file"""
        with open(self.mapping_save_file, "wb") as ifile:
            pickle.dump(self._data, ifile)

    def load(self) -> [Dict, None]:
        """Load mapping dictionary from pickle file"""
        try:
            with open(self.mapping_save_file, "rb") as ifile:
                data = pickle.load(ifile)
        except FileNotFoundError:
            logger.warning("cannot find mapping save file, no mapping yet !")
            return None
        else:
            return data


mapping = Mapping()
