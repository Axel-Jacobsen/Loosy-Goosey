"""
File to find nearest N = 5 neighbors to (x,y)
Bounds: x in (-180, 180), y in (-90,90)
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
import time

FNAME = 'trash.csv'


def dist(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


MAX_D = dist(180, 90, -180, -90)


def sort_by_second(r):
    return r[1]


def load_vals(fname):
    x_data = {}
    y_data = {}
    with open(fname) as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_data[row['id']] = float(row['x'])
            y_data[row['id']] = float(row['y'])

    return x_data, y_data


def dict_to_arr(d):
    return [(key, float(d[key])) for key in d.keys()]


def start_index(arr, v, tuple_pos=1):
    i = 0
    while v > arr[i][tuple_pos]:
        i = i + 1
    return i

def get_lowest_N(lowest_N, N, id, d, x_val, y_val):
    for i, v in enumerate(lowest_N):
        if d < v[1]:
            lowest_N.insert(i, (id, d, x_val, y_val))
            lowest_N = lowest_N[0:N]
            break
        elif d == v[1]:
            # we are dealing w/ a duplicate so break
            break
    return lowest_N


def get_nearest_neighbors(x, y, , y_dict, N=5):
    lowest_N = [(None, MAX_D) for _ in range(N)]
    CLOSE_SIZE = N + 200

    start_index_x = start_index(x_data, x)
    # start_index_y = start_index(y_data, y)

    close_xs = x_data[(start_index_x - CLOSE_SIZE) : (start_index_x + CLOSE_SIZE)]
    # close_ys = y_data[(start_index_y - CLOSE_SIZE) : (start_index_y + CLOSE_SIZE)]

    xs_x = [v[1] for v in close_xs]
    xs_y = [y_dict[v[0]] for v in close_xs]
    # ys_y = [v[1] for v in close_ys]
    # ys_x = [x_dict[v[0]] for v in close_ys]

    plt.scatter(xs_x, xs_y, c='k')
    # plt.scatter(ys_x, ys_y, c='k')

    for x_row in close_xs:
        x_val = x_row[1]
        y_val = y_dict[x_row[0]]
        id    = x_row[0]
        d     = dist(x, y, x_val, y_val)

        lowest_N = get_lowest_N(lowest_N, N, id, d, x_val, y_val)

    # for y_row in close_ys:
    #     x_val = x_dict[y_row[0]]
    #     y_val = y_row[1]
    #     id    = y_row[0]
    #     d     = dist(x, y, x_val, y_val)

    #     lowest_N = get_lowest_N(lowest_N, N, id, d, x_val, y_val)

    assert len(lowest_N) == 20

    return lowest_N


def prep_data(fname):
    x_dict, y_dict = load_vals(FNAME)
    x_data_arr = dict_to_arr(x_dict)
    y_data_arr = dict_to_arr(y_dict)
    x_data_arr.sort(key=sort_by_second)
    y_data_arr.sort(key=sort_by_second)
    return x_data_arr, y_data_arr, x_dict, y_dict


def plot_vals(fname):
    xs, ys = [], []
    with open(fname) as f:
        reader = csv.DictReader(f)
        for row in reader:
            xs.append(float(row['x']))
            ys.append(float(row['y']))
    return xs, ys


if __name__ == '__main__':

    '''
    TODO: select close points with a radius
    '''
    print("Preparing data")
    x_data, y_data, x_dict, y_dict = prep_data(FNAME)

    print("Finding nearest points")
    t1 = time.time()
    lowest_n = get_nearest_neighbors(0, 0, x_data, y_data, x_dict, y_dict, N=20)
    t = time.time() - t1
    print('Time to process: {:.3f} s'.format(t))

    low_xs = [r[2] for r in lowest_n]
    low_ys = [r[3] for r in lowest_n]

    xs, ys = plot_vals(FNAME)
    plt.scatter(xs, ys, s=3)
    plt.scatter(low_xs, low_ys, 5)
    plt.scatter(0, 0, s=9)
    plt.axis('equal')
    plt.show()

    print('DONE')
