import numpy as np
cimport numpy as np

from ._union_find import UnionFind
from ._union_find cimport UnionFind

cdef np.double_t INFTY = np.inf

cond_edge_dtype = np.dtype([
    ("parent", np.int_),
    ("child", np.int_),
    ("lamb_val", np.double),
    ("child_size", np.int_)
]) 


cdef tuple clean_memb_tab(long[:] memb_tab_temp):
    """ Takes a temporary membership table (labels are not 0,...,k-1) and returns a size table and a correct membership table

    Parameters
    ----------
        memb_tab_temp : Memoryview of long integers that represents a temporary membership tables
    
    Returns
    -------
        memb_tab : a membership table with cluster label in 0,...,k-1

        size_tab : np.ndarray of cluster sizes. size_tab[i] contains the size of the cluter which id is i 
    """
    cdef : 
        int n_nodes = len(memb_tab_temp)
        long next_label = 0
        long[:] clusters_id = np.zeros(2*n_nodes-1, dtype = np.int_)
        np.ndarray[dtype = int, ndim =1] size_tab = np.zeros(2*n_nodes, dtype = np.intc)
        np.ndarray[dtype = long, ndim = 1] memb_tab = np.asarray(memb_tab_temp, dtype = np.int_)
        int i = 0
    
    # Computing size table
    for i in range(n_nodes): 
        size_tab[memb_tab_temp[i]] = size_tab[memb_tab_temp[i]]+1

    # Assigning cluster id
    for i in range(2*n_nodes-1):
        if size_tab[i] != 0:
            clusters_id[i] = next_label
            next_label+=1
    
    # Relabelling in membership_table
    for i in range(n_nodes):
        memb_tab[i] = clusters_id[memb_tab[i]]
    
    # Cleanning size_table 
    i = 0
    while i < size_tab.shape[0] :
        if size_tab[i] == 0 : 
            size_tab = np.delete(size_tab, i, axis = 0)
        else :
            i+=1
    
    return memb_tab, size_tab




cpdef tuple _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold): 
    """ Extract clusters at a given threshold in the linkage tree

    Parameters
    ----------
        linkage_matrix : np.ndarray that represents the linkage tree in the standard linkage matrix form of scipy

        threshold : threshold at which the linkage tree is cut
    
    Returns
    -------
        memb_tab : the membership table as a np.ndarray.

        size_tab :  np.ndarray of cluster sizes. size_tab[i] contains the size of the cluter which id is i 


    The membership table is an array A such that A[i] contains the cluster label of node i. Labels of clusters are 
    0,...,k-1
    """
    cdef : 
        # Percolation defines a spanning tree so n_nodes = n_edges+1
        int n_nodes = linkage_matrix.shape[0]+1
        long current_node_cluster, next_node_cluster
        long current_node, next_node
        int i = 0
        double distance
        UnionFind U = UnionFind(n_nodes)
        long[:] memb_tab_temp = np.zeros(n_nodes, dtype = long) 
        np.ndarray[dtype = long, ndim = 1] memb_tab 
        np.ndarray[dtype = int, ndim = 1] size_tab 
        
    # Computes the percolation until the thershold is reached
    while threshold >= linkage_matrix[i,2] and i < linkage_matrix.shape[0]  :
        current_node = <long> linkage_matrix[i,0]
        next_node = <long> linkage_matrix[i,1]
        distance = linkage_matrix[i,2]

        current_node_cluster = U.fast_find(current_node)
        next_node_cluster = U.fast_find(next_node)

        U.union(current_node_cluster, next_node_cluster)
        i+=1

    for i in range(n_nodes):
        memb_tab_temp[i] = U.fast_find(i)

    memb_tab, size_tab = clean_memb_tab(memb_tab_temp)

    return memb_tab, size_tab



