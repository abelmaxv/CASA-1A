import numpy as np
cimport numpy as np

ctypedef packed struct edge_t :
    long first_node
    long second_node
    float distance
    

cdef edge_t[:] transform_graph(G)