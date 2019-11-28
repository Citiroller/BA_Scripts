#!/usr/bin/env python
# coding=utf-8
"""
This script perfoms a single hist fit for a generated dataset of for the upper detector.
This is for comparing a single hist fit with the MultiFit from lande_factor.py
"""
import numpy as np
import matplotlib.pyplot as plt
from kafe2 import HistContainer, HistFit, Plot
from lande_factor import DataGenerator, events_top, decay_top


if __name__ == '__main__':
    from scipy.constants import e, physical_constants
    g_ref = 2.0023318418  # lande factor of the myon
    tau_ref = 2.1969811e-6  # mean decay time
    b = 5e-3  # magnetic field in T
    m = physical_constants["muon mass"][0]
    omega_ref = g_ref * e * b / (2 * m)
    print("Expected omega ist {}".format(omega_ref))
    delta = 9.85  # phase delay
    gen_pars_top = {'tau': tau_ref * 1e6, 'k_top': 0.8, 'a_bar_top': 0.00125, 'omega': omega_ref * 1e-6, 'delta': delta,
                    'f_top': 2e-2}
    limits = (2, 13)
    gen = DataGenerator(events_top, limits=limits, size=int(1e6), **gen_pars_top)
    data = HistContainer(n_bins=100, bin_range=limits, fill_data=gen.gen_data())
    # do pre fit
    pre_fit = HistFit(data, decay_top, minimizer='iminuit')
    pre_fit.do_fit()
    # final hist fit
    fit = HistFit(data, events_top, cost_function='nllr', minimizer='iminuit')
    starting_values = {'omega': 3, 'delta': np.pi, 'a_bar_top': 1e-4}
    starting_values.update(pre_fit.parameter_name_value_dict)
    fit.set_parameter_values(**starting_values)
    par_names = {'x': 't', 'tau': r'\tau', 'omega': r'\omega', 'delta': r'\delta',
                 'k_top': r'K_0', 'a_bar_top': r'\bar{A}_0', 'f_top': 'f_0'}
    fit.assign_model_function_latex_name("F_0")
    fit.assign_model_function_latex_expression(r'{k_top}\cdot\exp{{\left(-\frac{x}{tau}\right)}}'
                                               r'\left(1+{a_bar_top}\cdot\cos\left({omega}{x}+{delta}\right)\right)'
                                               r'+{f_top}')
    fit.assign_parameter_latex_names(**par_names)
    fit._model_function._formatter._latex_x_name = '{t}'  # workaround, because it's currently hardcoded
    fit.do_fit()
    fit.report()
    plot = Plot(fit)
    plot.set_keywords('data', [dict(markersize=3, label='Upper Detector')])
    plot.set_keywords('model', [dict(label='Upper Model')])
    plot.set_keywords('model_density', [dict(label='Upper Model Density')])
    plot.plot()
    plot.axes[0]['main'].set_xlabel(r'$t$ [μs]')  # change axis label, this might change in the release version
    plt.show()
