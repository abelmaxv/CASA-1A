import matplotlib.pyplot as plt
from os import path, makedirs
import pandas as pd
from NetHDBSCAN.percolation import Percolation
from NetHDBSCAN.structures import Clustering, CondensedTree, LinkageTree
from IPython.display import display


# Display libs
import datashader as ds
import datashader.transfer_functions as tf
import matplotlib.pyplot as plt
from datashader.colors import rgb
import numpy as np

# Importing the uk model
print("Importing the network ... \n")

network_path = "data/data/networks/uk.csv"
nodes_path = "data/data/networks/uk_nodes.csv"

if path.isfile(network_path):
    G = pd.read_csv(network_path)
    display(G)
    nodes = pd.read_csv(nodes_path)
    display(nodes)
else : 
    print("Creating the network ...")
    import data.data_queries.uk_query
    print("Network created... \n ")
    G = pd.read_csv(network_path)
    nodes = pd.read_csv(nodes_path)

size = max(G["source"].max(), G["target"].max())+1
print(f"\nSize of the model : {size} \n")

print(f"Number of nodes to plot : {nodes.shape[0]} \n")

# Displaying the produced graph : 
print("Displaying the graph ... \n ")
network_display_path = "test/uk_test/uk_network.png"
if not(path.isfile(network_display_path)):
    canvas = ds.Canvas(plot_width=1000, plot_height=1000)
    agg = canvas.points(nodes, "x_coord", "y_coord", agg=ds.any())
    img = tf.shade(agg)
    img = np.array(img.to_pil())

    # Create a figure and axis with Matplotlib
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), facecolor='w', constrained_layout=True)
    ax.imshow(img)
    ax.axis('off')  # Turn off the axis
    ax.set_aspect('equal')  # Set aspect ratio to 'equal'


    # Save the figure
    plt.tight_layout()
    plt.savefig(network_display_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

else: 
    print("Graph had already been plotted. \n")



print("\n \n \n")


# Generate the percolation tree :
print("Generating the percolation tree ... \n")
tree_path = "data/data/percolation_trees/uk_tree.npy"
if path.isfile(tree_path):
    print("Percolation tree had already been computed. \n")
    percolation_tree = LinkageTree(path = tree_path)
else : 
    print("Creating percolation tree ... \n")  
    clusterer = Percolation()
    clusterer.percolate(G, data_type = "pandas")
    percolation_tree = clusterer.linkage_tree
    print("Saving the tree ... \n")
    percolation_tree.save(tree_path)

# Display the linkage tree : 
#print("Displaying the percolation tree ... \n")
#tree_display_path = "test/uk_test/uk_percolation_tree.png"
#if not(path.isfile(tree_display_path)): 
#    percolation_tree.plot(truncate_mode="level", p=10)
#    plt.title("Percolation tree of the uk model")
#    plt.savefig(tree_display_path)
#    plt.close()
#else :
#    print("Percolation tree had already been plotted.")



print("\n \n \n")



# Extract clusters at a threshold : 
threshold = 190

print(f"Extracting clusters at threshold {threshold} ... \n")
cluster_path = "data/data/clusters/uk/cut/" + str(threshold) + "/"

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
cut_display_path = "test/uk_test/uk_cut_clustering"+ str(threshold)+".png"
if path.isfile(cut_display_path) : 
    print(f"Cut clusters at threshold {threshold} had already been displayed.")
else : 
    clustering.add_clusters_to_graph(nodes, data_type = "pandas")
    colors = clustering.cluster_colors
    
    nodes_color = clustering.get_node_colors(min_size = 1000)
    color_key = {color: rgb(color[:7]) for color in colors}
    color_key["#8C8C8C"] = rgb("#8C8C8C")

    nodes["color"] = nodes["node"].apply(lambda x : nodes_color[x])
    nodes['color'] = nodes['color'].astype('category')
    canvas = ds.Canvas(plot_width= 1000, plot_height=1000)
    
    agg = canvas.points(nodes, "x_coord", "y_coord", agg = ds.count_cat("color"))

    img = tf.shade(agg, color_key=color_key)

    img = np.array(img.to_pil())
    plt.figure(figsize=(10, 10))
    plt.imshow(img,aspect = "auto")
    plt.axis("off")
    plt.savefig(cut_display_path, dpi=300, bbox_inches='tight', pad_inches=0) 
    plt.close()
    
    


print("\n \n \n")



# Compute the condensed tree
min_size = 10000
print(f"Handling the condensed tree with min_cluster_size {min_size} ... \n")
condensed_tree_path = "data/data/condensed_trees/uk/" + str(min_size) + "/"
if path.exists(condensed_tree_path):
    condensed_tree = CondensedTree(path = condensed_tree_path + "/uk_condensed_tree" + str(min_size) + ".npy")
else : 
    print("Computing the condensed tree ... \n")
    makedirs(condensed_tree_path)
    condensed_tree = percolation_tree.compute_condensed_tree(min_size=min_size)
    condensed_tree.save(condensed_tree_path + "/uk_condensed_tree" + str(min_size) + ".npy")


# Display the condensed tree
print("Displaying the condensed tree ... \n")
condensed_displayed_path = "test/uk_test/uk_condensed_tree"+str(min_size)+".png"
if path.isfile(condensed_displayed_path):
    print(f"Condensed tree with min_size {min_size} had already been computed.")
else : 
    condensed_tree.plot()
    plt.savefig(condensed_displayed_path)
    plt.close()



print("\n \n \n")



# Get clusters out of stability
print("Computing stability clusters ... \n")
cluster_path = "data/data/clusters/uk/stability/" + str(min_size) + "/"
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
cluster_condensed_display_path = "test/uk_test/uk_clusters_condensed_tree"+str(min_size)+".png"
if path.isfile(cluster_condensed_display_path):
    print(f"Condensed tree with clusters with min size {min_size} had already been computed.")
else :
    condensed_tree.plot(select_clusters = True)
    plt.savefig(cluster_condensed_display_path)
    plt.close()

# Displaying the stability clusters
print(f"Displaying the clusters with min_size {min_size} ... \n") 
stability_display_path = "test/uk_test/uk_stability_clustering"+ str(min_size)+".png"
if path.isfile(stability_display_path) : 
    print(f"Stability clusters at min_size {min_size} had already been displayed.")
else : 
    clustering.add_clusters_to_graph(nodes, data_type = "pandas")
    colors = clustering.cluster_colors
    
    nodes_color = clustering.get_node_colors(min_size = 1000)
    color_key = {color: rgb(color[:7]) for color in colors}
    color_key["#8C8C8C"] = rgb("#8C8C8C")

    nodes["color"] = nodes["node"].apply(lambda x : nodes_color[x])
    nodes['color'] = nodes['color'].astype('category')
    canvas = ds.Canvas(plot_width= 1000, plot_height=1000)

    agg = canvas.points(nodes, "x_coord", "y_coord", agg = ds.count_cat("color"))

    img = tf.shade(agg, color_key=color_key, how='eq_hist')

    img = np.array(img.to_pil())
    plt.figure(figsize=(10, 10))
    plt.imshow(img, aspect = "auto")
    plt.axis("off")
    plt.savefig(stability_display_path, dpi=300, bbox_inches='tight', pad_inches=0) 
    plt.close()
