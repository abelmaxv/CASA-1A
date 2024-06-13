import numpy as np
cimport numpy as np

HIERARCHY_dtype = np.dtype([
    ("left_node", np.int_),
    ("right_node", np.int_),
    ("value", np.single),
    ("cluster_size", np.intc)
])