"""
Get density of grid of points quickly
"""

from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from nearest_neighbors import load_xs_ys
import numpy as np


def get_density(xs, ys, x_low, x_top, y_low, y_top, level=5):

    x_range = list(filter(lambda x: x_low < x and x < x_top, xs))
    y_range = list(filter(lambda y: y_low < y and y < y_top, ys))

    # catch cases where level is negative (invalid case) and base case (level is 0)
    if level <= 0:
        return [[len(x_range) + len(y_range), {'x_low': x_low, 'x_top': x_top, 'y_low': y_low, 'y_top': y_top}]]

    x_mid = x_low/2 + x_top/2
    y_mid = y_low/2 + y_top/2

    return get_density(x_range, y_range, x_mid, x_top, y_mid, y_top, level-1) \
        + get_density(x_range, y_range, x_low, x_mid, y_mid, y_top, level-1) \
        + get_density(x_range, y_range, x_low, x_mid, y_low, y_mid, level-1) \
        + get_density(x_range, y_range, x_mid, x_top, y_low, y_mid, level-1)


def plot_density(densities):
    fig, ax = plt.subplots(1)

    rects = []
    colour = []

    for density, verticies in densities:
        width = verticies['x_top'] - verticies['x_low']
        height = verticies['y_top'] - verticies['y_low']
        colour.append(density)
        rects.append(
            Rectangle((verticies['x_low'], verticies['y_low']), width, height)
        )

    print('Trying to print')
    p = PatchCollection(np.array(rects))
    p.set_array(np.array(colour))
    ax.add_collection(p)
    plt.colorbar(p)
    plt.xlim((-180, 180))
    plt.ylim((-90, 90))
    plt.show()

    return fig, ax


if __name__ == '__main__':
    FNAME = 'trash.csv'

    xs, ys = load_xs_ys(FNAME)
    densities = get_density(xs, ys, -180, 180, -90, 90, level=3)
    
    fig, ax = plot_density(densities)
    plt.show()
