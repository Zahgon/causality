from networkx.algorithms import is_directed_acyclic_graph

class AdjustmentException(Exception):
    pass

class AdjustForDirectCauses(object):
    def __init__(self): 
        pass

    def find_predecessors(self, g, causes):
        pass

    def assumptions_satisfied(self, g, causes, effects, predecessors):
        pass

    def admissable_set(self, g, causes, effects):
        pass
