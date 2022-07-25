import pathlib
import tracker_dcs_web


def abspath_root():
    return pathlib.Path(tracker_dcs_web.__file__).parents[1]


def abspath_data(path):
    return abspath_root() / f"unittests/data/{path}"
