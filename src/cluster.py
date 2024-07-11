import numpy as np
import networkx as nx
from matplotlib import colormaps
from warnings import warn
import pandas as pd

def _check_format_pd(G):
    """ Check if the cluster labelling can be applied on a graph : 
    G must be a pandas Dataframe with a node column 
    """
    if not isinstance(G,pd.DataFrame):
        raise AttributeError("Wrong datatype. Clustering must operate on a networkx object or specify pandas")
    elif not ("node" in G.columns):
        raise AttributeError("The DataFrame must have a node column.")


def _check_format(G, size_tab):
    """ Check if the cluster labelling can be applied on a graph : 
    - G must a nx.MultiDiGrpah
    - Nodes must be labelled with integer 0,...,n-1 
    - n must be lower than self.mem_arr.shape[0]
    """
    if not (isinstance(G, nx.MultiDiGraph) or isinstance(G, nx.MultiGraph) or isinstance(G, nx.DiGraph) or isinstance(G, nx.Graph)):
        raise AttributeError("Wrong datatype. Clustering must operate on a networkx object")
    
    size = G.number_of_nodes()
    for n in G.nodes():
        if not(0 <= n < size):
            raise AttributeError("Nodes must be labeled with ordered integers. Add G = nx.convert_node_labels_to_integers(G) to the script.")
        if size_tab <= n:
            raise AttributeError("Can not apply clustering to the graph because id is to high")



def _convert_to_hex(color):
    """Converts a color in the format RGBA to a color in the format hex.
    
    Args:
        color (tuple): A tuple containing four elements (R, G, B, A) each ranging from 0 to 1.
        
    Returns:
        str: The hex representation of the color.
    """
    r = round(255 * color[0])
    g = round(255 * color[1])
    b = round(255 * color[2])
    a = round(255 * color[3])
    
    return '#{:02X}{:02X}{:02X}{:02X}'.format(r, g, b, a)



