#!/usr/bin/env python
# coding=utf-8
"""
This script generates a random poisson dataset and performs an unbinned likelihood fit of a poisson distribution on this
dataset. Finally, the likelihood function under variation of the parameter λ is displayed.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
# use the kafe2 version supplied from the git submodule, not the system installation to maintain compatibility
from .kafe2.kafe2 import UnbinnedFit, ContoursProfiler

LOW, HIGH = 0, 20  # limits for generating data
P = 4  # parameter of poisson distribution for generating data
np.random.seed(1578839424)  # fix seed for consistent reproduction


def poisson(x, p):
    return p**x/factorial(x)*np.exp(-p)


def gen_data(length=100):
    _data = []
    while len(_data) < length:
        x = np.random.randint(LOW, HIGH)
        y = np.random.rand()
        if y <= poisson(x, P):
            _data.append(x)
    print("Mean of data is {:3.2f}".format(np.mean(_data)))
    return _data


if __name__ == "__main__":
    data = gen_data(200)
    fit = UnbinnedFit(data, poisson)
    fit.assign_parameter_latex_names(p=r'\lambda')
    fit.do_fit()
    fit.report(asymmetric_parameter_errors=True)
    # create likelihood Plot
    fig = plt.figure(figsize=(8, 8))
    ax = plt.gca()
    cpf = ContoursProfiler(fit, profile_subtract_min=True)
    cpf.plot_profile('p', label_ticks_in_sigma=False, target_axes=ax)
    # cpf.plot_profiles_contours_matrix(show_grid_for='all', show_error_span_profiles=True, label_ticks_in_sigma=False)
    # plt.subplots_adjust(left=0.5)
    plt.tight_layout()
    plt.show()  # show the plot
