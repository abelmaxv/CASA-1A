import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox

# The very large model is London street network
print("Importing the network ... \n")
G = ox.graph_from_place("London, United Kingdom", network_type = "drive", simplify = True)


# Formating the network
print("Formating the network... \n")
G = nx.convert_node_labels_to_integers(G)
G = G.to_undirected()

#Saving the network 
print("Saving the network... \n")
ox.save_graphml(G, "data/data/networks/london.gml")

