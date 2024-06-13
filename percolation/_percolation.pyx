
cdef _tree.HIERARCHY_t[:] percolation_on_graph(_graph.edge_t[:] graph):

    cdef : 
        int n_samples = graph.shape[0] + 1
        _tree.HIERARCHY_t[:] hierarchical_tree = np.zeros(n_samples, dtype=_tree.HIERARCHY_dtype)
        int current_node_cluster, next_node_cluster
        int current_node, next_node, i
        float distance
        UnionFind U = UnionFind(n_samples)
        

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



