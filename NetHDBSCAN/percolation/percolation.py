import networkx as nx
import numpy as np
import pandas as pd
from ._percolation import percolate_network
from NetHDBSCAN.structures._tree import _condensed_tree
from NetHDBSCAN.structures.linkage_tree import LinkageTree
from NetHDBSCAN.structures.condensed_tree import CondensedTree

def _checks_format_nx(G):
    """ Checks if the graph given as the right format for the library : 
    - The paramenter is a networkx undirected object 
    - Nodes are labeled with integers 0, ..., n-1
    """
    if not (isinstance(G, nx.MultiGraph)) and not(isinstance(G, nx.Graph)):
        raise AttributeError("Wrong datatype. Undirected networkx graph was specified.")
    
    size = G.number_of_nodes()
    for n in G.nodes():
        if not(0 <= n < size):
            raise AttributeError("Nodes must be labeled with ordered integers. Add G = nx.convert_node_labels_to_integers(G) to the script.")


def _checks_format_pd(G):
    """ Checks if the graph given as the right format for the library : 
    - The paramenter is a panda data frame to list edges 
    - The columns of the data frame are named "source", "target" 

    WARNING : this function does not check if nodes are labeled with integers 0,..., n-1
    but the user has to make sure it is
    """
    if not (isinstance(G, pd.DataFrame)):
        raise AttributeError("Wrong datatype. Undirected  pandas DataFrame edge list was specified.")
    elif G.columns[0] != "source" or G.columns[1] != "target":
        raise AttributeError("The two first columns of the DataFrame must be source and taget.")


    

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
        """ 
        .. :no-docs:
        """
        if self._linkage_tree is None : 
            raise AttributeError("No percolation tree generated. Run self.percolate().")
        else : 
            return LinkageTree(self._linkage_tree)

    @property    
    def condensed_tree(self):
        """
        .. :no-docs:
        """
        if self._condensed_tree is None: 
            raise AttributeError("No condensed tree generated. Run self.compute.condensed_tree().")
        else: 
            return CondensedTree(self._condensed_tree)
        

    def percolate(self, G, length_attribute = "length", data_type = "networkx"):
        """ Computes the percolation algorithm on the a given network output by a osmnx querry.
    
        Parameters  
        ----------
            G : a networkx graph or an Pandas Data frame of edges (source, target, length)

            length_attribute : name of the weights on edges. By default, for a osmnx network this is 'legnth'

            data_type : data type for the G. "networkx" by defalt, "pandas" otherwise
        
        Returns
        -------
            self 
        
        """
        if data_type == "networkx":
            _checks_format_nx(G)
        elif data_type == "pandas":
            _checks_format_pd(G)
        else : 
            raise AttributeError("Wrong data type specified for the graph.")
        self._linkage_tree = percolate_network(G, length_attribute, data_type)
        return self


    def compute_condensed_tree(self, min_size = 10):
        """ Computes the condensed tree with the runt prunning method

        Parameters
        ----------
            min_size : parameter of the runt prunning method that corresponds the the minimum cluster size in 
            the condensed tree
        
        Returns
        ------
            self 
        """
        if self._linkage_tree is None : 
            raise ValueError("Need to compute the linkage tree before extracting pruning tree. Run self.percolate().") 
        
        self._condensed_tree = _condensed_tree(self._linkage_tree, min_size)
        return self