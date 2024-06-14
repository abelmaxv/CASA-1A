import networkx as nx
import numpy as np
from _percolation import percolate_network
from linkage_tree import LinkageTree


class Percolation: 
    
    def __init__(self, G, formated_label = False, compute_mst = False): 
        
        # The needed format for the network nodes name is ordered integers
        # May find something better than storing the whole graph ?
        if formated_label :
            self.network = G
        else :
            self.network =  nx.convert_node_labels_to_integers(G)
        
        self._linkage_tree = None 
        self.compute_mst = False

    def percolate(self):
        # If the MST is computed it is not necessary to clean the single linkage_matrix
        self._linkage_tree = percolate_network(self.network, not(self.compute_mst))

    @property 
    def linkage_tree(self):
        if self._linkage_tree is None : 
            raise AttributeError("No percolation tree generated")
        else : 
            return LinkageTree(self._linkage_tree)

    