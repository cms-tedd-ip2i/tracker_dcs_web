import os

from tracker_dcs_web.utils.locate import abspath_root, abspath_data


def test_root():
    root = abspath_root()
    elements = os.listdir(root)
    assert {"tracker_dcs_web", "unittests"}.issubset(elements)


def test_data_path():
    dummy = abspath_data("dummy_files/test.txt")
    assert dummy.exists()
