#!/usr/bin/python3
import json
import csv
import sys

from met_src.mineral import Mineral
from met_src.sample import Sample
from met_src.normal_distribution import NormalDistribution


def main(filename: str):
    with open(filename) as json_file:
        json_data = json.load(json_file)

    with open(filename.replace("json", "csv"), "w") as csv_file:
        fieldnames = ["name", "lon", "lat"]
        fieldnames += [mineral.name for mineral in Mineral]
        fieldnames += [mineral.name + " sigma" for mineral in Mineral]
        print(fieldnames)
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()

        for sample_name, sample in json_data.items():
            row = {"name": sample_name}
            if "coordinate" in sample:
                row.update(
                    {
                        "lon": sample["coordinate"]["lon"],
                        "lat": sample["coordinate"]["lat"],
                    }
                )
            for mineral, value in sample["composition"].items():
                mu, sigma = value["mu"], value["sigma"]
                row.update({mineral: mu, mineral + " sigma": sigma})
            writer.writerow(row)


if __name__ == "__main__":
    main(sys.argv[1])
