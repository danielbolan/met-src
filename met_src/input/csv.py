import csv

from met_src.mineral import Mineral
from met_src.sample import Sample
from met_src.normal_distribution import NormalDistribution


def read(input_path: str, target_sample: str = None) -> list[Sample]:
    samples = list()

    with open(input_path) as f:
        reader: list[dict[str, str]] = csv.DictReader(f)

        for row in reader:
            row = {k.lower(): v for k, v in row.items()}
            sample_name = row["name"]

            if target_sample is not None and target_sample != sample_name:
                continue

            compositions = dict()
            for mineral in Mineral:
                mineral_name = mineral.name.lower()
                if mineral_name in row:
                    mu = row[mineral_name]
                    sigma = row[mineral_name + " sigma"]
                    if mu and sigma:
                        print(mu, sigma)
                        compositions[mineral] = NormalDistribution(
                            float(mu), float(sigma)
                        )
                lon, lat = float(row.get("lon")), float(row.get("lat"))

            sample = Sample(sample_name, compositions, lon, lat)
            samples.append(sample)

    return samples
