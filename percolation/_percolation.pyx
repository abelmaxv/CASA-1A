import numpy as np
cimport numpy as np

from _union_find cimport UnionFind
from _tree cimport HIERARCHY_t
from _tree import HIERARCHY_dtype
from _graph cimport edge_t, transform_graph
from _graph import edge_dtype

cdef HIERARCHY_t[:] percolate_edge_list(edge_t[::1] edge_list, int n_nodes):
    """ Computes the percolation algorithm on the edge list of a given graph
    """
    cdef : 
        int n_samples = len(edge_list)
        HIERARCHY_t[:] hierarchical_tree = np.zeros(n_samples, dtype=HIERARCHY_dtype)
        long current_node_cluster, next_node_cluster
        long current_node, next_node 
        int i
        float distance
        UnionFind U = UnionFind(n_nodes)


    for i in range(n_samples):
        current_node = edge_list[i].first_node
        next_node = edge_list[i].second_node
        distance = edge_list[i].distance

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        hierarchical_tree[i].left_node = current_node_cluster
        hierarchical_tree[i].right_node = next_node_cluster
        hierarchical_tree[i].value = distance
        hierarchical_tree[i].cluster_size = U.size(current_node_cluster) + U.size(next_node_cluster)

        U.union(current_node_cluster, next_node_cluster)

    return hierarchical_tree




cpdef np.ndarray[HIERARCHY_t, ndim=1] percolate_network(G):
    
    cdef int number_of_nodes = G.number_of_nodes()
    cdef edge_t[::1] edge_list = transform_graph(G)


    np_edge_list = np.asarray(edge_list, dtype = edge_dtype)
    np_edge_list = np.sort(np_edge_list, order=('distance', 'first_node', 'second_node'))
    edge_list = np_edge_list

    cdef HIERARCHY_t[:] percolation_tree = percolate_edge_list(edge_list, number_of_nodes)
    return np.asarray(percolation_tree, dtype = HIERARCHY_dtype)