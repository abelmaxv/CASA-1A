#import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from percolation import Percolation

#G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)

# Create a new multidigraph
G = nx.MultiDiGraph()

# Add nodes
G.add_nodes_from([0, 1, 2])

# Add edges with length attribute
G.add_edge(0, 1, length=5.0)
G.add_edge(0, 2, length=7.5)
G.add_edge(1, 2, length=3.0)
G.add_edge(2, 0, length=2.5)


#fig, ax = ox.plot_graph(G,
#                        bgcolor= 'w',
#                        node_color='k',
#                        node_size = 10)


clusterer = Percolation(G)

clusterer.percolate()
print(clusterer.percolation_tree)