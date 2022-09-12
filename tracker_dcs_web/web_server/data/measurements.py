import pathlib
import re
from typing import List
from tracker_dcs_web.utils.logger import logger
from .metadata import Metadata


class Measurements(Metadata):
    def __init__(self, save_file: pathlib.Path = None):
        super().__init__("header.pck", save_file)

    def to_list(self):
        return self._data

    @staticmethod
    def parse(the_str: str) -> List[float]:
        lines = the_str.splitlines()
        if len(lines) != 1:
            msg = "Must send exactly one line"
            logger.warning(msg)
            raise ValueError(msg)
        values = re.split(f"\s*\t\s*", the_str)
        if len(values) < 2:
            msg = "Must send tab-separated values"
            logger.warning(msg)
            raise ValueError(msg)
        return values


measurements = Measurements()
