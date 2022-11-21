from abc import ABC, abstractmethod
import pathlib
import pickle
from typing import Dict, List
from tracker_dcs_web.utils.logger import logger
from tracker_dcs_web.utils.locate import abspath_root


class Metadata(ABC):
    def __init__(self, pck_name: str, save_file: pathlib.Path = None):
        if save_file is None:
            save_file = abspath_root() / pck_name
        self.save_file = save_file
        self._data = self.load()

    def __eq__(self, other):
        return self._data == other._data

    def __getitem__(self, item):
        try:
            return self._data[item]
        except KeyError as err:
            logger.warning(f"Key {err} cannot be found")
            raise

    def set(self, the_str: str):
        try:
            self._data = self.parse(the_str)
        except ValueError:
            raise
        if self._data:
            self.save()

    @staticmethod
    def skip(line):
        """Should the line be skipped?
        could improve this function to remove lines with blank characters,
        and commented lines. not a priority
        """
        if line == "":
            return True
        else:
            return False

    @abstractmethod
    def parse(self, the_str: str):
        ...

    def save(self):
        """Save mapping dictionary to pickle file"""
        logger.info(f"saving to {self.save_file.name}")
        with open(self.save_file, "wb") as ifile:
            pickle.dump(self._data, ifile)

    def load(self) -> [Dict, List, None]:
        """Load mapping dictionary from pickle file"""
        try:
            with open(self.save_file, "rb") as ifile:
                data = pickle.load(ifile)
        except FileNotFoundError:
            logger.info("cannot find save file")
            return None
        else:
            return data
