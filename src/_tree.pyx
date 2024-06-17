import numpy as np
cimport numpy as np

from ._union_find import UnionFind
from ._union_find cimport UnionFind




cpdef np.ndarray[dtype = long, ndim = 1] _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold): 
    """ Extract clusters at a given threshold in the linkage tree

    Parameters
    ----------
        linkage_matrix : np.ndarray that represents the linkage tree in the standard linkage matrix form of scipy

        threshold : threshold at which the linkage tree is cut
    
    Returns
    -------
        memb_tab : the membership table as a np.ndarray. 


    The membership table is an array A such that A[i] contains the cluster label of node i.
    """
    cdef : 
        # Percolation defines a spanning tree so n_nodes = n_edges+1
        int n_nodes = linkage_matrix.shape[0]+1
        long current_node_cluster, next_node_cluster
        long current_node, next_node
        int i = 0
        double distance
        UnionFind U = UnionFind(n_nodes)
        np.ndarray[dtype = long, ndim = 1] memb_tab = np.zeros(n_nodes, dtype = long) 
        
    # Computes the percolation until the thershold is reached
    while threshold > linkage_matrix[i,2] and i < linkage_matrix.shape[0]  :
        current_node = <long> linkage_matrix[i,0]
        next_node = <long> linkage_matrix[i,1]
        distance = linkage_matrix[i,2]

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        U.union(current_node_cluster, next_node_cluster)
        i+=1

    for i in range(n_nodes):
        memb_tab[i] = U.fast_find(i)

    return memb_tab
