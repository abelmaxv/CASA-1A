import numpy as np
cimport numpy as np
from ._union_find cimport UnionFind

ctypedef packed struct cond_edge_t :
    long parent
    long child
    double lamb_val
    long child_size


cdef tuple clean_memb_tab(long[:] memb_tab_temp)
cpdef tuple _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold)

cdef np.ndarray[dtype = long, ndim = 1] bfs_from_linkage_matrix(np.ndarray[dtype = double, ndim = 2] linkage_matrix, long node)
cpdef np.ndarray[dtype = cond_edge_t, ndim = 1] _condensed_tree (np.ndarray[dtype = double, ndim = 2] linkage_matrix, int min_cluster_size) 


#COPIED FROM HDBSCAN LIB
cpdef list recurse_leaf_dfs(np.ndarray cluster_tree, np.intp_t current_node)
