from sklearn.cluster import HDBSCAN
import osmnx as ox
import networkx as nx 
import numpy as np
from src.cluster import Clustering

print("import network... \n")
G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)
#ox.plot.plot_graph(G, node_color = '#3F4A99', edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = True, save = False, filepath = "test/small_test/small_clustering.png", close = True)

print("Floyd Warshall... \n")
dist_dict  = nx.floyd_warshall(G, weight="length")
n = G.number_of_nodes()


print("computing matrix... \n ")
dist_mat = np.zeros((n,n))
for i in range(n):
    for j in range(i, n):
        dist_mat[i,j] = dist_dict[i][j]
        dist_mat[j,i] = dist_dict[i][j]

print("HDBSCAN... \n")
clusterer = HDBSCAN(min_cluster_size = 20, metric= "precomputed", min_samples = 1)
clusterer.fit(dist_mat)
labels = clusterer.labels_
print(labels)
clustering = Clustering(clusterer.labels_)
print("computing sizes.... \n")
clustering.get_size_tab()
print('ok')

print('getting colors ... \n')
colors = clustering.get_node_colors()

print("displaying the graph... \n")
ox.plot.plot_graph(G, node_color = colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = True, save = False, filepath = "test/small_test/small_clustering.png", close = True)