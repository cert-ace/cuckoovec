# distutils: language = c++
# distutils: sources = libcuckoo/src/cuckoovector.hh
# Slow (single-threaded, cache-busting) and not-particularly-numerically-stable implementation of cuckoo linear algebra.
# floats indexed by size_t's

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.string cimport string
from libcpp cimport bool
from libcpp.pair cimport pair
from libcuckoo cimport cuckoovector, cv_locked_table

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

  def __setitem__(self, k, double v):
    s = bytes(k, encoding='UTF-8')
    self.vec.set(s, v)
	  
  def __getitem__(self, k):
    s = bytes(k, encoding='UTF-8')
    return self.vec.find(s)	
	  
  def norm(self, int p):
    return self.vec.norm(p)

  def dot(self, CuckooVector v):
    return self.vec.dot(v.vec)

  def scale(self, double a):
    self.vec.scale(a)
	
  def add(self, CuckooVector v):
    self.vec.add(v.vec)

  # Need to heap-allocate stuff in Cython. But Cython tries to use the default constructors...
  # which don't exist for these classes. Try to forcibly heap allocate.
  def items(self): 
    cdef cv_locked_table* lock = new cv_locked_table((self.vec.lock_table()))
    cdef cv_locked_table.cv_templated_iterator* iter = new cv_locked_table.cv_templated_iterator( deref(lock).begin() )
  
    while deref(iter) != deref(lock).end():
      yield (deref(deref(iter)).first, deref(deref(iter)).second)
      inc(deref(iter))

    del iter
    del lock
  
  
	
#  def items(self):
    # can't pass C++ objects to constructors without wrapping.
#    cvi = CuckooVectorIterator()
#    cvi.iter = self.vec.items()
#    return cvi


	
#        cdef veciterator entry = self.map.begin()
#        cdef pair[const string, double] kv; 
#        while entry != self.map.end():
#            kv = deref(entry)
#            yield kv
#            inc(entry)