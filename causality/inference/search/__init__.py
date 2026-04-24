import networkx as nx
import itertools

"""
This is an implementation of the IC* (Inductive Causation with latent
variables) algorithm as described in _Causality_ by Judea Pearl, 2000.
"""

try:
    xrange
except NameError:
    xrange = range

class SearchException(Exception):
    pass

class IC():
    def __init__(self, independence_test, alpha=0.05, k=None):
        self.independence_test = independence_test
        self.alpha = alpha
        self.separating_sets = None
        self._g = None
        self.max_k = k

    def search(self, data, variable_types):
        pass

    def _build_g(self, variable_types):
        """
        This initializes a complete graph over the variables.  We'll run
        independence tests on the complete graph to cut edges by trying to
        find separating sets.
        """
        pass

    def _apply_recursion_rule_1(self):
        pass

    def _apply_recursion_rule_2(self):
        pass

    def _marked_directed_path(self,a,b):
        pass


    def _orient_colliders(self):
        pass

    def separating_set(self, xi, xj, data=None, variable_types=None):
        pass

    def _find_skeleton(self, data, variable_types):
        """
        For each pair of nodes, run a conditional independence test over
        larger and larger conditioning sets to try to find a set that
        d-separates the pair.  If such a set exists, cut the edge between
        the nodes.  If not, keep the edge.
        """
        pass
