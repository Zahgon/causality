import pandas as pd
import numpy as np
import scipy.stats as ss
from statsmodels.nonparametric.kernel_regression import KernelReg
from sklearn.ensemble import RandomForestRegressor


class CausalDataFrame(pd.DataFrame):
    def zmean(self, *args, **kwargs):
        pass

    def zplot(self, *args, **kwargs):
        pass

    def _line_zplot(self, *args, **kwargs):
        pass

    def _bootstrapped_mean_zplot(self, *args, **kwargs):
        pass

    def _bootstrap_statistic(self, f, df, *args, **kwargs):
        pass

    def _get_model(self, *args, **kwargs):
        pass

class KernelModelWrapper(object):
    def __init__(self):
        self.model = None
        self.variable_types = {}
        self.X_shape = None
        self.y_shape = None

    def fit(self, X, y, variable_types={}):
        pass

    def predict(self, X):
        pass
