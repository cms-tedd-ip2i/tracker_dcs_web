import pathlib
import pytest
from tracker_dcs_web.scripts.dummy_labview import parse_args, main
from tracker_dcs_web.utils.locate import abspath_data


@pytest.fixture
def mapping() -> pathlib.Path:
    mapping = abspath_data("labview/mapping.txt")
    assert mapping.exists() and mapping.is_file()
    return mapping.as_posix()


@pytest.fixture
def header() -> pathlib.Path:
    header = abspath_data("labview/header.txt")
    assert header.exists() and header.is_file()
    return header.as_posix()


@pytest.fixture
def data() -> pathlib.Path:
    data = abspath_data("labview/measure_lines_8.txt")
    assert data.exists() and data.is_file()
    return data.as_posix()


def test_parse_args(mapping, header, data):
    url = "http://localhost:8000"
    args = parse_args([url, mapping, header, data])
    assert args.mapping == mapping
    assert args.header == header
    assert args.data == data
    assert args.url == url


def test_parse_args_fail():
    with pytest.raises(SystemExit):
        parse_args([])

    with pytest.raises(SystemExit):
        parse_args(["http://foo.com", "foo.txt"])


def test_main(mapping, header, data):
    main(["http://localhost:8001", mapping, header, data, "-n 1"])
