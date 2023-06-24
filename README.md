
# Continuous-Domain Constrainment of Meteorite Source Regions

Code used to produce the [results presented](https://sservi.directus.app/assets/2483b7e0-a336-443d-8739-3d5f4756e1fb.pdf#page=33) at the [European Lunar Symposium](https://sservi.nasa.gov/els2023/) on June 28, 2023.

If you don't want to run this code, you can download all output files at [dcb.lu/met_src_results](https://dcb.lu/met_src_results).

## Installation

Instructions are written with Ubuntu 22.04 in mind. If you have instructions for getting this running on other systems, I'd love to include them here.

```bash
python3 -m pip install poetry
poetry install

# if you don't already have GDAL installed
sudo apt install gdal-bin libgdal-dev

# poetry can't quite handle installing the GDAL wheel yet, and needs to be installed separately
# https://github.com/python-poetry/poetry/issues/845
# Results as presented were made with GDAL 3.4.1
poetry run python3 -m pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
poetry add gdal==`gdal-config --version`
```

## Usage
```bash
# All samples from [calzada2015]
poetry run main

# All samples, output shapefiles instead of png
poetry run main --out-format shapefile
poetry run main --out-format shapefile --sample "Dho 287" --zip

# Run on one sample only
poetry run main --sample "Dho 287"

# Run on a different file. Currently handles json and csv files. See below for formats
poetry run main --input my_samples.json
poetry run main --input my_samples.json --sample "Dho 287" --show-title --show-axes --dpi 300

# Run validation on Apollo and Luna samples
poetry run validation

# Print all flags
poetry run main --help
```

## Data Formats

This tool currently can handle JSON and CSV as input, and can output JSON, PNG, and shapefiles.

### Input

Examples of valid inputs can be found in `met_src/data/samples/`.

#### JSON

JSON needs to be structured as follows:
```
{
    "My Sample": {
        "coordinate": {
            "lon": -23.42,
            "lat": -3.01
        },
        "composition": {
            "FeO": {
                "mu": 0.1234,
                "sigma": 0.5678
            },
            "TiO2": {
                "mu": 0.02,
                "sigma": 0.07
            },
            ...
        }
    },
    "My Sample 2": {
        "composition": {
    ...
```

The coordinate field is optional, and only used for validation of known sample locations.

#### CSV

CSV files need to have headers like this:
```csv
name,      lon,    lat,   TiO,   TiO sigma, FeO, FeO sigma,...
My Sample, -23.42, -3.01, 0.123, 0.234,     0.2, 0.4,      ...
MySample2, -11.33, 55.23, 0.321, 0.432,        ,    ,      ...
```
Again, lon and lat can be omitted and are only used for validation.
Field names are case-insensitive. If a sample doesn't have a value for a particular mineral, it's okay to leave it blank, but make sure each row still has the correct number of fields.

### Output

#### JSON
Outputs a GeoJSON file. If a ground truth location is supplied (as in validation sets) it will be added as a slightly non-standard field in the root object.

#### PNG
Outputs a raster image of the map. There are three additional flags you can use to modify the output of PNGS:
```
--dpi FLOAT: Change the resolution of the output image. Higher DPI means higher resolution. Default is 250.
--show-title: Add a title to the top of the image, based on the name of the sample.
--show-axes: Show the lat/lon axes along the edges of the map.
```

#### Shapefile
Outputs an ESRI Shapefile. Coefficients are stored in the `coeff` field.

If the `--zip` flag is supplied, it will make a zip file of the shapefiles as well.

## Citations

This work is built on top of Abigail Calzada Díaz's PhD thesis:

```bibtex
@article{calzada2015,
  title={Constraining the source regions of lunar meteorites using orbital geochemical data},
  author={Calzada-Diaz, Abigail and Joy, KH and Crawford, IA and Nordheim, TA},
  journal={Meteoritics \& Planetary Science},
  volume={50},
  number={2},
  pages={214--228},
  year={2015},
  doi={10.1111/maps.12412}
}
```

The data comes from Lunar Prospector's Gamma Ray Spectrometer (LP-GRS):
```bibtex
@article{prettyman2006,
  title={Elemental composition of the lunar surface: Analysis of gamma ray spectroscopy data from Lunar Prospector},
  author={Prettyman, Thomas H and Hagerty, JJ and Elphic, RC and Feldman, WC and Lawrence, DJ and McKinney, GW and Vaniman, DT},
  journal={Journal of Geophysical Research: Planets},
  volume={111},
  number={E12007},
  year={2006},
  doi={10.17189/1519384}
}
```

The background image used in png outputs was provided by [Solar System Scope](https://www.solarsystemscope.com/textures/) under a CC-BY 4.0 license.
