import networkx as nx
import matplotlib.pyplot as plt
from numpy import sqrt
from percolation.percolation import Percolation

# Creation of the toy model
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

# Edges weight are euclidian distance : 
length = {}
dist = lambda e: sqrt((coords[e[0]]["coords"][0] - coords[e[1]]["coords"][0])**2 + (coords[e[0]]["coords"][1] - coords[e[1]]["coords"][1])**2)
for u,v in edge_list:
    length[(u,v,0)] = {"length" : dist((u,v))}
nx.set_edge_attributes(G,length)
print("Edges of the graph : ")
print(G.edges(data = True))

# Displaying the produced graph : 
pos = nx.get_node_attributes(G, 'coords')
nx.draw_networkx_nodes(G,pos, node_color='#6FCC9F', node_size=20)
nx.draw_networkx_edges(G,pos, edge_color= "#B0B0B0", arrows=False)
plt.title("Toy model network for testing algorithms")
plt.axis("off")
plt.savefig("test/toy_test/toy_network.png")
plt.close()

# Percolate the network : 
clusterer = Percolation()
clusterer.percolate(G)

# Display the linkage tree :
clusterer.linkage_tree.plot()
plt.savefig("test/toy_test/toy_percolation_tree.png")
plt.close()

print("\n \n \n")

# Extract clusters at a threshold : 
treshold = 2.5
clustering = clusterer.linkage_tree.label_of_cut(treshold)
print(f"Membership table of the clustering with treshold {treshold} :")
print(clustering.mem_tab)
print(f"Sizes of the clusters with treshold {treshold} :")
print(clustering.size_tab)
clustering.add_clusters_to_graph(G)

# Display the clusters : 
