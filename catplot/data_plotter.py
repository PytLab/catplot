import numpy as np
import matplotlib.pyplot as plt

from functions import line2list


class DataPlotter(object):
    def __init__(self, filename, field=' ', dtype=float):
        self.filename = filename
        self.field = field
        self.dtype = dtype
        #load data
        self.load()

    def load(self):
        "Load all data in file into array."
        data = []
        with open(self.filename, 'r') as f:
            for line in f:
                linedata = line2list(line, field=self.field,
                                     dtype=self.dtype)
                data.append(linedata)
        self.data = np.array(data)

        return data

    def plot2d(self, xcol, ycol):
        x = self.data[:, xcol]
        y = self.data[:, ycol]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color='#104E8B', linewidth=2)

        fig.show()
