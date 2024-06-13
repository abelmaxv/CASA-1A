import numpy as np
cimport numpy as np


edge_dtype = np.dtype([
    ("first_node", np.int_),
    ("second_node", np.int_),
    ("distance", np.single)
]) 

cdef edge_t[:] transform_graph(G):
    """ Transforms a Networkx multidigraph provided by osmnx into 
    an edge_t 
    """
    cdef int number_of_edges = G.number_of_edges()
    cdef edge_t[:] edge_array = np.zeros(number_of_edges, dtype=edge_dtype)
    cdef int i = 0

    for u, v, data in G.edges(data=True):
        edge_array[i].first_node = u
        edge_array[i].second_node = v
        edge_array[i].distance = data["length"]
        i+=1 

    return edge_array




