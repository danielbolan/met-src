import pathlib
import sys
import zipfile

from osgeo import ogr, osr

from met_src.coefficient_map import CoefficientMap, MapCell


def build_wkt_from_cell(cell: MapCell) -> str:
    return (
        f"POLYGON(("
        f"{cell.min_lon} {cell.min_lat}, "
        f"{cell.min_lon} {cell.max_lat}, "
        f"{cell.max_lon} {cell.max_lat}, "
        f"{cell.max_lon} {cell.min_lat}, "
        f"{cell.min_lon} {cell.min_lat}"
        f"))"
    )


def get_srs() -> osr.SpatialReference:
    srs = osr.SpatialReference()
    srs.ImportFromESRI(
        [
            'GEOGCS["Moon 2000",'
            'DATUM["D_Moon_2000",'
            'SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],'
            'PRIMEM["Greenwich",0],'
            'UNIT["Degree",0.017453292519943295]]'
        ]
    )
    return srs


def create_map_layer(coefficient_map: CoefficientMap, data_source: ogr.DataSource):
    """
    Add each cell in a CoefficientMap to a new layer in the shapefile.
    Field name is shortened to 'coeff' since they can't be longer than 10 characters.
    """
    srs = get_srs()
    layer: ogr.Layer = data_source.CreateLayer("coefficients", srs, ogr.wkbPolygon)
    layer.CreateField(ogr.FieldDefn("coeff", ogr.OFTReal))
    layer_definition = layer.GetLayerDefn()
    for cell in coefficient_map.cells:
        wkt = build_wkt_from_cell(cell)
        geometry = ogr.CreateGeometryFromWkt(wkt)

        feature = ogr.Feature(layer_definition)
        feature.SetField("coeff", cell.coefficient)
        feature.SetGeometry(geometry)
        layer.CreateFeature(feature)

        feature = None
        geometry = None


def zip_files(output_dir: pathlib.Path, name: str):
    with zipfile.ZipFile(output_dir / f"{name}.zip", "w") as f:
        for ext in ["shp", "dbf", "prj", "shx"]:
            f.write(output_dir / f"{name}.{ext}", arcname=f"{name}.{ext}")


def write(coefficient_map: CoefficientMap, output_dir: pathlib.Path, **kwargs):
    """
    Output the map of overlap coefficients as a shapefile.

    There is one shapefile-specific flag available to use, stored in kwargs if supplied:
    --zip: Whether to also produce a .zip bundle of the output files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    name = coefficient_map.sample_name
    output_path: pathlib.Path = output_dir / f"{name}.shp"

    driver: ogr.Driver = ogr.GetDriverByName("Esri Shapefile")
    data_source: ogr.DataSource = driver.CreateDataSource(str(output_path))

    print("Writing shapefile to", output_path)
    create_map_layer(coefficient_map, data_source)
    # add_ground_truth_layer(coefficient_map, data_source)

    data_source = None

    if kwargs.get("zip"):
        zip_files(output_dir, name)
