cimport numpy as np

ctypedef packed struct edge_t :
    int64_t first_node
    int64_t second_node
    float64_t distance