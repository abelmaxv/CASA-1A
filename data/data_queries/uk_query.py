import pandas as pd
from IPython.display import display
import networkx as nx

raw_edge_path = "data/raw_data/uk_edges.tsv"
raw_node_path = "data/raw_data/uk_nodes.csv"

edge_path = "data/data/networks/uk.csv"
node_path = "data/data/networks/uk_nodes.csv"

# Importing the data : 
print("Importing the data ... \n")
edge_columns = ["source", "target", "length"]
edge_df = pd.read_csv(raw_edge_path, delimiter= "\t", names = edge_columns )
display(edge_df)

node_df = pd.read_csv(raw_node_path)
node_df = node_df[["TOID", "POINT_X", "POINT_Y"]]
node_df.rename({"TOID": "node", "POINT_X" : "x_coord", "POINT_Y": "y_coord"}, inplace = True, axis = 1)
display(node_df)

# Convert into a graph 
print("Converting into a graph ... \n")
G = nx.from_pandas_edgelist(edge_df, edge_attr="length")

# Extracting the largest CC
print("Extracting the largest CC ... \n")
largest_cc = max(nx.connected_components(G), key=len)
G = G.subgraph(largest_cc)

# Converting into a pandas DataFrame
print("Converting to pandas DataFrame ... \n")
edge_df = nx.to_pandas_edgelist(G)
display(edge_df)

# Relabelling the nodes
print("Relabelling the nodes in the edge DataFrame ... \n ")
node_set = set(edge_df["source"])
node_set.update(edge_df["target"])
node_to_id = {node : id for id, node in enumerate(node_set)}

edge_df["source"] = edge_df["source"].apply(lambda x: node_to_id[x])
edge_df["target"] = edge_df["target"].apply(lambda x: node_to_id[x])

display(edge_df)

print("Relabelling nodes in node DataFrame... \n")
node_df["node"] = node_df["node"].apply(lambda x : node_to_id[x] if x in node_set else None)
node_df = node_df.dropna(subset=["node"]).astype({"node": int}) 
display(node_df)

# Saving the DataFrames
print("Saving the DataFrames ... \n")
edge_df.to_csv(edge_path, index = False)
node_df.to_csv(node_path, index = False)