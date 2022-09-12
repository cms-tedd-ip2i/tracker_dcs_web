from abc import ABC, abstractmethod
import pathlib
import pickle
import re
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
            logger.warning(err)
            raise

    def set(self, the_str: str):
        try:
            self._data = self.parse(the_str)
        except ValueError:
            raise

    @staticmethod
    @abstractmethod
    def parse(the_str: str):
        ...

    def save(self):
        """Save mapping dictionary to pickle file"""
        with open(self.save_file, "wb") as ifile:
            pickle.dump(self._data, ifile)

    def load(self) -> [Dict, List, None]:
        """Load mapping dictionary from pickle file"""
        try:
            with open(self.save_file, "rb") as ifile:
                data = pickle.load(ifile)
        except FileNotFoundError:
            logger.warning("cannot find mapping save file, no mapping yet !")
            return None
        else:
            return data
