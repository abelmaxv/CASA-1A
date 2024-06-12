cdef class UnionFind(object):

    def __init__(self, N):
        self.parent = np.full(2 * N - 1, -1., dtype=np.intp, order='C')
        self.next_label = N
        self.size = np.hstack((np.ones(N, dtype=np.intp),
                               np.zeros(N - 1, dtype=np.intp)))

    cdef void union(self, intp_t m, intp_t n):
        self.parent[m] = self.next_label
        self.parent[n] = self.next_label
        self.size[self.next_label] = self.size[m] + self.size[n]
        self.next_label += 1
        return

    #Allow negarive indices
    @cython.wraparound(True) 
    cdef intp_t fast_find(self, intp_t n):
        cdef intp_t p
        p = n
        # find the highest node in the linkage graph so far
        while self.parent[n] != -1:
            n = self.parent[n]
        # provide a shortcut up to the highest node
        while self.parent[p] != n:
            p, self.parent[p] = self.parent[p], n
        return n