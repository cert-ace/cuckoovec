# distutils: language = c++
# distutils: sources = libcuckoo/src/cuckoovector.hh
# Slow (single-threaded, cache-busting) and not-particularly-numerically-stable implementation of cuckoo linear algebra.
# floats indexed by size_t's

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.string cimport string
from libcpp cimport bool
from libcpp.pair cimport pair
from libcuckoo cimport cuckoovector

cdef class CuckooVector:
  cdef cuckoovector *vec;
  
  def __cinit__(self):
    self.vec = new cuckoovector()
	
  def __dealloc__(self):
    del self.vec
	
  def __init__(self, dict m):
    for k,v in m.iteritems():
      s = bytes(k, encoding='UTF-8')
      self.vec.inserts(s, v)

  def norm(self, int p):
    return self.vec.norm(p)

  def dot(self, CuckooVector v):
    return self.vec.dot(v.vec)
#
#  def add(self, a, CuckooVector v):
#    return self.vec.add(a, v.vec)
        
#    def __iter__(self):
#        cdef veciterator entry = self.map.begin()
#        cdef pair[const string, double] kv; 
#        while entry != self.map.end():
#            kv = deref(entry)
#            yield kv
#            inc(entry)