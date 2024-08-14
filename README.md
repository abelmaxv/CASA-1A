# NetHDBSCAN

This library provides a graph clustering algorithm inspired by HDBSCAN.

## Installation

To install the python package, run the following command 

````
pip install NetHDBSCAN==0.0.1
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

Although [a complete documentation]() available, the next section provides a basic use case of the algorithm.

