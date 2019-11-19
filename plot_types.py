#!/usr/bin/env python
"""
This script shows different methods for displaying the density of an one dimensional dataset.
Namely a histogram, the kernel density method and the rug plot
This script requires the python package seaborn, please run "pip install seaborn" before running this script
"""
import numpy as np
import seaborn
import matplotlib.pyplot as plt


if __name__ == '__main__':
    np.random.seed(123)  # fix seed for reproduction
    data = np.random.normal(loc=0, scale=1, size=25)  # generate normal distributed dataset
    # plot histogram, kernel density and rug plot
    fig, ax = plt.subplots()
    seaborn.distplot(data, hist=True, kde=True, rug=True, ax=ax)
    ax.set_xlabel('$x$')
    ax.set_ylabel('Density')
    plt.show()  # show the plot
