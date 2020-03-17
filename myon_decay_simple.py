#!/usr/bin/env python
# coding=utf-8
"""
This script performs an unbinned fit of the myon decay with the first 200 usable datapoints of a given dataset.
"""
import numpy as np
import matplotlib.pyplot as plt
# use the kafe2 version supplied from the git submodule, not the system installation to maintain compatibility
from .kafe2.kafe2 import UnbinnedFit, Plot, ContoursProfiler


def simple_decay(t, tau=2.2, fbg=0.1, a=1., b=9.75):
    """Probability density function for the decay time of a myon. The pdf is normalized to the interval (a, b).

    :param t: decay time
    :param fbg: background
    :param tau: expected mean of the decay time
    :param a: lower limit of normalization
    :param b: upper limit of normalization
    :return: probability for decay time x
    """
    pdf1 = np.exp(-t / tau) / tau / (np.exp(-a / tau) - np.exp(-b / tau))
    pdf2 = 1. / (b - a)
    return (1 - fbg) * pdf1 + fbg * pdf2


if __name__ == '__main__':
    data = np.loadtxt("dpFilt_190325-0148.dat", delimiter=',')[:, 2]  # just load double pulses
    limits = (2, 15)
    # only use delta t in between the limits, to avoid underground
    data = data[(data >= limits[0]) & (data <= limits[1])]
    # create the fit object, currently the iminuit minimizer is required due to a bug with the scipy minimizer
    fit = UnbinnedFit(data[0:200], simple_decay, minimizer='iminuit')  # only use first 200 events
    # fix the parameters for normalizing the distribution function
    fit.fix_parameter('a', limits[0])
    fit.fix_parameter('b', limits[1])
    # set the background to physically logical values
    fit.limit_parameter('fbg', (0, 1))
    # set labels
    fit.data_container.label = "lifetime measurements"
    fit.data_container.axis_labels = ['life time ' r'$\tau$' '(µs)', 'Density']
    fit.model_label = "exponential decay law + flat background"
    # assign latex names for the parameters for nicer display
    fit.assign_parameter_latex_names(t='t', tau=r'\tau', fbg='f', a='a', b='b')
    # assign a latex expression for the fit function for nicer display
    fit.assign_model_function_latex_expression("(1-{fbg}) \\frac{{e^{{-{t}/{tau}}}}}"
                                               "{{{tau}(e^{{-{a}/{tau}}}-e^{{-{b}/{tau}}})}}"
                                               "+ {fbg} \\frac{{1}}{{{b}-{a}}}")
    # do the fit
    fit.do_fit()
    fit.report()

    # plot the fit results
    plot = Plot(fit)
    plot.plot(with_asymmetric_parameter_errors=True)

    # create contours
    cpf = ContoursProfiler(fit)
    cpf.plot_profiles_contours_matrix(parameters=['tau', 'fbg'], label_ticks_in_sigma=False)
    plt.show()
