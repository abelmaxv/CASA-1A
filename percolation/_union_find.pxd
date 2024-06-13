import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind:
    cdef int next_label
    cdef int[:] parent
    cdef int[:] size

    cdef void union(self, int m, int n) 
    cdef int fast_find(self, int n)