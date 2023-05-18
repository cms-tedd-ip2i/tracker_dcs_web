import argparse
import itertools
import logging
import mimetypes
import os
import pathlib
import requests
import time
from typing import TextIO


logging.basicConfig(level=logging.INFO)


def send_data(data: str, url: str):
    logging.info("send data")
    response = requests.post(f"{url}/data", params={"measurements": data})
    response.raise_for_status()


def send_mapping(mapping: TextIO, url: str):
    mapping.seek(0)
    filename = "mapping.txt"
    response = requests.post(
        f"{url}/mapping",
        files={
            "upload_file": (
                filename,
                mapping,
                mimetypes.guess_type(filename)[0],
            )
        },
    )
    response.raise_for_status()


def good_file(file_path) -> pathlib.Path:
    """type for argparse (file that exists)"""
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"{file_path} does not exist or is not a file")
    return file_path


def parse_args(args: [str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send dummy labview data")
    parser.add_argument("url", type=str, help="web server url")
    parser.add_argument("mapping", type=good_file, help="mapping file")
    parser.add_argument("header", type=good_file, help="header file")
    parser.add_argument("data", type=good_file, help="data file")
    parser.add_argument("-t", type=int, help="time period", default=2)
    parser.add_argument("-n", type=int, help="number of messages", default=None)

    args = parser.parse_args(args)
    return args


def main(args=None):
    """Load items.

    > load_rei tests/data/SCHNEIDER_*.txt

    """
    import sys

    if not args:
        args = sys.argv[1:]
    args = parse_args(args)

    with open(args.mapping) as mapping_file:
        send_mapping(mapping_file, args.url)

    with open(args.header) as header_file:
        header = header_file.read()
    send_data(header, args.url)

    with open(args.data) as data_file:
        data = data_file.readlines()

    n_sent = 0
    for dataline in itertools.cycle(data):
        send_data(dataline, args.url)
        if args.n:
            n_sent += 1
            if n_sent >= args.n:
                break
            else:
                time.sleep(args.t)

    logging.info(f"sent {n_sent} data")


if __name__ == "__main__":
    main()
