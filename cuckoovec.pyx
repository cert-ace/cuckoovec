# Slow (single-threaded, cache-busting) and not-particularly-numerically-stable implementation of cuckoo linear algebra.
# floats indexed by size_t's

from __future__ import division
from cython.operator cimport dereference as deref, preincrement as inc
from libcuckoo cimport cuckoovector
from libcpp.string cimport string
from libcpp cimport bool

cdef class CuckooVector:
    cdef cuckoovector *map;

    def __cinit__(self):
        self.map = new cuckoovector()
        
    def __dealloc__(self):
        del self.map

    # Entries are kvpairs with members first:size_t and second:np.float64_t
    def __iter__(self):
        cdef cuckoovector.locked_table iter = self.map.lock_table()
        cdef cuckoovector.locked_table.templated_iterator entry = iter.begin()
        while (entry != iter.end()):
            yield deref(entry)
            inc(entry)
        
    def norm(self, int p):
        cdef double nrm = 0.0
        for entry in self:
            nrm = nrm + abs(entry.second)^p
        return nrm
                
    def dot_naive(self, CuckooVector v):
        cdef double dt = 0.0
        cdef double vj = 0.0
        for entry in self: 
            if v.map.find(entry.first, vj):
                dt = dt + entry.second*vj
        return dt
            
    def add_naive(self, a, CuckooVector v):
        cdef double vj = 0.0
        for entry in self: 
            entry.second = a * entry.second
            if v.map.find(entry.first, vj):
                entry.second = entry.second + vj 
            