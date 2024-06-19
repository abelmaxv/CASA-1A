class CondensedTree(object):
    """ Implementation of the result of the runt pruning on a linkage tree

    Attributes
    ----------
        condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree

    The representation of condensed tree is a numpy array of edges with the form (p,c,l,s) with
        - p parent
        - c children
        - v lambda value 
        - s size of the child
    """

    def __init__(self, array_rep):
        self.array_rep = array_rep
