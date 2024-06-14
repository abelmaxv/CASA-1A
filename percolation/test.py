import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from percolation import Percolation

G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)




#fig, ax = ox.plot_graph(G,
#                        bgcolor= 'w',
#                        node_color='k',
#                        node_size = 10)


clusterer = Percolation(G)

clusterer.percolate()