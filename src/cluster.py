import numpy as np
import networkx as nx


class Cluster(object):

    def __init__(self, tab):
        # tab is a numpy array that contains the cluster name of each node
        self.tab = tab
    
    def clusters_to_dict(self):
        clusters_dict = {}
        for i in range(self.tab.shape[0]):
            clusters_dict[i] = self.tab[i]
        return clusters_dict
    
    def add_clusters_to_graph(self, G):
        clusters_dict = self.clusters_to_dict()
        nx.set_node_attributes(G, clusters_dict, 'cluster')