class Clustering(object):
    """ Class to represent one clustering of a graph

    Attributes
    ----------
        mem_tab : membership table of the clustering

        size_tab : stores the size of each cluster of the clustering

        cluster_colors : contains color for each cluster

        mem_path : path to initialise membership table from csv file

        size_path : path to initialise size table from csv file

        color_path : path to initialise color table from csv file
    """

    def __init__(self, mem_tab = None, size_tab = None, cluster_colors = None, mem_path = None, size_path = None, color_path = None):
        if mem_path != None : 
            if mem_path[-4:] != ".npy":
                raise AttributeError("The membership table is suppose to be generated from a csv file.")
            else:
                self._mem_tab = np.load(mem_path)
        else :
            self._mem_tab = mem_tab

        if size_path != None : 
            if size_path[-4:] != ".npy":
                raise AttributeError("The size table is suppose to be generated from a csv file.")
            else:
                self._size_tab = np.load(size_path)
        else :
            self._size_tab = size_tab

        if color_path != None : 
            if color_path[-4:] != ".csv":
                raise AttributeError("The color table is suppose to be generated from a csv file.")
            else:
                self._cluster_colors = np.genfromtxt(color_path, dtype=str, delimiter=',', comments=None)
        else :
            self._cluster_colors = cluster_colors
    
    
    @property
    def mem_tab(self):
        if self._mem_tab is None: 
            raise AttributeError("Membership table was not initialised.")
        else : 
            return self._mem_tab
        
    @property
    def cluster_colors(self):
        if self._cluster_colors is None: 
            raise AttributeError("Cluster colors were not initialised. Run self.get_cluster_colors.")
        else : 
            return self._cluster_colors
        
    @property
    def size_tab(self):
        if self._size_tab is None : 
            raise AttributeError("Size table was not initialised. Run self.get_size_tab.")
        else :
            return self._size_tab

    def get_size_tab(self):
        """ TO DO
        """
        size_tab = np.zeros(self.mem_tab.shape[0])
        for i in self.mem_tab:
            size_tab[i] +=1
        i = 0 
        while i < size_tab.shape[0]:
            if size_tab[i] == 0:
                size_tab = np.delete(size_tab, i, axis = 0)
            else: 
                i+=1
        self._size_tab = size_tab
        return self
    
    def clusters_to_dict(self):
        """ Transforms the membership table in a dictionnary.
        This is usefull to put cluster node attributes.
        """
        clusters_dict = {}
        for i in range(self.mem_tab.shape[0]):
            clusters_dict[i] = self.mem_tab[i]
        return clusters_dict
    
    def add_clusters_to_graph(self, G, data_type = "networkx"):
        """ Adds the cluster labelling to the nodes attributes of a graph
        """
        if data_type == "networkx":
            _check_format(G, self.mem_tab.shape[0])
            clusters_dict = self.clusters_to_dict()
            nx.set_node_attributes(G, clusters_dict, 'cluster')
        elif data_type == "pandas":
            _check_format_pd(G)
            G["cluster"] = G["node"].apply(lambda x : self.mem_tab[x])
            G['cluster'] = pd.Categorical(G['cluster'])

    def get_cluster_colors(self, cmap = "plasma", start = 0, stop = 1, min_size = 0, default = "#8C8C8C"):
        """ Generate a color palatte with one color for each cluster

        Paramters
        ---------
            cmap: Name of the matplotlib colormap from which to choose the colors.
            
            start : Where to start in the colorspace (from 0 to 1).
            
            stop : Where to end in the colorspace (from 0 to 1).

            min_size : if a cluster has a size too small it is colored with default color

            default : default color (grey)

        Returns
        -------
            colors_hex : a list of hex color for each cluster
        """
        if self._size_tab is None:
            self.get_size_tab()
        n = self._size_tab.shape[0]
        colors = colormaps[cmap](np.linspace(start, stop, n)) 
        #Shuffle so that close labels don't have the same color
        np.random.shuffle(colors)
        colors_hex = [_convert_to_hex(colors[i]) if self.size_tab[i] >= min_size else default for i in range(colors.shape[0])]
        self._cluster_colors = colors_hex
        return colors_hex
    

    def get_node_colors (self, cmap = "plasma", start = 0, stop = 1, min_size = 0, default = "#8C8C8C", change = False):
        """ Attributes a color per node associated to its label

        Parameters
        ----------
            cmap: Name of the matplotlib colormap from which to choose the colors.
            
            start : Where to start in the colorspace (from 0 to 1).
            
            stop : Where to end in the colorspace (from 0 to 1).

            change : if False, it uses the precomputed colors
                     if True, it computes new colors
            
            min_size : if a cluster has a size too small it is colored with default color

            default : default color (grey)
        
        Returns
        -------
            node_colors : an array of string with hex color for each node

        """
        n = self.mem_tab.shape[0]
        if self._cluster_colors is None or change :
            cluster_colors = self.get_cluster_colors(cmap, start, stop, min_size, default)
        else: 
            cluster_colors = self.cluster_colors
        
        node_colors = ["" for i in range(n)]
        for i in range(n):
            if self.mem_tab[i] != -1 : 
                node_colors[i] = cluster_colors[self.mem_tab[i]]
            else: 
                node_colors[i] = default
        
        return node_colors
    


    def save(self, mem_path = None, size_path = None, color_path = None):
        """ Save the cluster in a csv file

        Parameters 
        ----------
            mem_path : path where to store the membership table

            size_path : path where to store the size table

            color_path : path where to store the color table
        """
        if mem_path[-4:] != ".npy" or size_path[-4:] != ".npy" or color_path[-4:] != ".csv":
            raise AttributeError("Wrong file formats for saving.")
        
        try :
            if mem_path != None:
                np.save(mem_path, self.mem_tab) 
        except AttributeError:
            warn("No membership table to save ... \n")
       
        try :
            if size_path != None:
                np.save(size_path, self.size_tab) 
        except AttributeError:
            warn("No size table to save ... \n")

        try :
            if color_path != None:
                cluster_colors = self.cluster_colors
                np.savetxt(color_path, cluster_colors, fmt='%s', delimiter=",") 
        except AttributeError:
            warn("No color table to save ... \n")

        return