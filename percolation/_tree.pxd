import numpy as np
cimport numpy as np
from _union_find cimport UnionFind


cpdef np.ndarray[dtype = long, ndim = 1] _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold)


