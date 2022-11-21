import pandas as pd
import pathlib
from tracker_dcs_web.utils.locate import abspath_root
from tracker_dcs_web.utils.logger import logger
from typing import Dict, List


class Measurements:
    def __init__(self):
        self.save_file = abspath_root() / "header.csv"
        self._header = self.load()
        self._data = None

    def load(self) -> [pd.DataFrame, None]:
        """Load header dataframe from save file if it exists"""
        if not self.save_file.exists():
            logger.info("cannot find measurements header save file")
            return None
        df = pd.read_csv(self.save_file)
        return df

    def save(self):
        """Save header dataframe to save file"""
        logger.info(f"saving measurements header to {self.save_file.name}")
        self._header.to_csv(self.save_file, index=False)

    def set(self, the_str: str):
        """Set header or data line

        :param the_str: tab separated values.
        """
        the_str = the_str.strip()
        n_lines = len(the_str.split("\n"))
        if n_lines > 1:
            raise ValueError("Send only one line")
        values = the_str.strip().split("\t")
        if self._header is None or "Date" in values:
            header = pd.DataFrame(columns=values)
            if not header.empty:
                raise ValueError("header not empty!")
            if not {"Date", "H:M:S"}.issubset(set(header.columns)):
                raise ValueError("Columns Date and H:M:S must be provided")
            self._header = header
            self.save()
        else:
            try:
                self._data = pd.DataFrame(data=[values], columns=self._header.columns)
            except ValueError:
                logger.error("data does not match header:")
                logger.error(
                    f"columns: {len(self._header.columns)} {list(self._header.columns)}"
                )
                logger.error(f"values : {len(values)} {values}")
                raise

            # parse time

            pdf = self._data
            try:
                pdf["Datetime_ns"] = pd.to_datetime(
                    pdf["Date"] + " " + pdf["H:M:S"], format="%d/%m/%Y %H:%M:%S"
                )
            except KeyError:
                logger.error("Columns Date and H:M:S must be provided")
                raise
            else:
                pdf.drop(
                    columns=["Times[s]", "Date", "H:M:S"], inplace=True, errors="ignore"
                )

            # convert to numeric
            for col in pdf.columns:
                pdf[col] = pd.to_numeric(pdf[col])

    def columns(self) -> List:
        """Return list of columns"""
        return self._header.columns.to_list()

    def records(self) -> [Dict, None]:
        """Return json representation of the current data"""
        if self._data is not None:
            return self._data.to_dict(orient="records")[0]
        else:
            return {}


measurements = Measurements()
