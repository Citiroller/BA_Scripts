#!/usr/bin/env python
# coding=utf-8
"""
This example illustrates the difference between unbinned and histogram fits. To achieve this a normal distributed
dataset is generated. Then the first n elements of this dataset are fitted with an unbinned fit and histogram fits with
different binning. This procedure is done for multiple values of n
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from multiprocessing import Pool
# use the kafe2 version supplied from the git submodule, not the system installation to maintain compatibility
from .kafe2.kafe2 import UnbinnedFit, HistContainer, HistFit


np.random.seed(1009131719)  # fix the seed for reproduction


def pdf(x, mu=0, sigma=1):
    return norm(mu, sigma).pdf(x)


def cdf(x, mu=0, sigma=1):
    return norm(mu, sigma).cdf(x)


class Fitters:
    def __init__(self, size, low, high, steps):
        self.data = self.gen_data(int(size))
        self.steps = self.gen_steps(low, high, steps)
        self.borders = (np.min(self.data), np.max(self.data))
        self.n_bins = None
        self.minimizer = "iminuit"

    @staticmethod
    def gen_data(size=100000):
        return np.random.standard_normal(size)

    @staticmethod
    def gen_steps(low, high, size, log=True):
        if log:
            low = np.log10(low)
            high = np.log10(high)
            return np.logspace(low, high, num=size, dtype=int)-1
        else:
            return np.linspace(low, high, num=size, dtype=int)-1

    def do_unbinned(self, step):
        _data = self.data[0:step]
        _fit = UnbinnedFit(_data, model_density_function=pdf, minimizer=self.minimizer)
        _fit.do_fit()
        _params = _fit.parameter_values
        _errors = _fit.parameter_errors
        return [_params, _errors]

    def do_hist(self, step):
        _hist_cont = HistContainer(n_bins=self.n_bins, bin_range=self.borders, fill_data=self.data[0:step])
        _hist_fit = HistFit(_hist_cont, model_density_function=pdf, model_density_antiderivative=cdf,
                            minimizer=self.minimizer)
                            # cost_function=HistCostFunction_Chi2(errors_to_use=None))
        _hist_fit.do_fit()
        _params = _hist_fit.parameter_values
        _errors = _hist_fit.parameter_errors
        return [_params, _errors]

    def do_fits(self):
        _result = []
        with Pool(processes=10) as p:
            _result.append(p.map(self.do_unbinned, [i for i in self.steps]))
            for n in [3, 6, 10, 50]:
                self.n_bins = n
                _result.append(p.map(self.do_hist, [i for i in self.steps]))
        return np.array(_result)


if __name__ == '__main__':
    fitters = Fitters(1e4, 4, 1e4, 50)
    result = fitters.do_fits()
    mu_lim = [-0.25, 0.25]
    sig_lim = [0.2, 1.1]
    helper_dict = {3: {'index': 1, 'loc': 0, 'title': '3 Bins'}, 6: {'index': 2, 'loc': 1, 'title': '6 Bins'},
                   10: {'index': 3, 'loc': 2, 'title': '10 Bins'}, 50: {'index': 4, 'loc': 3, 'title': '50 Bins'},
                   0: {'index': 0, 'loc': 4, 'title': 'Unbinned'}}
    fig, axs = plt.subplots(nrows=5, ncols=2, sharex='col')
    fig.set_size_inches(8.26, 11.7)
    fig.set_dpi(300)
    for key, params in helper_dict.items():
        index = params['index']
        loc = params['loc']
        title = params['title']
        # generate plot for the fitted values of mu
        ax = axs[loc, 0]
        ax.errorbar(fitters.steps, result[index, :, 0, 0], yerr=result[index, :, 1, 0], fmt='o')
        ax.plot(fitters.steps, np.zeros(len(fitters.steps)), 'r--')
        ax.set_ylim(mu_lim[0], mu_lim[1])
        ax.set_xscale('log')
        ax.set_title(title+' $\\mu$')
        ax.set_ylabel(r'$\mu$ best fit')
        ax.set_xlabel('Number of Datapoints')
        ax.label_outer()
        # generate plot for the fitted value of sigma
        ax = axs[loc, 1]
        ax.errorbar(fitters.steps, result[index, :, 0, 1], yerr=result[index, :, 1, 1], fmt='o')
        ax.plot(fitters.steps, np.ones(len(fitters.steps)), 'r--')
        ax.set_ylim(sig_lim[0], sig_lim[1])
        ax.set_title(title+r' $\sigma$')
        ax.set_ylabel(r'$\sigma$ best fit')
        ax.set_xscale('log')
    plt.xlabel('Number of Datapoints')
    plt.tight_layout()
    plt.savefig('UnbinnedBinned.png')
