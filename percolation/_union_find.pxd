import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind:
    cdef long next_label
    cdef long[:] parent
    cdef long[:] size

    cdef void union(self, long m, long n) 
    cdef long fast_find(self, long n)