cdef np.ndarray[dtype = long, ndim = 1] bfs_from_linkage_matrix(np.ndarray[dtype = double, ndim = 1] linkage_matrix, long node):
    """ Performs a breadth first tree search of the linkage tree from some given node

    Parameters
    ----------
        linkage_matrix : np.ndarray that represents the linkage tree in the standard linkage matrix form of scipy

        node : a long itegers that specifies where to start the bfs in the tree

    Returns 
    -------
        result : a np.ndarray that contains the nodes encountered during the bfs
    """
    cdef : 
        int n_nodes = linkage_matrix.shape[0]+1
        long[:] to_process = np.zeros(n_nodes, dtype = np.intc)
        long current_node
        long first_child
        long second_child
        # Pointers to make a queue out of to_process
        int start = 0
        int end = 1 
        np.ndarray[dtype = long, ndim = 1] result = np.zeros(n_nodes, dtype = np.int_)
        # To trucate the result array at the end
        int nb_results = 0

    # initialise to_process
    to_process[0] = node
    
    # BFS
    while start < end : 
        current_node = to_process[start]
        start +=1
        result[nb_results] = current_node
        nb_results +=1

        # Notice that if current_node >= n_nodes, the children are 
        # linkage_matrix[current_node - n_nodes, 0] and linkage_matrix[current_node - n_nodes, 1]
        if current_node >= n_nodes : 
            first_child = <long>  linkage_matrix[current_node - n_nodes, 0]
            second_child =  <long>  linkage_matrix[current_node - n_nodes, 1]

            to_process[end] = first_child
            to_process[end+1] = second_child
            end+=2
    
    return result[:nb_results]


cpdef np.ndarray[dtype = cond_edge_t, ndim = 1] _condensed_tree (np.ndarray[dtype = double, ndim = 2] linkage_matrix, int min_cluster_size) :
    """ Implementing runt prunning
    """
    cdef :
        long n_nodes = linkage_matrix.shape[0]+1
        long current_node
        long first_child
        long second_child
        long first_child_size
        long second_child_size
        double lamb_val
        double dist
        cond_edge_t cond_edge1
        cond_edge_t cond_edge2
        cond_edge_t[:] result = np.zeros(n_nodes-1, dtype = cond_edge_dtype)
        int edge_count = 0
        np.ndarray[dtype = char, ndim = 1] ingnore = np.zeros(n_nodes, dtype = np.int8)

    # maximum cluster label is nb_label -1 = n_nodes + len(likage_matrix) - 1
    current_node = n_nodes + linkage_matrix.shape[0] - 1

    while current_node >= n_nodes:

        if ignore[current_node] == 0: 

            # Setting the variables
            first_child =  <long>linkage_matrix[current_node-n_nodes, 0]
            second_child = <long> linkage_matrix[current_node - n_nodes, 1]

            dist = linkage_matrix[current_node-n_nodes, 2]
            if dist>0.0:
                lamb_val = 1/dist
            else: 
                lamb_val = INFTY
                
            if first_child >= n_nodes : 
                first_child_size = <long> linkage_matrix[first_child-n_nodes,3]
            else : 
                first_child_size = 1

            if second_child >= n_nodes : 
                second_child_size = <long> linkage_matrix[first_child-n_nodes,3]
            else : 
                second_child_size = 1
            
            # Checks is runt size of the edge is high enough
            # if so, add node to result
            if first_child_size >= min_cluster_size and second_child_size >= min_cluster_size : 
                cond_edge1.parent = current_node
                cond_edge1.child = first_child
                cond_edge1.lamb_val = lamb_val
                cond_edge1.child_size = first_child_size
                
                result[edge_count] = cond_edge1
                edge_count +=1

                cond_edge2.parent = current_node
                cond_edge2.child = second_child
                cond_edge2.lamb_val = lamb_val
                cond_edge2.child_size = second_child_size

                result[edge_count] = cond_edge2
                edge_count +=1
            
            elif 

        current_node = current_node -1


    return np.asarray(result, dtype = cond_edge_dtype)[:edge_count]


cpdef list recurse_leaf_dfs(np.ndarray cluster_tree, np.intp_t current_node):
    #COPIED FROM HDBSCAN LIB
    children = cluster_tree[cluster_tree['parent'] == current_node]['child']
    if len(children) == 0:
        return [current_node,]
    else:
        return sum([recurse_leaf_dfs(cluster_tree, child) for child in children], [])