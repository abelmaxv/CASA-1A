import numpy as np
cimport numpy as np


edge_dtype = np.dtype([
    ("first_node", np.int_),
    ("second_node", np.int_),
    ("distance", np.single)
]) 

cdef edge_t[::1] transform_graph(G, str length_attribute):
    """ Transforms a networkx.MultiDiGraph in a MemoryView of edge_t that
    represents the same graph.

    Parameters
    ----------
        G : a networkx MultiDiGraph

        length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'.
    """

    cdef int number_of_edges = G.number_of_edges()
    cdef edge_t[::1] edge_array = np.zeros(number_of_edges, dtype=edge_dtype)
    cdef int i = 0

    for u, v, data in G.edges(data=True):
        edge_array[i].first_node = u
        edge_array[i].second_node = v
        edge_array[i].distance = data[length_attribute]
        i+=1 

    return edge_array




