cimport numpy as np

from _union_find cimport UnionFind
from _graph cimport edge_t


cdef np.ndarray[dtype = double, ndim=2] clean_linkage_matrix(np.ndarray[dtype = double, ndim=2] linkage_matrix)
cdef np.ndarray[ndim=2, dtype = double] percolate_edge_list(edge_t[::1] edge_list, int n_nodes)
cpdef np.ndarray[dtype = double, ndim=2] percolate_network(G, char clean)