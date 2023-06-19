import csv
import math
import os
from dataclasses import dataclass

import met_src
from met_src.mineral import Mineral
from met_src.normal_distribution import NormalDistribution

DEFAULT_PATH = os.path.join(
    met_src.__path__[0], "data", "lpgrs", "lpgrs_high1_elem_abundance_2deg.tab"
)

_CACHE = None


@dataclass
class LpgrsCell:
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float
    composition: dict[Mineral, NormalDistribution]


def get_lpgrs_data(filepath=DEFAULT_PATH):
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    position_columns = {
        "min_lat": 1,
        "max_lat": 2,
        "min_lon": 3,
        "max_lon": 4,
    }

    composition_columns = {
        Mineral.MgO: 7,
        Mineral.Al2O3: 8,
        Mineral.SiO2: 9,
        Mineral.CaO: 10,
        Mineral.TiO2: 11,
        Mineral.FeO: 12,
        Mineral.K: 13,
        Mineral.Th: 14,
        Mineral.U: 15,
    }

    error_columns = {
        Mineral.MgO: 16,
        Mineral.Al2O3: 25,
        Mineral.SiO2: 33,
        Mineral.CaO: 40,
        Mineral.TiO2: 46,
        Mineral.FeO: 51,
        Mineral.K: 55,
        Mineral.Th: 58,
        Mineral.U: 60,
    }

    _CACHE = []
    with open(filepath, "r") as input:
        for row in input:
            row = row.strip().split(" ")
            row = filter(len, row)  # remove empty entries
            row = map(float, row)
            row = list(row)

            composition = {}
            for name, column in position_columns.items():
                composition[name] = row[column]

            for mineral in Mineral:
                mu = row[composition_columns[mineral]]
                sigma = row[error_columns[mineral]] ** 0.5
                measurement = NormalDistribution(mu, sigma)
                composition[mineral] = measurement

            min_lon = row[position_columns["min_lon"]]
            min_lat = row[position_columns["min_lat"]]
            max_lon = row[position_columns["max_lon"]]
            max_lat = row[position_columns["max_lat"]]
            bbox = (min_lon, min_lat, max_lon, max_lat)

            _CACHE.append(LpgrsCell(*bbox, composition))

    return _CACHE
