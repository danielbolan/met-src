import os
import pathlib

import click

import met_src
from met_src.coefficient_map import CoefficientMap


@click.command()
@click.option(
    "--input-path",
    type=click.Path(file_okay=True, dir_okay=False),
    default=os.path.join(met_src.__path__[0], "data", "samples", "calzada2015.json"),
    help=(
        f"Input file to read from. Accepted file formats: "
        f"{', '.join(met_src.input.FORMATTERS.keys())}"
    ),
)
@click.option(
    "--sample",
    required=False,
    help="If supplied, results will be produced for the given sample.",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default="results",
    help="Directory for output files",
)
@click.option(
    "--output-format",
    type=click.Choice(met_src.output.FORMATTERS.keys(), case_sensitive=False),
    default="png",
    help=(
        f"File format for the output. Accepted file formats:\n"
        f"{', '.join(met_src.output.FORMATTERS.keys())}"
    ),
)

# Shapefile-specific options
@click.option(
    "--zip",
    is_flag=True,
    required=False,
    help="Whether to store output in a zipfile. Only used for shapefile outputs.",
)

# PNG-specific options
@click.option(
    "--dpi",
    required=False,
    default=250.0,
    help="Affects the resolution of PNG images.",
)
@click.option(
    "--show-title",
    is_flag=True,
    required=False,
    help="Whether to show the title in PNG images.",
)
@click.option(
    "--show-axes",
    is_flag=True,
    required=False,
    help="Whether to show the lat/lon axes in PNG images.",
)
def main(input_path, sample, output_dir, output_format, **kwargs):
    """
    This script calculates the overlap coefficents between meteorite samples and
    surface measurements from Lunar Prospector's Gamma Ray Spectrometer (LP-GRS).

    For examples of how to format the input files of your samples, see
    met_src/data/samples/calzada2015.{csv,json} .
    """
    samples = met_src.input.read(input_path, sample)

    output_subdir = os.path.splitext(os.path.split(input_path)[1])[0]
    output_dir = pathlib.Path(output_dir) / output_subdir

    for sample in samples:
        coefficient_map = CoefficientMap.from_sample(sample)
        met_src.output.write(coefficient_map, output_dir, output_format, **kwargs)


@click.command()
@click.pass_context
@click.option(
    "--sample",
    required=False,
    help="If supplied, results will be produced for the given sample.",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    default="results",
    help="Directory for output files",
)
@click.option(
    "--output-format",
    type=click.Choice(met_src.output.FORMATTERS.keys(), case_sensitive=False),
    default="png",
    help=(
        f"File format for the output. Accepted file formats:\n"
        f"{', '.join(met_src.output.FORMATTERS.keys())}"
    ),
)

# Shapefile-specific options
@click.option(
    "--zip",
    is_flag=True,
    required=False,
    help="Whether to store output in a zipfile. Only used for shapefile outputs.",
)

# PNG-specific options
@click.option(
    "--dpi",
    required=False,
    default=250.0,
    help="Affects the resolution of PNG images.",
)
@click.option(
    "--show-title",
    is_flag=True,
    required=False,
    help="Whether to show the title in PNG images.",
)
@click.option(
    "--show-axes",
    is_flag=True,
    required=False,
    help="Whether to show the lat/lon axes in PNG images.",
)
def validate(ctx, sample, output_dir, output_format, **kwargs):
    """
    Run constrainment on the validation set in met_src/data/samples/validation.json.

    If the output format is PNG, it will mark the actual location of the sample for reference.
    """
    input_path = os.path.join(met_src.__path__[0], "data", "samples", "validation.json")
    ctx.forward(
        main,
        input_path=input_path,
        sample=sample,
        output_dir=output_dir,
        output_format=output_format,
        **kwargs,
    )
