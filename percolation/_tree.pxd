import numpy as np
cimport numpy as np

ctypedef packed struct HIERARCHY_t : 
    long left_node
    long right_node
    float value 
    int cluster_size


