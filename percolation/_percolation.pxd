cimport numpy as np

from _union_find cimport UnionFind
from _tree cimport HIERARCHY_t
from _graph cimport edge_t


cdef HIERARCHY_t[:] percolate_edge_list(edge_t[::1] edge_list, int n_nodes)
cpdef np.ndarray[HIERARCHY_t, ndim=1] percolate_network(G)