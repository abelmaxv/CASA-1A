import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from percolation.percolation import Percolation
import osmnx as ox

# The small model is Meudon street network
print("Importing the network ... \n")
G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)

# Computes percolation
print("Percolates ...")
clusterer = Percolation()
clusterer.percolate(G)

# Mean size measures
start = 2
end = 30
step = 2

print(f"Doing measures for min_size in range {start} - {end} ...")

X = []
Y = []

for min_size in range(start, end, step):
    clusterer.compute_condensed_tree(min_size)
    clustering = clusterer.condensed_tree.label_of_stability()
    if clustering.size_tab.size != 0:
        print(clustering.size_tab)
        X.append(min_size)
        Y.append(np.mean(clustering.size_tab))


# Ploting the graph
plt.plot(X,Y)
plt.xlabel("min_size")
plt.ylabel("<clust_size>")
plt.show()
