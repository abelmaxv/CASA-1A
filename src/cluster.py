import numpy as np
import networkx as nx

def _check_format(G, size_tab):
    """ Check if the cluster labelling can be applied on a graph : 
    - G must a nx.MultiDiGrpah
    - Nodes must be labelled with integer 0,...,n-1
    - n must be lower than self.mem_arr.shape[0]
    """
    if not (isinstance(G, nx.MultiDiGraph)):
        raise AttributeError("Wrong datatype. Clustering must operate on a networkx.MultiDiGraph object")
    
    size = G.number_of_nodes()
    for n in G.nodes():
        if not(0 <= n < size):
            raise AttributeError("Nodes must be labeled with ordered integers. Add G = nx.convert_node_labels_to_integers(G) to the script.")
        if size_tab <= n:
            raise AttributeError("Can not apply clustering to the graph because id is to high")




class Clustering(object):
    """ Class to represent one clustering of a graph

    Attributes
    ----------
        mem_tab : membership table of the clustering

        size_tab : stores the size of each cluster of the clustering
    """

    def __init__(self, mem_tab):
        self.mem_tab = mem_tab
        self._size_tab = None

    @property
    def size_tab(self):
        if self._size_tab is None:
            raise AttributeError("Size table was not computed")
        else:
            return self._size_tab
    
    
    def clusters_to_dict(self):
        """ Transforms the membership table in a dictionnary.
        This is usefull to put cluster node attributes.
        """
        clusters_dict = {}
        for i in range(self.mem_tab.shape[0]):
            clusters_dict[i] = self.mem_tab[i]
        return clusters_dict
    
    def add_clusters_to_graph(self, G):
        """ Adds the cluster labelling to the nodes attributes of a graph
        """
        _check_format(G, self.mem_tab.shape[0])
        clusters_dict = self.clusters_to_dict()
        nx.set_node_attributes(G, clusters_dict, 'cluster')

    def compute_sizes(self):
        pass