import enum
import os

from met_src.input import json, csv


FORMATTERS = {
    "csv": csv.read,
    "json": json.read,
}


def read(input_path: str, target_sample: str = None):
    _, input_ext = os.path.splitext(input_path)
    input_format = input_ext[1:].lower()
    if input_format not in FORMATTERS:
        raise ValueError(f"Cannot read from unknown file format '{input_format}'")
    reader = FORMATTERS[input_format]
    return reader(input_path, target_sample)
