import networkx as nx
import matplotlib.pyplot as plt
from percolation import Percolation
import matplotlib.pyplot as plt
import osmnx as ox

G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)


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


clusters = clusterer.linkage_tree.label_of_cut(50)
clusters.add_clusters_to_graph(G)

clusterer.linkage_tree.plot()

plt.show()


print(clusters.tab)

#cls = ox.plot.get_node_colors_by_attr(G, 'cluster', cmap='tab20')

#fig, ax = plt.subplots(figsize=(12,7))

#fig, ax = ox.plot_graph(G, 
#                        node_color=cls,
#                        node_size = 25,
#                        ax=ax)