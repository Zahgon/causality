import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats
import itertools
from collections import Counter

DEFAULT_BINS = 2

class RobustRegressionTest():
    def __init__(self, y, x, z, data, alpha):
        self.regression = sm.RLM(data[y], data[x+z])
        self.result = self.regression.fit()
        self.coefficient = self.result.params[x][0]
        confidence_interval = self.result.conf_int(alpha=alpha/2.)
        self.upper = confidence_interval[1][x][0]
        self.lower = confidence_interval[0][x][0]

    def independent(self):
        pass

class ChiSquaredTest():
    def __init__(self, y, x, z, data, alpha):
        self.alpha = alpha
        self.total_chi2 = 0.
        self.total_dof = 0
        for xi, yi in itertools.product(x,y):
            tables = data[[xi]+[yi]+z].copy()
            groupby_key = list([zi for zi in z] + [xi])
            tables = tables.join(pd.get_dummies(data[yi],prefix=yi)).groupby(groupby_key).sum()
            del tables[yi]

            z_values = {zi : data.groupby(zi).groups.keys() for zi in z}
            x_values = {xi : data.groupby(xi).groups.keys()}
            y_values = {yi : data.groupby(yi).groups.keys()}

            contingencies = itertools.product(*[z_values[zi] for zi in z])

            for contingency in contingencies:
                contingency_table = tables.loc[contingency].values
                try:
                    chi2, _, dof, _ = scipy.stats.chi2_contingency(contingency_table)
                except ValueError:
                    raise Exception("Not enough data or entries with 0 present: Chi^2 Test not applicable.")
                self.total_dof += dof
                self.total_chi2 += chi2
        self.total_p = 1. - scipy.stats.chi2.cdf(self.total_chi2, self.total_dof)

    def independent(self):
        pass


class MutualInformationTest():
    """
    This is mostly from "Distribution of Mutual Information" by Marcus Hutter.  This MVP implementation
    doesn't contain priors, but will soon be adjusted to include the priors for n_xy.

    It uses a very basic variance estimate on MI to get approximate confidence intervals
    on I(X,Y|Z=z) for each z, then basic error propagation (incorrectly assuming 0 covariance, i.e.
    Cov(I(X,Y|Z=z_i), I(X,Y|Z=z_j)) = 0.  This second assumption results in an underestimate of the
    final confidence interval.
    """
    def __init__(self, y, x, z, X, alpha, variable_types={}):
        self.I, self.dI = self.discrete_mutual_information(x, y, z, X)
        z = scipy.stats.norm.ppf(1.-alpha/2.) # one-sided
        self.dI = z*self.dI

    def independent(self):
        pass

    def discrete_mutual_information(self, x, y, z, X):
        pass

    def max_likelihood_information(self, x, y, X):
        """
        This estimator appears to get very imprecise quickly as the dimensions and
        cardinality of x and y get larger.  It works well for dimensions around 1,
        and cardinality around 5.  Higher dimensions require lower cardinality.  For
        further refinment, I'll have to see if using a prior for I(x,y) helps.
        """
        pass

