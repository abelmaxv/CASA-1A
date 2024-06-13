cdef np.ndarray[HIERARCHY_t, ndim=1, mode="c"] percolation_on_graph(edge_t[:] graph):
    """ Computes the percolation tree
    
    Parameters
    ----------
    graph : ndarray of shape (n_samples -1), dtype= edge_dtype
            The representation of a graph is a collection of 
            edges.

    Returns
    -------
    hierarchical_tree : nd array of shape (n_samples - 1 ), dtype = HIERARCHY_dtype

    """
    cdef : 
        cnp.ndarray[HIERARCHY_t, ndim=1, mode="c"] hierarchical_tree
        int n_samples = graph.shape[0] + 1
        int current_node_cluster, next_node_cluster
        int current_node, next_node, i
        float distance
        UnionFind U = UnionFind(n_samples)


    hierarchical_tree = np.zeros(n_samples-1, dtype=HIERARCHY_dtype)

    for i in range(n_samples - 1):

        current_node = graph[i].first_node
        next_node = graph[i].second_node
        distance = graph[i].distance

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        hierarchical_tree[i].left_node = current_node_cluster
        hierarchical_tree[i].right_node = next_node_cluster
        hierarchical_tree[i].value = distance
        hierarchical_tree[i].cluster_size = U.size[current_node_cluster] + U.size[next_node_cluster]

        U.union(current_node_cluster, next_node_cluster)

    return hierarchical_tree



