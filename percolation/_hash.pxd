cdef class HashTable:
    
    cdef long[:] tab
    cdef int size
    
    cdef int hash_fun(self,long key) 
    cdef int value_of_key(self,long key)
    cdef long key_of_value(self,int value)
    cdef int add(self,long key)
