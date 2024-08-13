import networkx as nx
import osmnx as ox

# The meudon model is Meudon street network
print("Importing the network ... \n")
G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)


# Formating the network
print("Formating the network ... \n")
G = nx.convert_node_labels_to_integers(G)
G = G.to_undirected()

#Saving the network 
print("Saving the network... \n")
ox.save_graphml(G, "data/data/networks/meudon.gml")

