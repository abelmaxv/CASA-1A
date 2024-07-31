import networkx as nx
import numpy as np
import osmnx as ox
from sklearn.cluster import HDBSCAN
from src.cluster import Clustering

# Load the graph
network_path = "data/data/networks/meudon.gml"
node_dtypes = {'id': int}
G = ox.load_graphml(network_path, node_dtypes=node_dtypes)
G = G.to_undirected()


# Compute the shortest path length between all pairs of nodes using Floyd-Warshall
dist_matrix_np = nx.floyd_warshall_numpy(G, weight="length")
print(dist_matrix_np)


# Apply HDBSCAN clustering
clusterer = HDBSCAN(min_cluster_size=20, metric='precomputed', min_samples = 2)
cluster_labels = clusterer.fit_predict(dist_matrix_np)

print(cluster_labels)

membership_table_np = np.array(cluster_labels)
clustering = Clustering(membership_table_np)

stability_display_path = "test/floyd_hdbscan/floyd_hdbscan.png"
clustering.add_clusters_to_graph(G)
node_colors = clustering.get_node_colors()
ox.plot.plot_graph(G, node_color = node_colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF', show = False, save = True, filepath = stability_display_path, close = True)