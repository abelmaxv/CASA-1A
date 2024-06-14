import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind:
    cdef long[:] parent
    cdef int[:] _size

    cdef void union(self, long m, long n) 
    cdef long fast_find(self, long n)
    cdef int size(self, long n)