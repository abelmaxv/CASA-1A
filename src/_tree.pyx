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
        memb_tab : a membership table with cluster label in 0,...,k-1 and -1 if i does not belong to any

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
        if memb_tab_temp[i] != -1 : 
            size_tab[memb_tab_temp[i]] = size_tab[memb_tab_temp[i]]+1

    # Assigning cluster id
    for i in range(2*n_nodes-1):
        if size_tab[i] != 0:
            clusters_id[i] = next_label
            next_label+=1
    
    # Relabelling in membership_table
    for i in range(n_nodes):
        if memb_tab_temp[i] == -1 : 
            memb_tab[i] = -1
        else: 
            memb_tab[i] = clusters_id[memb_tab[i]]
    
    # Cleanning size_table 
    i = 0
    size_tab = size_tab[size_tab!=0]
    
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

        U.union(current_node, next_node)
        i+=1

    for i in range(n_nodes):
        memb_tab_temp[i] = U.fast_find(i)

    memb_tab, size_tab = clean_memb_tab(memb_tab_temp)

    return memb_tab, size_tab



cdef np.ndarray[dtype = long, ndim = 1] bfs_from_linkage_matrix(np.ndarray[dtype = double, ndim = 2] linkage_matrix, long node):
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
        long[:] to_process = np.empty(n_nodes+ linkage_matrix.shape[0], dtype = np.int_)
        long current_node
        long first_child
        long second_child
        # Pointers to make a queue out of to_process
        int start = 0
        int end = 1 
        np.ndarray[dtype = long, ndim = 1] result = np.empty(n_nodes + linkage_matrix.shape[0], dtype = np.int_)
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


cpdef list recurse_leaf_dfs(np.ndarray cluster_tree, np.intp_t current_node):
    #COPIED FROM HDBSCAN LIB
    children = cluster_tree[cluster_tree['parent'] == current_node]['child']
    if len(children) == 0:
        return [current_node,]
    else:
        return sum([recurse_leaf_dfs(cluster_tree, child) for child in children], [])
    



