#!/usr/bin/env python
"""This script displays histogramms of the decay times for the upper and lower detector for a given dataset of the
Landé factor experiment."""
import numpy as np
import matplotlib.pyplot as plt


def load_data(fname="dpFilt_190325-0148.dat"):
    _data = np.loadtxt(fname, delimiter=',')
    print("Data size before strip: {}".format(len(_data)))
    # remove physically impossible events
    delete = []
    for i, event in enumerate(_data):
        if (event[3] > 0 or event[4] > 0) and (event[5] > 0):
            delete.append(i)
    _data = np.delete(_data, delete, 0)
    print("Data size after strip: {}".format(len(_data)))
    return np.array([_data[:, 3], _data[:, 5]])


if __name__ == '__main__':
    upper, lower = load_data()
    limits = (2, 13)
    n_bins = 100
    ax1 = plt.figure().add_subplot(1, 1, 1)
    ax2 = plt.figure().add_subplot(1, 1, 1)
    ax1.hist(upper, bins=n_bins, range=limits, label='Oberer Detektor', color='C0')
    ax2.hist(lower, bins=n_bins, range=limits, label='Unterer Detektor', color='C1')
    for ax in (ax1, ax2):
        ax.legend(loc='best')
        ax.set_xlim(limits)
        ax.set_xlabel(r'Zerfallszeit $t$ [μs]')
        ax.set_ylabel(r'Anzahl Ereignisse')
    plt.show()
