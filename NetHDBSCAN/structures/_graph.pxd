import numpy as np
cimport numpy as np

ctypedef packed struct edge_t :
    long first_node
    long second_node
    float distance
    
cdef edge_t[::1] transform_graph_pd(G, str length_attribute)
cdef edge_t[::1] transform_graph_nx(G, str length_attribute)