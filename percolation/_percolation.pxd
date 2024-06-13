cimport numpy as np
import numpy as np

from _union_find cimport UnionFind 
import _graph
cimport _graph
import _tree
cimport _tree

cdef _tree.HIERARCHY_t[:] percolation_on_graph(_graph.edge_t[:] graph)