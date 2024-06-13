import networkx as nx
import numpy as np
from _percolation import percolate_network


class Percolation: 
    
    def __init__(self, G, formated_label = False): 
        
        # The needed format for the network nodes name is ordered integers
        if formated_label :
            self.network = G
        else :
            self.network =  nx.convert_node_labels_to_integers(G)

        self.percolation_tree = None 

    def percolate(self):
        self.percolation_tree = percolate_network(self.network)

    