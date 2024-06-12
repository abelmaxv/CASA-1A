import numpy as np
cimport numpy as cnp
import networkx as nx


edge_dtype = np.dtype([
    ("first_node", np.int64),
    ("second_node", np.int64),
    ("distance", np.float64)
]) 

cdef edge_t[:] transform_graph(G):

    cdef int size = G.number_of_edges()
    cdef edge_t[:] edge_array = np.zeros(size, dtype=edge_dtype)
    
    cdef int i = 0
    for u, v, data in G.edges(data=True):
        edge_array[i].first_node = u
        edge_array[i].second_node = v
        edge_array[i].distance = data["length"]
    return edge_array





