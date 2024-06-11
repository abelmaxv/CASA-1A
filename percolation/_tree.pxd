# Inspired from HDBSCAN implementation in skitlearn

cimport numpy as cnp

# Data type to construct tree in the percolation method
# packed is used to occupie less empty memory
ctypedef packed struct HIERARCHY_t : 
    intp_t left_node
    intp_t right_node
    float64_t value 
    intp_t cluster_size


