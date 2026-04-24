import pandas as pd
from statsmodels.nonparametric.kernel_density import KDEMultivariateConditional, KDEMultivariate, EstimatorSettings
from statsmodels.nonparametric.kernel_regression import KernelReg
import itertools
from scipy.integrate import nquad
from scipy import stats
import numpy as np
from networkx.algorithms import is_directed_acyclic_graph

try:
    xrange
except NameError:
    xrange = range

class CausalEffect(object):
    def __init__(self, X, causes, effects, admissable_set=[], variable_types=None, expectation=False, density=True):
        """
        We want to calculate the causal effect of X and Y through
        back-door adjustment, P(Y|do(X)) = Sum( P(Y|X,Z)P(Z), Z) 
        for some admissable set of control variables, Z.  First we 
        calculate the conditional density P(Y|X,Z), then the density
        P(Z).  We find the support of Z so we can properly sum over
        it later.  variable_types are a dictionary with the column name
        pointing to an element of set(['o', 'u', 'c']), for 'ordered',
        'unordered discrete', or 'continuous'.
        """
        conditional_density_vars = causes + admissable_set
        self.causes = causes
        self.effects = effects
        self.admissable_set = list(admissable_set) # uses a list internally; AdjustForDirectCauses.admissable_set returns a set
        self.conditional_density_vars = conditional_density_vars

        if len(X) > 300 or max(len(causes+admissable_set),len(effects+admissable_set)) >= 3:
            self.defaults=EstimatorSettings(n_jobs=4, efficient=True)
        else:
            self.defaults=EstimatorSettings(n_jobs=-1, efficient=False)
        
        if variable_types:
            self.variable_types = variable_types
            dep_type      = [variable_types[var] for var in effects]
            indep_type    = [variable_types[var] for var in conditional_density_vars]
            density_types = [variable_types[var] for var in admissable_set]
        else:
            self.variable_types = self.__infer_variable_types(X)

        if 'c' not in variable_types.values():
            bw = 'cv_ml'
        else:
            bw = 'normal_reference'


        if admissable_set:            
            self.density = KDEMultivariate(X[admissable_set], 
                                  var_type=''.join(density_types),
                                  bw=bw,
                                  defaults=self.defaults)
        
        self.conditional_density = KDEMultivariateConditional(endog=X[effects],
                                                         exog=X[conditional_density_vars],
                                                         dep_type=''.join(dep_type),
                                                         indep_type=''.join(indep_type),
                                                         bw=bw,
                                                         defaults=self.defaults)
        if expectation:
            self.conditional_expectation = KernelReg(X[effects].values,
                                                 X[conditional_density_vars].values,
                                                 ''.join(indep_type),
                                                 bw='cv_ls')

        self.support = self.__get_support(X)
        
        self.discrete_variables = [ variable for variable, var_type in self.variable_types.items() if var_type in ['o', 'u']]
        self.discrete_Z = list(set(self.discrete_variables).intersection(set(admissable_set)))
        self.continuous_variables = [ variable for variable, var_type in self.variable_types.items() if var_type == 'c' ]
        self.continuous_Z = list(set(self.continuous_variables).intersection(set(admissable_set)))
       
 
    def __infer_variable_types(self,X):
        """
        fill this in later.
        """
        pass
       
 
    def __get_support(self, X):
        """
        find the smallest cube around which the densities are supported,
        allowing a little flexibility for variables with larger bandwidths.
        """
        pass

        
    def integration_function(self,*args):
        # takes continuous z, discrete z, then x
        pass

    
    def expectation_integration_function(self, *args):
        pass

    
    def pdf(self, x):
        """
        Currently, this does the whole sum/integral over the cube support of Z.
        We may be able to improve this by taking into account how the joint
        and conditionals factorize, and/or finding a more efficient support.
        
        This should be reasonably fast for |Z| <= 2 or 3, and small enough discrete
        variable cardinalities.  It runs in O(n_1 n_2 ... n_k) in the cardinality of
        the discrete variables, |Z_1| = n_1, etc.  It likewise runs in O(V^n) for n
        continuous Z variables.  Factorizing the joint/conditional distributions in
        the sum could linearize the runtime.
        """
        pass

       
 
    def expected_value( self, x):
        """
        Currently, this does the whole sum/integral over the cube support of Z.
        We may be able to improve this by taking into account how the joint
        and conditionals factorize, and/or finding a more efficient support.
        
        This should be reasonably fast for |Z| <= 2 or 3, and small enough discrete
        variable cardinalities.  It runs in O(n_1 n_2 ... n_k) in the cardinality of
        the discrete variables, |Z_1| = n_1, etc.  It likewise runs in O(V^n) for n
        continuous Z variables.  Factorizing the joint/conditional distributions in
        the sum could linearize the runtime.
        """
        pass
       
