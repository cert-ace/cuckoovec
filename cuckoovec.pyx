# Slow (single-threaded, cache-busting) and not-particularly-numerically-stable implementation of cuckoo linear algebra.
# floats indexed by size_t's

from __future__ import division
from cython.operator cimport preincrement as inc
cimport numpy as np
from libcuckoo cimport cuckoohash_map
from libcpp.string cimport string

cdef class CuckooVector:
    cdef cuckoohash_map[string, np.float64_t] *map;

    def __cinit__():
        self.map = new cuckoohash_map[string, np.float64_t]()
        
    def __dealloc__(self):
        del self.map

    # Entries are kvpairs with members first:size_t and second:np.float64_t
    def __iter__(self):
        return self.map.lock_table()
        #cdef locked_table iter = self.map.lock_table()
        #cdef entry = iter.begin()
        #while (entry != iter.end()):
        #    yield entry
        #    inc(entry)
        #del iter
        
    def norm(int p):
        cdef np.float64_t nrm = 0
        for entry in self:
            nrm = nrm + abs(entry.second)^p
        return nrm
                
    def dot_naive(CuckooVector v):
        cdef np.float64_t dt = 0.0
        cdef np.float64_t vj
        for entry in self: 
            if v.find(entry.first, &vj):
                dt = dt + entry.second*vj
        return dt
            
    def add_naive(a, CuckooVector v):
        cdef np.float64_t vj
        for entry in self: 
            entry.second = a * entry.second
            if v.find(entry.first, &vj):
                entry.second = entry.second + vj 
            