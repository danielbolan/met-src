import json

from met_src.normal_distribution import NormalDistribution
from met_src.mineral import Mineral
from met_src.sample import Sample


def read(input_path: str, target_sample: str = None) -> list[Sample]:
    print(f"parsing JSON from {input_path}")
    with open(input_path) as input_file:
        json_data = json.load(input_file)

    if target_sample is not None and target_sample in json_data:
        json_data = {target_sample: json_data[target_sample]}

    samples = list()
    for sample_name, sample in json_data.items():
        composition = dict()
        for mineral, value in sample["composition"].items():
            distribution = NormalDistribution(value["mu"], value["sigma"])
            composition[Mineral[mineral]] = distribution

        parsed_sample = Sample(sample_name, composition)

        if "coordinate" in sample:
            parsed_sample.lon = sample["coordinate"]["lon"]
            parsed_sample.lat = sample["coordinate"]["lat"]

        samples.append(parsed_sample)

    return samples
