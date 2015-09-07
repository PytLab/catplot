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
                if line.startswith('#'):
                    continue
                linedata = line2list(line, field=self.field,
                                     dtype=self.dtype)
                data.append(linedata)
        self.data = np.array(data)

        return data

    def plot2d(self, xcol, ycol):
        "显示特定两列数据"
        x = self.data[:, xcol]
        y = self.data[:, ycol]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color='#104E8B', linewidth=3)

        fig.show()

    def plotall(self):
        "将所有数据一起显示"
        ncols = self.data.shape[1]
        x = self.data[:, 0]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for col in xrange(1, ncols):
            y = self.data[:, col]
            ax.plot(x, y, linewidth=3)
        fig.show()
