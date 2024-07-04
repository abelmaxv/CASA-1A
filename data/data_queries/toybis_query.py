import networkx as nx
from numpy import sqrt

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
    8 : {"coords" : (50,8.)},
    9 : {"coords" : (60,17.5)},
    10 : {"coords" : (65,8)}     
}

nx.set_node_attributes(G,coords)

# Edge weights are euclidian distances : 
length = {}
dist = lambda e: sqrt((coords[e[0]]["coords"][0] - coords[e[1]]["coords"][0])**2 + (coords[e[0]]["coords"][1] - coords[e[1]]["coords"][1])**2)
for u,v in edge_list:
    length[(u,v,0)] = {"length" : dist((u,v))}
nx.set_edge_attributes(G,length)

# Formating the network
print("Formating the network ...\n")
G = G.to_undirected()

#Saving the network
print("Saving the network...\n ")
nx.write_gml(G, "data/data/networks/toybis.gml")

