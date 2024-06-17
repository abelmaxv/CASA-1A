import numpy as np
cimport numpy as np

cimport cython

cdef class UnionFind(object):

    def __init__(self, N):
        self.parent_arr = -1 * np.ones(2 * N - 1, dtype=np.int_, order='C')
        self.next_label = N
        self.size_arr = np.hstack((np.ones(N, dtype=np.intc),
                                   np.zeros(N-1, dtype=np.intc)))


    cdef void union(self, long m, long n):
        if n != m :
            self.size_arr[self.next_label] = self.size_arr[m] + self.size_arr[n]
            self.parent_arr[m] = self.next_label
            self.parent_arr[n] = self.next_label
            self.next_label += 1
        return

    cdef long fast_find(self, long n):
        #cdef long p
        #p = n
        while self.parent_arr[n] != -1:
            n = self.parent_arr[n]
        # label up to the root
        #while self.parent_arr[p] != n:
            #self.parent_arr[p]=n
            #p = self.parent_arr[p]
        return n