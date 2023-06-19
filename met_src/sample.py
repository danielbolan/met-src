from dataclasses import dataclass

from met_src.mineral import Mineral
from met_src.normal_distribution import NormalDistribution


@dataclass
class Sample:
    name: str
    composition: dict[Mineral, NormalDistribution]
    lon: float = None
    lat: float = None
