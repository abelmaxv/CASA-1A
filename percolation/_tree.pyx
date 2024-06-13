import numpy as np
cimport numpy as np

HIERARCHY_dtype = np.dtype([
    ("left_node", np.intp),
    ("right_node", np.intp),
    ("value", np.float64),
    ("cluster_size", np.intp)
])