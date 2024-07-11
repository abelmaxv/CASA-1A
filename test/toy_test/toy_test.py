import networkx as nx
import matplotlib.pyplot as plt
from os import path, makedirs
from percolation.percolation import Percolation
from src.linkage_tree import LinkageTree
from src.cluster import Clustering
from src.condensed_tree import CondensedTree

# Importing the toy model
print("Importing the network ... \n")

network_path = "data/data/networks/toy.gml"
if path.isfile(network_path):
    G = nx.read_gml(network_path, destringizer= int)
else : 
    print("Creating the network ...")
    import data.data_queries.toy_query
    G = nx.read_gml(network_path, destringizer= int)

print(f"\nSize of the model : {G.number_of_nodes()} \n")

# Displaying the produced graph : 
print("Displaying the graph ... \n ")
network_display_path = "test/toy_test/toy_network.png"
if not(path.isfile(network_display_path)):
    pos = nx.get_node_attributes(G, 'coords')
    nx.draw_networkx_nodes(G,pos, node_color='#6FCC9F', node_size=30)
    nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
    plt.title("Toy model network")
    plt.axis("off")
    plt.savefig(network_display_path)
    plt.close()
else: 
    print("Graph had already been plotted. \n")



print("\n \n \n")


# Generate the percolation tree :
print("Generating the percolation tree ... \n")
tree_path = "data/data/percolation_trees/toy_tree.npy"
if path.isfile(tree_path):
    print("Percolation tree had already been computed. \n")
    percolation_tree = LinkageTree(path = tree_path)
else : 
    print("Creating percolation tree ... \n")  
    clusterer = Percolation()
    clusterer.percolate(G)
    percolation_tree = clusterer.linkage_tree
    percolation_tree.save(tree_path)

# Display the linkage tree : 
print("Displaying the percolation tree ... \n")
tree_display_path = "test/toy_test/toy_percolation_tree.png"
if not(path.isfile(tree_display_path)): 
    percolation_tree.plot()
    plt.title("Percolation tree of the toy model")
    plt.savefig(tree_display_path)
    plt.close()
else :
    print("Percolation tree had already been plotted.")



print("\n \n \n")



# Extract clusters at a threshold : 
threshold = 3

print(f"Extracting clusters at threshold {threshold} ... \n")
cluster_path = "data/data/clusters/toy/cut/" + str(threshold) + "/"

if path.exists(cluster_path):
    print(f"Cut at threshold {threshold} had already been computed.")
    clustering = Clustering(mem_path= cluster_path + "mem.npy", size_path= cluster_path + "size.npy", color_path= cluster_path + "color.csv")
else :
    makedirs(cluster_path)
    clustering = percolation_tree.label_of_cut(threshold)
    clustering.get_cluster_colors()
    clustering.save(mem_path= cluster_path + "mem.npy", size_path= cluster_path + "size.npy", color_path= cluster_path + "color.csv")

print(f"Membership table of the clustering with treshold {threshold} :")
print(clustering.mem_tab)
print("\n")
print(f"Sizes of the clusters with treshold {threshold} :")
print(clustering.size_tab)


# Display the clusters :
print(f"Displaying the clusters at threshold {threshold} ... \n") 
pos = nx.get_node_attributes(G, "coords")
cut_display_path = "test/toy_test/toy_cut_clustering"+ str(threshold)+".png"
if path.isfile(cut_display_path) : 
    print(f"Cut clusters at threshold {threshold} had already been displayed.")
else : 
    clustering.add_clusters_to_graph(G)
    node_colors = clustering.get_node_colors()
    nx.draw_networkx_nodes(G,pos, node_color=node_colors, node_size=30)
    nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
    plt.title(f"Clustering of the toy model at threshold {threshold}")
    plt.axis("off")
    plt.savefig(cut_display_path)
    plt.close()



print("\n \n \n")



# Compute the condensed tree
min_size = 2
print(f"Handling the condensed tree with min_cluster_size {min_size} ... \n")
condensed_tree_path = "data/data/condensed_trees/toy/" + str(min_size) + "/"
if path.exists(condensed_tree_path):
    condensed_tree = CondensedTree(path = condensed_tree_path + "/toy_condensed_tree" + str(min_size) + ".npy")
else : 
    print("Computing the condensed tree ... \n")
    makedirs(condensed_tree_path)
    condensed_tree = percolation_tree.compute_condensed_tree(min_size=min_size)
    condensed_tree.save(condensed_tree_path + "/toy_condensed_tree" + str(min_size) + ".npy")


# Display the condensed tree
print("Displaying the condensed tree ... \n")
condensed_displayed_path = "test/toy_test/toy_condensed_tree"+str(min_size)+".png"
if path.isfile(condensed_displayed_path):
    print(f"Condensed tree with min_size {min_size} had already been computed.")
else : 
    condensed_tree.plot()
    plt.title(f"Condensed tree of the toy model (min_size={min_size})")
    plt.savefig(condensed_displayed_path)
    plt.close()



print("\n \n \n")



# Get clusters out of stability
print("Computing stability clusters ... \n")
cluster_path = "data/data/clusters/toy/stability/" + str(min_size) + "/"
if path.exists(cluster_path):
    print(f"Stability clusters with min_size {min_size} had already been computed.")
    clustering = Clustering(mem_path= cluster_path + "mem.npy", size_path= cluster_path + "size.npy", color_path= cluster_path + "color.csv")
else :
    makedirs(cluster_path)
    clustering = condensed_tree.label_of_stability()
    clustering.get_cluster_colors()
    clustering.save(mem_path= cluster_path + "mem.npy", size_path= cluster_path + "size.npy", color_path= cluster_path + "color.csv")

print(f"Membership table of the stability clustering  with min_size {min_size}: ")
print(clustering.mem_tab)
print(f"Sizes of the clusters with min_size {min_size} :")
print(clustering.size_tab)



# Displaying clusters in the tree
print("Displaying clusters in the condensed tree... \n")
cluster_condensed_display_path = "test/toy_test/toy_clusters_condensed_tree"+str(min_size)+".png"
if path.isfile(cluster_condensed_display_path):
    print(f"Condensed tree with clusters with min size {min_size} had already been computed.")
else :
    condensed_tree.plot(select_clusters = True)
    plt.title(f"Condensed tree with clusters of the toy model (min_size={min_size})")
    plt.savefig(cluster_condensed_display_path)
    plt.close()

# Displaying the stability clusters
print(f"Displaying the clusters with min_size {min_size} ... \n") 
stability_display_path = "test/toy_test/toy_stability_clustering"+ str(min_size)+".png"
if path.isfile(stability_display_path) : 
    print(f"Stability clusters at min_size {min_size} had already been displayed.")
else : 
    clustering.add_clusters_to_graph(G)
    node_colors = clustering.get_node_colors()
    nx.draw_networkx_nodes(G,pos, node_color=node_colors, node_size=30)
    nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
    plt.title(f"Stability clustering of the toy model")
    plt.axis("off")
    plt.savefig(stability_display_path)
    plt.close()
