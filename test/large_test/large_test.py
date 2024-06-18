import networkx as nx
import matplotlib.pyplot as plt
from numpy import sqrt
from percolation.percolation import Percolation
import osmnx as ox

# The small model is Modena street network
G = ox.graph_from_place("Modena, Italy", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)

# Displaying the produced graph : 
ox.plot.plot_graph(G,node_size = 5, node_color = '#3F4A99', edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = "test/large_test/large_network.png", close = True)

# Percolate the network : 
clusterer = Percolation()
clusterer.percolate(G)

# Display the linkage tree :
clusterer.linkage_tree.plot()
plt.savefig("test/large_test/large_percolation_tree.png")
plt.close()

print("\n \n \n")

# Extract clusters at a threshold : 
treshold = 300
clustering = clusterer.linkage_tree.label_of_cut(treshold)
print(f"Membership table of the clustering with treshold {treshold} :")
print(clustering.mem_tab)
print("\n")
print(f"Sizes of the clusters with treshold {treshold} :")
print(clustering.size_tab)
clustering.add_clusters_to_graph(G)

# Display the clusters : 
node_colors = clustering.get_node_colors()
ox.plot.plot_graph(G, node_size = 5, node_color = node_colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = "test/large_test/large_clustering.png", close = True)
