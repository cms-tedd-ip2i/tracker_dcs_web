import pytest
from tracker_dcs_web.web_server.data import Mapping, MappingHelper


def test_mapping_bad():
    # not enough lines
    with pytest.raises(ValueError):
        Mapping(data="foo")

    # not a 3-column tsv
    with pytest.raises(ValueError):
        Mapping(data="foo\t\bar\t\baz\t\gee")
    with pytest.raises(ValueError):
        Mapping(data="foo\n\bar")


def test_mapping_ok():
    mapping = Mapping(
        data="""
15_10\t13_4\t42, 28
15_12\t13_5\t35,45

5_1\t9_4\t0
5_3\t1_2\t9
"""
    )
    assert mapping.data
    mapping = MappingHelper.parse_mapping(mapping)
    assert {42, 28, 35, 45, 0, 9} == set(mapping.data.keys())
    assert mapping.data[28].slot == "15_10"
    assert mapping.data[28].dummy_module == "13_4"
    assert mapping.data[42].slot == "15_10"
    assert mapping.data[42].dummy_module == "13_4"

    # test save
    save = MappingHelper.save_mapping(mapping)
    assert save.exists()

    # test load
    mapping2 = MappingHelper.load_mapping()
    assert mapping2 == mapping
