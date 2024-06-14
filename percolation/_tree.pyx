import numpy as np
cimport numpy as np

from _union_find import UnionFind
from _union_find cimport UnionFind




# To improve !
def extract_from_union_find(UnionFind U, int n_nodes):
    """ Gets the union_find table of a clustering and returns the list list of clusters.
    """
    clusters = []
    for i in range(2*n_nodes):
        clusters.append([])
    for i in range(n_nodes):
        clusters[U.fast_find(i)].append(i)
    return [l for l in clusters if l != []]




cpdef _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold): 
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
        

    while threshold > linkage_matrix[i,2] and i < linkage_matrix.shape[0]  :
        current_node = <long> linkage_matrix[i,0]
        next_node = <long> linkage_matrix[i,1]
        distance = linkage_matrix[i,2]

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        U.union(current_node_cluster, next_node_cluster)
        i+=1

    clusters = extract_from_union_find(U, n_nodes)

    return clusters
