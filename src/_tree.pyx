import numpy as np
cimport numpy as np

from ._union_find import UnionFind
from ._union_find cimport UnionFind


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
