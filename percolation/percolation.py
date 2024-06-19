import networkx as nx
import numpy as np
from ._percolation import percolate_network
from src._tree import _condensed_tree
from src.linkage_tree import LinkageTree
from src.condensed_tree import CondensedTree

def _checks_format(G):
    """ Checks if the graph given as the right format for the library : 
    - The paramenter is a nx.MultiDiGraph object 
    - Nodes are labeled with integers 0, ..., n-1
    """
    if not (isinstance(G, nx.MultiDiGraph)):
        raise AttributeError("Wrong datatype. Percolation must operate on a networkx.MultiDiGraph object")
    
    size = G.number_of_nodes()
    for n in G.nodes():
        if not(0 <= n < size):
            raise AttributeError("Nodes must be labeled with ordered integers. Add G = nx.convert_node_labels_to_integers(G) to the script.")



class Percolation: 
    """ This is a class to implement the percolation algorithm. 

    Atributes 
    ---------
        linkage_tree : the result of the percolation computed on a network 
        as a linkage matrix ; None is no percolation computed

        condensed_tree : np.ndarray that respresents the result of the runt pruning procedure on the linkage tree
    
    A linkage matrix is a np.ndarray A with 4 columns : 
        - A[i,0] and A[i,1] are the names of the merged clusters at step i
        - A[i,2] contains the length of the link that merged the two clusters
        - A[i,3] contains the size of the new cluster

    The representation of condensed tree is a numpy array of edges with the form (p,c,l,s) with
        - p parent
        - c children
        - v lambda value 
        - s size of the child
    """
    
    def __init__(self): 
        self._linkage_tree = None 
        self._condensed_tree = None


    @property 
    def linkage_tree(self):
        if self._linkage_tree is None : 
            raise AttributeError("No percolation tree generated. Run self.percolate().")
        else : 
            return LinkageTree(self._linkage_tree)

    @property    
    def condensed_tree(self):
        if self._condensed_tree is None: 
            raise AttributeError("No condensed tree generated. Run self.compute.condensed_tree().")
        else: 
            return CondensedTree(self._condensed_tree)
        

    def percolate(self, G, length_attribute = "length"):
        """ Computes the percolation algorithm on the a given network output by a osmnx querry.
    
        Parameters  
        ----------
            G : a networkx MultiDiGraph

            length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'
        
        Returns
        -------
            self : the linkage tree is stored as a linkage matrix in the _linkage_tree attribute
        
        A linkage matrix is a np.ndarray A with 4 columns : 
        - A[i,0] and A[i,1] are the names of the merged clusters at step i
        - A[i,2] contains the length of the link that merged the two clusters
        - A[i,3] contains the size of the new cluster

        """
        _checks_format(G)
        self._linkage_tree = percolate_network(G, length_attribute)
        return self


    def compute_condensed_tree(self, min_size = 10):
        """ 
        """
        if self._linkage_tree is None : 
            raise ValueError("Need to compute the linkage tree before extracting pruning tree. Run self.percolate().") 
        
        self._condensed_tree = _condensed_tree(self._linkage_tree, min_size)
        return self