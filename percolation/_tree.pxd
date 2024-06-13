import numpy as np
cimport numpy as np

ctypedef packed struct HIERARCHY_t : 
    int left_node
    int right_node
    double value 
    int cluster_size