cpdef np.ndarray[dtype = cond_edge_t, ndim = 1] _condensed_tree (np.ndarray[dtype = double, ndim = 2] linkage_matrix, int min_cluster_size) :
    """ Implementing runt prunning procedure to create condensed_tree

    Parameters
    ----------
        linkage_matrix : np.ndarray that represents the linkage tree in the standard linkage matrix form of scipy.

        min_cluster_size : parameter for the min runt score of the runt procedure
    
    Returns 
    -------
         condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree

    The representation of condensed tree is a numpy array of edges with the form (p,c,l,s) with
        - p parent
        - c children
        - v lambda value 
        - s size of the child
    """
    cdef :
        long n_nodes = linkage_matrix.shape[0]+1
        long current_node
        long first_child
        long second_child
        long first_child_size
        long second_child_size
        long node
        long root
        double lamb_val
        double dist
        cond_edge_t cond_edge1
        cond_edge_t cond_edge2
        cond_edge_t cond_edge
        # Builds a tree of clusters, thus the size is nb_label -1 = n_nodes + len(likage_matrix) - 1 (at most)
        cond_edge_t[:] result = np.zeros(n_nodes + linkage_matrix.shape[0] -1, dtype = cond_edge_dtype)
        int edge_count = 0
        char[:] ignore = np.zeros(n_nodes+linkage_matrix.shape[0], dtype = np.int8)
        long[:] relabelling = np.zeros(n_nodes + linkage_matrix.shape[0], dtype = np.int_)
        long next_label = n_nodes

    # maximum cluster label is nb_label -1 = n_nodes + len(likage_matrix) - 1
    root = n_nodes + linkage_matrix.shape[0] - 1
    relabelling[root] = next_label
    next_label+=1


    # Important to treate clusters in the bfs order
    for current_node in bfs_from_linkage_matrix(linkage_matrix, root):

        if ignore[current_node] == 0 and current_node >= n_nodes: 

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
                second_child_size = <long> linkage_matrix[second_child-n_nodes,3]
            else : 
                second_child_size = 1
            
            # Checks is runt size of the edge is high enough
            # if so, add node to result (cluster spliting)
            if first_child_size >= min_cluster_size and second_child_size >= min_cluster_size : 
                relabelling[first_child] = next_label
                next_label+=1

                cond_edge1.parent = relabelling[current_node]
                cond_edge1.child = relabelling[first_child]
                cond_edge1.lamb_val = lamb_val
                cond_edge1.child_size = first_child_size

                result[edge_count] = cond_edge1
                edge_count +=1

                relabelling[second_child] = next_label
                next_label+=1

                cond_edge2.parent = relabelling[current_node]
                cond_edge2.child = relabelling[second_child]
                cond_edge2.lamb_val = lamb_val
                cond_edge2.child_size = second_child_size
                
                result[edge_count] = cond_edge2
                edge_count +=1
            
            # Handeling descendants when one children is too small
            # (cluster does not split)
            elif first_child_size >= min_cluster_size : 
                relabelling[first_child] = relabelling[current_node]
                for node in bfs_from_linkage_matrix(linkage_matrix, second_child) :
                    ignore[node] = 1
                    cond_edge.parent = relabelling[current_node]
                    cond_edge.child = node
                    cond_edge.lamb_val = lamb_val
                    cond_edge.child_size = 1

                    if node < n_nodes : 
                        result[edge_count] = cond_edge
                        edge_count +=1
            

            elif second_child_size >= min_cluster_size : 
                relabelling[second_child] = relabelling [current_node]
                for node in bfs_from_linkage_matrix(linkage_matrix, first_child) :
                    ignore[node] = 1
                    cond_edge.parent = relabelling[current_node]
                    cond_edge.child = node
                    cond_edge.lamb_val = lamb_val
                    cond_edge.child_size = 1

                    if node < n_nodes: 
                        result[edge_count] = cond_edge
                        edge_count +=1

            else : 
                for node in bfs_from_linkage_matrix(linkage_matrix, second_child) :
                    ignore[node] = 1
                    cond_edge.parent = relabelling[current_node]
                    cond_edge.child = node
                    cond_edge.lamb_val = lamb_val
                    cond_edge.child_size = 1

                    if node< n_nodes :
                        result[edge_count] = cond_edge
                        edge_count +=1

                for node in bfs_from_linkage_matrix(linkage_matrix, first_child) :
                    ignore[node] = 1
                    cond_edge.parent = relabelling[current_node]
                    cond_edge.child = node
                    cond_edge.lamb_val = lamb_val
                    cond_edge.child_size = 1


                    if node < n_nodes: 
                        result[edge_count] = cond_edge
                        edge_count +=1                            
            

    return np.asarray(result, dtype = cond_edge_dtype)[:edge_count]






cpdef np.ndarray[dtype = double, ndim = 1] _compute_stability(np.ndarray[dtype = cond_edge_t, ndim = 1] condensed_tree) : 
    """ Computes the stability score for all clusters in the cluster tree

    Parameters  
    ----------
        condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree

    Returns 
    -------
        clusters_stability : a np.ndarray that stores the stability score for all the clusters in the tree
    """ 
    cdef:
        long n_clusters = 2*condensed_tree[0].parent-1
        np.ndarray[dtype = double, ndim = 1] clusters_stability = np.zeros(n_clusters, dtype = np.double)
        cond_edge_t current_edge
        double[:] birth = np.zeros(n_clusters, dtype = np.double)
        long parent
        long child 
        double lamb_val 
        long child_size

    # Edges of the condensed_tree are given in bfs order
    for current_edge in condensed_tree : 
        parent = current_edge.parent
        child = current_edge.child
        lamb_val = current_edge.lamb_val
        child_size = current_edge.child_size

        if birth[child] == 0:
            birth[child] = lamb_val
        
        clusters_stability[parent] += (lamb_val - birth[parent])*child_size

    return clusters_stability




