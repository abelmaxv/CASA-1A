import numpy as np
import networkx as nx
from matplotlib import colormaps

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



def _convert_to_hex(color):
    """ Converts a color in the forma RGB to a color in rhe format hex.
    """
    return '#'+ hex(round(256*color[0]))[2:3] + hex(round(256*color[1]))[2:3] + hex(round(256*color[2]))[2:3]



class Clustering(object):
    """ Class to represent one clustering of a graph

    Attributes
    ----------
        mem_tab : membership table of the clustering

        size_tab : stores the size of each cluster of the clustering
    """

    def __init__(self, mem_tab, size_tab):
        self.mem_tab = mem_tab
        self.size_tab = size_tab
        self._cluster_colors = None

    @property
    def cluster_colors(self):
        if self._cluster_colors is None: 
            raise AttributeError("Cluster colors were not initialised. Run self.get_cluster_colors.")
        else : 
            return self._cluster_colors
    
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

    def get_cluster_colors(self, cmap = "plasma", start = 0, stop = 1):
        """ Generate a color palatte with one color for each cluster

        Paramters
        ---------
            cmap: Name of the matplotlib colormap from which to choose the colors.
            
            start : Where to start in the colorspace (from 0 to 1).
            
            stop : Where to end in the colorspace (from 0 to 1).

        Returns
        -------
            colors_hex : a list of hex color for each cluster
        """
        n = self.size_tab.shape[0]
        colors = colormaps[cmap](np.linspace(start, stop, n)) 
        #Shuffle so that close labels don't have the same color
        np.random.shuffle(colors)
        colors_hex = [_convert_to_hex(color) for color in colors]
        self._cluster_colors = colors_hex
        return colors_hex
    

    def get_node_colors (self, cmap = "plasma", start = 0, stop = 1, change = False):
        """
        """
        n = self.mem_tab.shape[0]
        if self._cluster_colors is None or change :
            cluster_colors = self.get_cluster_colors(cmap, start, stop)
        else: 
            cluster_colors = self.cluster_colors
        
        node_colors = ["" for i in range(n)]
        for i in range(n):
            node_colors[i] = cluster_colors[self.mem_tab[i]]
        
        return node_colors
    