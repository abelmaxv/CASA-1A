import networkx as nx
import matplotlib.pyplot as plt
from numpy import sqrt
from percolation.percolation import Percolation

# Creation of the toy model
print("Building the network ... \n")
G = nx.MultiDiGraph()

# Clics that are connected by a few edges :
edge_list = [(0,1), (0,2), (0,3), (1,2), (1, 3), (2, 3),
     (4,5), (4,6), (4, 7), (5, 6), (5, 7), (6, 7),
     (8,9), (8, 10), (9, 10), 
     (1, 4), (3, 6), (3, 9), (6, 8), (7, 8)
     ]
G.add_edges_from(edge_list)

# The network is embeded in the space (as a street network): 
coords = {
    0 : {"coords" :(3.,8.)},
    1 : {"coords" :(4.5,10.)},
    2 : {"coords" : (4.,6.)},
    3 : {"coords" : (7.,8.)},
    4 : {"coords" : (9.,16.)},
    5 : {"coords" : (10.5,17.5)},
    6 : {"coords" : (12.,16.)},
    7 : {"coords" : (13.5,17.5)},
    8 : {"coords" : (23.,2.5)},
    9 : {"coords" : (24.5,4.)},
    10 : {"coords" : (26.5,2.)}     
}

nx.set_node_attributes(G,coords)

# Edge weights are euclidian distances : 
length = {}
dist = lambda e: sqrt((coords[e[0]]["coords"][0] - coords[e[1]]["coords"][0])**2 + (coords[e[0]]["coords"][1] - coords[e[1]]["coords"][1])**2)
for u,v in edge_list:
    length[(u,v,0)] = {"length" : dist((u,v))}
nx.set_edge_attributes(G,length)
print("Edges of the graph : ")
print(G.edges(data = True))

print(f"Size of the model : {G.number_of_nodes()} \n")

# Displaying the produced graph : 
print("Displaying the graph ... \n ")
pos = nx.get_node_attributes(G, 'coords')
nx.draw_networkx_nodes(G,pos, node_color='#6FCC9F', node_size=30)
nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
plt.title("Toy model network for testing algorithms")
plt.axis("off")
plt.savefig("test/toy_test/toy_network.png")
plt.close()

# Percolate the network :
print("Percolating ... \n")  
clusterer = Percolation()
clusterer.percolate(G)

# Display the linkage tree : 
print("Displaying the percolation tree ... \n")
clusterer.linkage_tree.plot()
plt.title("Percolation tree of the toy model")
plt.savefig("test/toy_test/toy_percolation_tree.png")
plt.close()

print("\n \n \n")

# Extract clusters at a threshold : 
threshold = 3
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
node_colors = clustering.get_node_colors()
nx.draw_networkx_nodes(G,pos, node_color=node_colors, node_size=30)
nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
plt.title(f"Clustering of the toy model at threshold {threshold}")
plt.axis("off")
plt.savefig("test/toy_test/toy_clustering.png")
plt.close()


# Compute the condensed tree
min_cluster_size = 2
print(f"Computing the condensed tree with min_cluster_size {min_cluster_size} ... \n")

# Display the condensed tree
print("Displaying the condensed tree ... \n")
clusterer.compute_condensed_tree(min_cluster_size)
clusterer.condensed_tree.plot()
plt.title("Condensed tree of the toy model")
plt.savefig("test/toy_test/toy_condensed_tree.png")