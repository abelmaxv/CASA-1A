import numpy as np
cimport numpy as np

from ._union_find import UnionFind
from ._union_find cimport UnionFind




cpdef np.ndarray[dtype = long, ndim = 1] _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold): 
    """ Extracts the cluster from the linkage tree at a given threshold.
        Computes percolation until threshold is reached.
    """
    cdef : 
        # Percolation defines a spanning tree so n_nodes = n_edges+1
        int n_nodes = linkage_matrix.shape[0]+1
        long current_node_cluster, next_node_cluster
        long current_node, next_node
        int i = 0
        double distance
        UnionFind U = UnionFind(n_nodes)
        np.ndarray[dtype = long, ndim = 1] result = np.zeros(n_nodes, dtype = long) 
        

    while threshold > linkage_matrix[i,2] and i < linkage_matrix.shape[0]  :
        current_node = <long> linkage_matrix[i,0]
        next_node = <long> linkage_matrix[i,1]
        distance = linkage_matrix[i,2]

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        U.union(current_node_cluster, next_node_cluster)
        i+=1

    for i in range(n_nodes):
        result[i] = U.fast_find(i)

    return result
