"""
File to find nearest N = 5 neighbors to (x,y)
Bounds: x in (-180, 180), y in (-90,90)
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
import time
from prep_data import PrepData


def dist(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


MAX_D = dist(180, 90, -180, -90)


# Get the start index by first assuming that points are evenly distributed across all latitudes and longitudes
def get_start_index(arr, x, tuple_pos=1):
    i = int((x + 180) / 360 * len(arr))
    if x < arr[i][tuple_pos]:
        while x < arr[i][tuple_pos]:
            i = i - 1
    else:
        while x > arr[i][tuple_pos]:
            i = i + 1

    return i


def get_lowest_N(lowest_N, N, unit_data, index=3):
    # unit_data: (id, x, y, d)
    for i, v in enumerate(lowest_N):
        if unit_data[index] < v[index]:
            lowest_N.insert(i, unit_data)
            lowest_N = lowest_N[0:N]
            break
        elif unit_data[index] == v[index]:
            # we are dealing w/ a duplicate so break
            break

    return lowest_N, lowest_N[-1][3]


def get_nearest_neighbors(x, y, data, N=5, tune=200):
    # Let CLOSE_DIST be either N + tune, or 0.1% of the points; we will look
    # at 2 * CLOSE_POINTS
    # NOTE: tune=200 is just a guess; you would want tune to be large enough that,
    #       for small data sets, we would get all candidate 'close points'
    CLOSE_DIST = max(N + tune, int(len(data) * 0.01))
    lowest_N = [(None, None, None, MAX_D) for _ in range(N)]
    current_max_d = MAX_D

    start_index_x = get_start_index(data, x)

    # Do we cut off before we calculate the distances, or after we calculate the distance but before get_lowest_N(...) (at the cost of more values being calculated? Go with first for now, test to confirm later)
    for i in range(1, CLOSE_DIST):
        # if y val is less than max D, continue w/ calcs
        v1 = data[start_index_x + i]
        if abs(x - v1[1]) < current_max_d and abs(y - v1[2]) < current_max_d:
            d1 = dist(x, y, v1[1], v1[2])
            v1.append(d1)
            lowest_N, current_max_d = get_lowest_N(lowest_N, N, v1)

        v2 = data[start_index_x - i]
        if abs(x - v2[1]) < current_max_d and abs(y - v2[2]) < current_max_d:
            d2 = dist(x, y, v2[1], v2[2])
            v2.append(d2)
            lowest_N, current_max_d = get_lowest_N(lowest_N, N, v2)

    return lowest_N


if __name__ == '__main__':

    FNAME = 'trash.csv'
    X, Y = 0, 0

    print("Preparing data")
    data = PrepData.load_and_sort_values(FNAME)

    print("Finding nearest points")
    tt = 0
    for i in range(100):
        t1 = time.time()
        lowest_n = get_nearest_neighbors(X, Y, data, N=5)
        tt += time.time() - t1
    print('Points found; Average execution time: {}'.format(tt/100))

    print('Plotting points')
    low_xs = [r[1] for r in lowest_n]
    low_ys = [r[2] for r in lowest_n]

    xs, ys = PrepData.load_xs_ys(FNAME)
    plt.scatter(xs, ys, s=3, zorder=0)
    plt.scatter(low_xs, low_ys, 5, zorder=0)
    plt.scatter(X, Y, s=9, zorder=2, c='0')
    plt.axis('equal')
    plt.xlim((-180, 180))
    plt.ylim((-90, 90))

    print('DONE')
    plt.show()
