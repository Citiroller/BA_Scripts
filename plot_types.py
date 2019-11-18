# This script requires the python package seaborn
# please run pip install seaborn before running this script

import numpy as np
import seaborn
import matplotlib.pyplot as plt


if __name__ == '__main__':
    np.random.seed(123)  # fix seed for reproduction
    data = np.random.normal(loc=0, scale=1, size=25)  # generate normal distributed dataset
    # plot histogram, kernel density and rug plot
    seaborn.distplot(data, hist=True, kde=True, rug=True)
    plt.show()  # show the plot