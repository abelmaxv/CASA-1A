#import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from percolation import Percolation
import matplotlib.pyplot as plt
from osmnx import graph_from_place 

G = graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)
pos = 

# Create a new multidigraph
#G = nx.MultiDiGraph()

# Add nodes
#G.add_nodes_from([0, 1, 2])

# Add edges with length attribute
#G.add_edge(0, 1, length=5.0)
#G.add_edge(0, 2, length=7.5)
#G.add_edge(1, 2, length=3.0)
#G.add_edge(2, 0, length=2.5)


#fig, ax = ox.plot_graph(G,
#                        bgcolor= 'w',
#                        node_color='k',
#                        node_size = 10)


clusterer = Percolation(G)

clusterer.percolate()

clusters = clusterer.linkage_tree.label_of_cut(100)

cls = [i/len(clusters) for i in range(len(clusters))]
i=0
while i<5:
    nx.draw_networkx_nodes(G, 
                           pos=pos,
                           node_color=cls[i],
                           node_size=4,
                           ax=ax, 
                           nodelist= list(communities_fg[i])
                          )
    i+=1