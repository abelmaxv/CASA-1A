import numpy as np
cimport numpy as cnp

import networkx as nx

# Numpy structured dtype representing an edge of a graph
# A graph is represented as an ordered list of edges
edge_dtype = np.dtype([
    ("first_node", np.int64),
    ("second_node", np.int64),
    ("distance", np.float64)
]) 

cpdef cnp.ndarray[edge_t, ndim= 1; mode='c'] networkx_to_list()