cdef char[:] select_clusters (np.ndarray[dtype = cond_edge_t, ndim = 1] condensed_tree, np.ndarray[dtype = double, ndim = 1] clusters_stability):
    """ Selects the relevent clusters given the stability array. Performs two searches in the cluster tree. 

    Paramters
    ---------
        condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree

        clusters_stability : a np.ndarray that stores the stability score for all the clusters in the tree
    
    Returns 
    -------
        is_selected : a np.ndarray that indicates wether cluster i is selected
    """

    cdef : 
        int n_clusters = 2*condensed_tree[0].parent-1
        double[:] relative_stability = np.zeros(n_clusters, dtype = np.double)
        double[:] score = np.zeros(n_clusters, dtype = np.double)
        char[:] is_selected = np.zeros(n_clusters, dtype = np.int8)
        char[:] ancestor_selected = np.zeros(n_clusters, dtype = np.int8)
        cond_edge_t cond_edge
        long child
        long parent
        long root = condensed_tree[0].parent

    # Computing score of each cluster and selection array bottom-up
    for cond_edge in condensed_tree[::-1] :
        child = cond_edge.child
        parent = cond_edge.parent

        relative_stability[parent] += score[child]
        score[parent] = max(relative_stability[parent], clusters_stability[parent])

        if relative_stability[parent]>=clusters_stability[parent]:
            is_selected[parent] = 0
        else : 
            is_selected[parent] = 1

    # Clean the selection array top-to-bottom
    # Do not select the root which is irrelevant
    is_selected[root] = 0
    for cond_edge in condensed_tree : 
        
        child = cond_edge.child
        parent = cond_edge.parent

        if ancestor_selected[parent] == 1:
            ancestor_selected[child] = 1
            is_selected[child] = 0
            is_selected[parent] = 0

        elif is_selected[parent] == 1:
            ancestor_selected[child] = 1
            is_selected[child] = 0
    return is_selected
    
    
 
cdef np.ndarray[dtype = long, ndim = 1] label_of_stability_temp(np.ndarray[dtype = cond_edge_t, ndim = 1] condensed_tree, char[:] is_selected):
    """ Commputes a temporary membership table from the condensed tree and the cluster slection.

    Parmeters
    ---------
        condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree

        is_selected : a np.ndarray that indicates wether cluster i is selected
    
    Returns
    -------
        memb_tab_temp : np.ndarray of long integers that represents a temporary membership table
    
    Here temporary means that clusters label are not {0,..., k-1} integers
    """
    cdef : 
        long n_clusters = 2*condensed_tree[0].parent-1
        # Numper of nodes is the label of the root
        long n_nodes = condensed_tree[0].parent
        np.ndarray[dtype = long, ndim = 1] memb_tab_temp = (-1) * np.ones(n_clusters, dtype = long)
        cond_edge_t cond_edge
        long parent
        long child

    for cond_edge in condensed_tree:
        parent = cond_edge.parent
        child = cond_edge.child

        if is_selected[parent]==1: 
            memb_tab_temp[parent] = parent
        
        memb_tab_temp[child] = memb_tab_temp[parent]
    memb_tab_temp = memb_tab_temp[:n_nodes]
    return memb_tab_temp




cpdef tuple _label_of_stability(np.ndarray[dtype = cond_edge_t, ndim = 1] condensed_tree, np.ndarray[dtype = double, ndim = 1] clusters_stability):
    """ TO DO 
    """
    cdef : 
        char[:] is_selected = select_clusters(condensed_tree, clusters_stability)
        long[:] memb_tab_temp = label_of_stability_temp(condensed_tree, is_selected)
        np.ndarray[dtype=long, ndim = 1] memb_tab
        np.ndarray[dtype = int, ndim =1] size_tab

    memb_tab, size_tab = clean_memb_tab(memb_tab_temp)

    return memb_tab, size_tab


cpdef np.ndarray[dtype = long, ndim = 1] _get_selected_clusters(np.ndarray[dtype = cond_edge_t, ndim = 1] condensed_tree, np.ndarray[dtype = double, ndim = 1] clusters_stability):
    """ TO DO
    """
    cdef : 
        char[:] is_selected = select_clusters(condensed_tree, clusters_stability)
        long[:] memb_tab_temp = label_of_stability_temp(condensed_tree, is_selected)
        int n_clusters = 2*condensed_tree[0].parent -1
        int[:] size = np.zeros(n_clusters, dtype = np.intc)
        int cluster_count = 0
        np.ndarray[dtype = long, ndim = 1] cluster_list = np.empty(n_clusters, dtype = np.int_)
        int i


    # Look for non empty clusters
    for i in range(len(memb_tab_temp)):
        if memb_tab_temp[i] != -1:
            size[memb_tab_temp[i]]+=1

    # List the non empty clusters
    for i in range(len(size)):
        if size[i]>0:
            cluster_list[cluster_count] = i
            cluster_count+=1
    return cluster_list[:cluster_count]
    
    
    
        

