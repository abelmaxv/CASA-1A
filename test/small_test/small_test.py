import networkx as nx
import matplotlib.pyplot as plt
from numpy import sqrt
from percolation.percolation import Percolation
import osmnx as ox

# The small model is Meudon street network
print("Importing the network ... \n")
G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)
print(f"Size of the model : {G.number_of_nodes()} \n")

# Displaying the produced graph : 
print("Displaying the graph ... \n ")
ox.plot.plot_graph(G, node_color = '#3F4A99', edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = "test/small_test/small_network.png", close = True)

# Percolate the network :
print("Percolating ... \n") 
clusterer = Percolation()
clusterer.percolate(G)

# Display the linkage tree :
print("Displaying the percolation tree ... \n")
clusterer.linkage_tree.plot(truncate_mode='level', p = 7)
plt.title("Simplified percolation tree of the small model (Meudon, France)")
plt.savefig("test/small_test/small_percolation_tree.png")
plt.close()

print("\n \n \n")

# Extract clusters at a threshold : 
threshold = 200
print(f"Extracting clusters at threshold {threshold} ... \n")
clustering = clusterer.linkage_tree.label_of_cut(threshold)
print(f"Membership table of the clustering with treshold {threshold} :")
print(clustering.mem_tab)
print("\n")
print(f"Sizes of the clusters with treshold {threshold} :")
print(clustering.size_tab)
clustering.add_clusters_to_graph(G)

# Display the clusters : 
print(f"Displaying the clusters at threshold {threshold} ... \n")
node_colors = clustering.get_node_colors(min_size = 20)
ox.plot.plot_graph(G, node_color = node_colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = "test/small_test/small_clustering.png", close = True)

print("\n \n \n")

# Compute the condensed tree
print("Computing the condensed tree ... \n")
clusterer.compute_condensed_tree(min_size=20)

# Display the condense tree
print("Displaying the condensed tree ... \n")
clusterer.condensed_tree.plot()
plt.title("Condensed tree of the small model (Meudon, France)")
plt.savefig("test/small_test/small_condensed_tree.png")
plt.close()


# Get clusters out of stability
print("Computing stability clusters ... \n")
clustering = clusterer.condensed_tree.label_of_stability()
print("Membership table of the stability clustering : ")
print(clustering.mem_tab)
print("\n")
print("Sizes of the stability clusters : ")
print(clustering.size_tab)

# Displaying clusters in the tree
print("Displaying clusters in the tree... \n")
clusterer.condensed_tree.plot(select_clusters = True)
plt.title("Condensed tree with clusters of the small model (Meudon, France)")
plt.savefig("test/small_test/small_clusters_condensed_tree.png")
plt.close()

# Displaying the clusters
print("Displaying the stability clusters ... \n")
node_colors = clustering.get_node_colors()
ox.plot.plot_graph(G, node_color = node_colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = "test/small_test/small_stability_clustering.png", close = True)
