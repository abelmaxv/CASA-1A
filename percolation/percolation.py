# The structure of the code as well as the objects are inspired from HDBSCAN implementation in skitlearn


import networkx as nx


def percolation(G):
    """ Computes the percolation tree
    
    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    percolation tree

    """

    