import pathlib
import re
from typing import List
from tracker_dcs_web.utils.logger import logger
from .metadata import Metadata


class Measurements(Metadata):
    """Measurements table, which includes the header and the measured values
    as a function of time.

    The header is saved to disk, and loaded back automatically at startup.
    The values are not saved
    """

    def __init__(self, save_file: pathlib.Path = None):
        super().__init__("header.pck", save_file)
        self.values = None

    def to_list(self) -> List:
        """Returns measurements as a list"""
        return self._data

    def parse_header(self, values: List[str]):
        return values

    def parse(self, the_str: str) -> [List, None]:
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
        float_values = []
        is_header = False
        for value in values:
            try:
                float_values.append(float(value))
            except ValueError:
                is_header = True
                break
        if is_header:
            return self.parse_header(values)
        else:
            self.values = float_values
            return None


measurements = Measurements()
