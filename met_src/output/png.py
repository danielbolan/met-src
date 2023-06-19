import pathlib
import os

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

import met_src
from met_src.coefficient_map import CoefficientMap, MapCell


def get_cmap():
    """
    Modified version of matplotlib's 'magma' colormap, where the lowest values have their alpha values reduced.
    """
    cmap = plt.cm.magma(np.linspace(0, 1, 256))
    alpha_fade_in = 96
    cmap[:alpha_fade_in, 3] = np.linspace(0, 1, alpha_fade_in)
    return mpl.colors.ListedColormap(cmap, "magma_fade_in", N=cmap.shape[0])


def get_pyplot_patch(cell: MapCell):
    origin = (cell.min_lon, cell.min_lat)
    width = cell.max_lon - cell.min_lon
    height = cell.max_lat - cell.min_lat
    return mpl.patches.Rectangle(origin, width, height)


def write(coefficient_map: CoefficientMap, output_dir: pathlib.Path, **kwargs):
    """
    Output the map of overlap coefficients as a PNG using pyplot.

    There are three PNG-specific options available:
    --dpi: Change the resolution of the image. Defaults to 250.
    --show-title: Whether to display the sample name as a title above the map.
    --show-axes: Whether to display the lat/lon axes along the edge of the map.
    """
    plt.rcParams["figure.dpi"] = kwargs.get("dpi", 250)
    fig, ax = plt.subplots(1)
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    ax.set_aspect(1)
    plt.box(False)

    plt.xlabel("Longitude (°)")
    plt.ylabel("Latitude (°)")
    plt.axis(kwargs.get("show-axes"))
    if kwargs.get("show-title"):
        plt.title(coefficient_map.sample_name)

    bg_path = os.path.join(met_src.__path__[0], "data", "img", "2k_moon.jpg")
    bg_img = plt.imread(bg_path)
    ax.imshow(bg_img, extent=(-180, 180, -90, 90))

    patches = [get_pyplot_patch(cell) for cell in coefficient_map.cells]
    values = [cell.coefficient for cell in coefficient_map.cells]
    patch_collection = mpl.collections.PatchCollection(
        patches,
        array=values,
        cmap=get_cmap(),
    )
    ax.add_collection(patch_collection)

    lon, lat = coefficient_map.truth_lon, coefficient_map.truth_lat
    if lon is not None and lat is not None:
        ax.scatter(lon, lat, marker="o", color="#00000033", s=10)
        ax.scatter(lon, lat, marker="x", color="white", s=10, linewidth=1)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{coefficient_map.sample_name}.png"
    print(f"writing to {output_path}")
    plt.savefig(
        output_path,
        pad_inches=0,
        bbox_inches="tight",
        transparent=True,
    )
    # plt.show()
    plt.close()
