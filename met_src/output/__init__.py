import met_src.output.json as json
import met_src.output.png as png
import met_src.output.shapefile as shapefile


FORMATTERS = {
    "json": json.write,
    "png": png.write,
    "shapefile": shapefile.write,
}


def write(coefficient_map, output_dir, output_format, **kwargs):
    if output_format not in FORMATTERS:
        raise ValueError("Cannot write to unknown output format '{output_format}'")
    write = FORMATTERS[output_format]
    write(coefficient_map, output_dir, **kwargs)
