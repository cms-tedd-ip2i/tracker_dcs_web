import pytest
from tracker_dcs_web.web_server.data import Mapping


def test_mapping_no_save():
    mapping = Mapping()
    assert mapping._data is None


@pytest.fixture()
def mapping():
    mapping = Mapping()
    mapping.set(
        """
15_10\t13_4\t42, 28
15_12\t13_5\t35,45

5_1\t9_4\t0
5_3\t1_2\t9
"""
    )
    mapping.save()
    yield mapping
    mapping.mapping_save_file.unlink()


def test_set_mapping(mapping):
    assert {42, 28, 35, 45, 0, 9} == set(mapping._data.keys())
    assert mapping[28].id == 28
    assert mapping[28].slot == "15_10"
    assert mapping[28].dummy_module == "13_4"
    assert mapping[42].id == 42
    assert mapping[42].slot == "15_10"
    assert mapping[42].dummy_module == "13_4"


def test_load_mapping(mapping):
    mapping2 = Mapping()
    assert mapping2 == mapping


def test_mapping_bad():
    # not enough lines
    mapping = Mapping()

    # not a 3-column tsv
    with pytest.raises(ValueError):
        mapping.set("foo\t\bar\t\baz\t\gee")
    with pytest.raises(ValueError):
        mapping.set("foo\n\bar")
