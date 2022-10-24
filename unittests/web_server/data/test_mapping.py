import pytest
from tracker_dcs_web.web_server.data.mapping import Mapping


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
    yield mapping
    mapping.save_file.unlink()


def test_set_mapping(mapping):
    # all sensors found
    assert {42, 28, 35, 45, 0, 9} == set(mapping._data.keys())
    # sensors 42 and 28 have the same mapping
    assert mapping[28].id == 28
    assert mapping[28].slot == "15_10"
    assert mapping[28].dummy_module == "13_4"
    assert mapping[42].id == 42
    assert mapping[42].slot == "15_10"
    assert mapping[42].dummy_module == "13_4"
    # this sensor does not exist:
    with pytest.raises(KeyError):
        _ = mapping[7]


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
