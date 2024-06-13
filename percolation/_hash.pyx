import numpy as np
cimport numpy as np

cdef class HashTable(object):
    """A Hash table is needed to store identifiers for all nodes
    """

    def __init__(self, int N):
        self.size = N
        self.tab = np.full(N, -1, dtype = np.int_)


    cdef int hash_fun(self, long key):
        # Hash function may be improved using universal hash?
        return key%self.size


    cdef int value_of_key(self, long key):
        cdef int i 
        cdef int start_indice

        i = self.hash_fun(key)
        start_indice = i

        while self.tab[i] != key:
            i+=1
            if i == start_indice:
                raise ValueError(f"Key {key} is not present in hash table")
        return i


    cdef long key_of_value(self, int value):
        if self.tab[value] != -1 :
            return self.tab[value]
        else :
            raise ValueError(f"No key has value {value}")
    

    cdef int add(self,long key):
        cdef int i
        cdef int start_indice
        
        i = self.hash_fun(key)
        start_indice = i 

        while self.tab[i] != -1:
            i+=1
            if i == start_indice:
                raise ValueError(f"The hash table is full")
        
        self.tab[i] = key
        return i

