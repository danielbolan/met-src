from dataclasses import dataclass

import met_src.lpgrs
from met_src.sample import Sample


@dataclass
class MapCell:
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float
    coefficient: float


@dataclass
class CoefficientMap:
    sample_name: str
    cells: list[MapCell]
    truth_lon: float = None
    truth_lat: float = None

    def from_sample(sample: Sample):
        """
        Produce a CoefficentMap by computing the overlap coefficient between the given sample
        and each cell in the LP-GRS dataset.
        """
        cells = list()
        for lpgrs_cell in met_src.lpgrs.get_lpgrs_data():
            coefficient = 1
            for mineral, sample_distribution in sample.composition.items():
                lpgrs_distribution = lpgrs_cell.composition[mineral]
                coefficient *= sample_distribution.overlap_coefficient(
                    lpgrs_distribution
                )
            bbox = (
                lpgrs_cell.min_lat,
                lpgrs_cell.min_lon,
                lpgrs_cell.max_lat,
                lpgrs_cell.max_lon,
            )
            cell = MapCell(*bbox, coefficient)
            cells.append(cell)

        coefficient_map = CoefficientMap(sample.name, cells)

        if sample.lon:
            coefficient_map.truth_lon = sample.lon
        if sample.lat:
            coefficient_map.truth_lat = sample.lat

        return coefficient_map
