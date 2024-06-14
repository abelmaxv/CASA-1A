import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind(object):

    def __init__(self, N):
        self.parent = np.array(list(range(N)), dtype = np.int_)
        self._size = np.ones(N, dtype=np.intc)

    #Allow negative indices
    @cython.wraparound(True)
    cdef long fast_find(self, long n):
        cdef long p
        p = n
        # find the highest node in the linkage graph so far
        while self.parent[n] != n:
            n = self.parent[n]
        # provide a shortcut up to the highest node
        while self.parent[p] != n:
            p, self.parent[p] = self.parent[p], n
        return n

    cdef int size(self, long n):
        return self._size[self.fast_find(n)]


    cdef void union(self, long m, long n):
        pn = self.fast_find(n)
        pm = self.fast_find(m)
        if self._size[pn] < self._size[pm]:
            pn, pm = pm, pn
        self.parent[pm] = pn
        self._size[pn] = self._size[pn] + self._size[pm]
        return