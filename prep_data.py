import csv


class PrepData():

    @staticmethod
    def load_values(fname):
        data = []
        with open(fname) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append([row['id'], float(row['x']), float(row['y'])])

        return data

    @staticmethod
    def load_and_sort_values(fname):
        data = PrepData.load_values(fname)
        # Sort by the x (i.e. longitude)
        data.sort(key=(lambda r: r[1]))

        return data

    @staticmethod
    def load_xs_ys(fname):
        xs, ys = [], []
        with open(fname) as f:
            reader = csv.DictReader(f)
            for row in reader:
                xs.append(float(row['x']))
                ys.append(float(row['y']))

        return xs, ys
