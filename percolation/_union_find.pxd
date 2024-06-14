import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind:
    cdef long[:] parent_arr
    cdef int[:] size_arr
    cdef long next_label


    cdef void union(self, long m, long n) 
    cdef long fast_find(self, long n)