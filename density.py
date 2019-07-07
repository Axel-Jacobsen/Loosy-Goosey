"""
Get density of grid of points quickly
"""

from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from prep_data import PrepData
import time
import numpy as np


def get_density(data, x_low, x_top, y_low, y_top, level=5):
    """
    Return value of this is a list of lists, of the form
    [[num_points_in_grid, [x_low, x_high, y_low, y_high]],
     [num_points_in_grid, [x_low, x_high, y_low, y_high]], ....]
    """
    data = list(filter(lambda row: x_low < row[1] and row[1] < x_top, data))
    data = list(filter(lambda row: y_low < row[2] and row[2] < y_top, data))

    # catch cases where level is negative (invalid case) and base case (level is 0)
    if level <= 0:
        return [[len(data), {'x_low': x_low, 'x_top': x_top, 'y_low': y_low, 'y_top': y_top}]]

    x_mid = x_low/2 + x_top/2
    y_mid = y_low/2 + y_top/2

    return get_density(data, x_mid, x_top, y_mid, y_top, level-1) \
        + get_density(data, x_low, x_mid, y_mid, y_top, level-1) \
        + get_density(data, x_low, x_mid, y_low, y_mid, level-1) \
        + get_density(data, x_mid, x_top, y_low, y_mid, level-1)


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

    data = PrepData.load_values(FNAME)
    xs, ys = PrepData.load_xs_ys(FNAME)
    plt.scatter(xs, ys, s=2)
    t1 = time.time()
    densities = get_density(data, -180, 180, -90, 90, level=9)
    print('Time to get density: ', time.time() - t1)

    fig, ax = plot_density(densities)
    plt.show()
