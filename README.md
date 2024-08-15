# NetHDBSCAN

This library provides a graph clustering algorithm inspired by HDBSCAN.

## Installation

To install the python package, run the following command 

````
pip install NetHDBSCAN
````

## Usage

The library is separated into two subpackages that both contain classes : 

- subpackage ``percolation`` contains ````Percolation````
- subpackage ``structure`` contains ````Clustering````, ````CondensedTree```` and ````LinkageTree````
 
These classes can be imported with the following script :

`````python
from NetHDBSCAN.percolation import Percolation
from NetHDBSCAN.structures import Clustering, CondensedTree, LinkageTree
`````

The algorithm can operate on a [networkx](https://networkx.org/documentation/stable/index.html) graph structure or a [pandas](https://pandas.pydata.org/) data frame that contains edge list. 

>[!IMPORTANT]
>It is important to format the network so that it is undirected and vertices are labeled 0, ..., n-1 where n is ther number of vertices. 

Although a complete documentation (soon) is available, the next section provides a basic use case of the algorithm.

## Basic Example

The following is a standard use case of the library. More can be found in the [test directory](tests/).

- Import the required libraries :
`````python
from NetHDBSCAN.percolation import Percolation
from NetHDBSCAN.structures import Clustering, CondensedTree, LinkageTree
import networkx as nx
import osmnx as ox
`````

- Import a city network with a OpenStreetMap query and format the network: 
````python
G = ox.graph_from_place("Meudon, France", network_type = "drive", simplify = True)
G = nx.convert_node_labels_to_integers(G)
G = G.to_undirected()
````

- Create the linkage tree with the percolation algorithm :
````python 
clusterer = Percolation()
clusterer.percolate(G)
percolation_tree = clusterer.linkage_tree
````

- Build the condensed tree with a ````min_size```` parameter : 
````python
min_size = 20 
condensed_tree = percolation_tree.compute_condensed_tree(min_size=min_size)
````

- Extract clusters by optimizing stability : 
`````python 
clustering = condensed_tree.label_of_stability()
`````

- Display the obtained clustering : 
````python
node_colors = clustering.get_node_colors()
ox.plot.plot_graph(G, node_color = node_colors, edge_color = "#B0B0B0", bgcolor = '#FFFFFF')
