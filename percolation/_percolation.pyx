import numpy as np
cimport numpy as np

from _union_find cimport UnionFind
from _graph cimport edge_t, transform_graph
from _graph import edge_dtype

cdef  np.ndarray[ndim = 2, dtype = double] percolate_edge_list(edge_t[::1] edge_list, int n_nodes):
    """ Computes the percolation algorithm on the edge list of a given graph
    """
    cdef : 
        int n_samples = len(edge_list)
        long current_node_cluster, next_node_cluster
        long current_node, next_node 
        int i
        double distance
        UnionFind U = UnionFind(n_nodes)
        np.ndarray[ndim = 2, dtype = double] linkage_matrix = np.zeros((n_samples,4), dtype = np.double)

    for i in range(n_samples):

        current_node = edge_list[i].first_node
        next_node = edge_list[i].second_node
        distance = edge_list[i].distance

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)
        
        # Standard representation of the linkage tree
        linkage_matrix[i,0] = current_node_cluster
        linkage_matrix[i,1] = next_node_cluster
        linkage_matrix[i,2] = distance
        linkage_matrix[i,3] = U.size_arr[current_node_cluster] + U.size_arr[next_node_cluster]

        U.union(current_node_cluster, next_node_cluster)

    return linkage_matrix




cdef np.ndarray[dtype = double, ndim=2] clean_linkage_matrix(np.ndarray[dtype = double, ndim=2] linkage_matrix):
    """ Removes redundant rows in the linkage_matrix.
    """
    cdef int i = 0
    while i < linkage_matrix.shape[0]:
        if linkage_matrix[i, 0] == linkage_matrix[i,1]:
            linkage_matrix = np.delete(linkage_matrix, i, axis= 0)
        else: 
            i+=1
    return linkage_matrix



cpdef np.ndarray[dtype = double, ndim=2] percolate_network(G, char clean):
    
    cdef int number_of_nodes = G.number_of_nodes()
    cdef edge_t[::1] edge_list = transform_graph(G)


    np_edge_list = np.asarray(edge_list, dtype = edge_dtype)
    np_edge_list = np.sort(np_edge_list, order=('distance', 'first_node', 'second_node'))
    edge_list = np_edge_list

    cdef np.ndarray[ndim= 2, dtype = double] linkage_matrix = percolate_edge_list(edge_list, number_of_nodes)
    
    #If a MST was computed, this is not necessary to clean the linkage_matrix
    if clean: 
        linkage_matrix = clean_linkage_matrix(linkage_matrix)

    return linkage_matrix