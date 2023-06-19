from pathlib import Path
import json

from met_src.coefficient_map import CoefficientMap


def write(coefficient_map: CoefficientMap, output_dir: Path, **kwargs):
    """
    Writes a (slightly-nonstandard) geoJSON file.

    GeoJSON files are usually assumed to use WGS84, which obviously isn't the case here.

    The ground_truth object is technically not a geoJSON object but a foreign memeber,
    but might be able to be used as one anyways.
    """
    output = {
        "name": coefficient_map.sample_name,
        "type": "FeatureCollection",
    }

    output["features"] = []
    for cell in coefficient_map.cells:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [cell.min_lon, cell.min_lat],
                        [cell.min_lon, cell.max_lat],
                        [cell.max_lon, cell.max_lat],
                        [cell.max_lon, cell.min_lat],
                        [cell.min_lon, cell.min_lat],
                    ]
                ],
            },
            "properties": {
                "coefficient": cell.coefficient,
            },
        }
        output["features"].append(feature)

    lon, lat = coefficient_map.truth_lon, coefficient_map.truth_lat
    if lon is not None and lat is not None:
        output["ground_truth"] = {
            "type": "Point",
            "coordinates": [lon, lat],
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{coefficient_map.sample_name}.json"
    print(f"writing JSON to {output_path}")

    with open(output_path, "w") as output_file:
        json.dump(output, output_file, indent=4)
