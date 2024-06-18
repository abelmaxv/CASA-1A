import numpy as np
cimport numpy as np
from ._union_find cimport UnionFind


cdef tuple clean_memb_tab(long[:] memb_tab_temp)
cpdef tuple _label_of_cut(np.ndarray[dtype = double, ndim = 2] linkage_matrix, double threshold)


