import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)




fig, ax = ox.plot_graph(G,
                        bgcolor= 'w',
                        node_color='k',
                        node_size = 10)


stats = ox.basic_stats(G)
print(stats)
print(type(G))