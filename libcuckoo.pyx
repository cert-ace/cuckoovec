# distutils: language = c++
# distutils: sources = libcuckoo/src/cuckoovector.hh
# Slow (single-threaded, cache-busting) and not-particularly-numerically-stable implementation of cuckoo linear algebra.
# floats indexed by size_t's

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.string cimport string
from libcpp cimport bool
from libcpp.pair cimport pair
from libcuckoo cimport cuckoovector, cuckoomatrix, cv_locked_table, cm_locked_table

ctypedef void (*kvcallback)(string k, double v)
ctypedef cuckoovector *cuckoovector_ptr

cdef class CuckooVectorView:
  cdef cuckoovector *vec;
	
  def __setitem__(self, k, double v):
    s = bytes(k, encoding='UTF-8')
    self.vec.set(s, v)
	  
  def __getitem__(self, k):
    s = bytes(k, encoding='UTF-8')
    return self.vec.find(s)	
	  
  def norm(self, int p):
    return self.vec.norm(p)

  def dot(self, CuckooVectorView v):
    return self.vec.dot(v.vec)

  def scale(self, double a):
    self.vec.scale(a)
	
  def add(self, CuckooVectorView v):
    self.vec.add(v.vec)

  def add_scale(self, CuckooVectorView v, double vscale):
    self.vec.add_scale(v.vec, vscale)

  # Key iteration methods
  # Need to heap-allocate stuff in Cython. But Cython tries to use the default constructors,
  # which don't exist for these classes. Do weird things to forcibly heap allocate.
  # copy-and-paste versions for C callback and Python generator
  
  cdef each(self, kvcallback kvcb): 
    cdef cv_locked_table* lock = new cv_locked_table((self.vec.lock_table()))
    cdef cv_locked_table.cv_templated_iterator* iter = new cv_locked_table.cv_templated_iterator( deref(lock).begin() )
  
    while deref(iter) != deref(lock).end():
      kvcb(deref(deref(iter)).first.decode('UTF-8'), deref(deref(iter)).second)
      inc(deref(iter))

    del iter
    del lock

  def items(self): 
    cdef cv_locked_table* lock = new cv_locked_table((self.vec.lock_table()))
    cdef cv_locked_table.cv_templated_iterator* iter = new cv_locked_table.cv_templated_iterator( deref(lock).begin() )
  
    while deref(iter) != deref(lock).end():
      yield (deref(deref(iter)).first.decode('UTF-8'), deref(deref(iter)).second)
      inc(deref(iter))

    del iter
    del lock

cdef CuckooVectorView_Init(cuckoovector *v):
  cdef CuckooVectorView v_out = CuckooVectorView()
  v_out.vec = v
  return v_out

# A CuckooVector is a CuckooVectorView that also owns the underlying cuckoovector
# pointer (i.e. deletes it upon destruction)
cdef class CuckooVector(CuckooVectorView):
  def __cinit__(self):
    self.vec = new cuckoovector()

  def __init__(self, dict m):      
    for k,v in m.iteritems():
      s = bytes(k, encoding='UTF-8')
      self.vec.inserts(s, v)
	
  def __dealloc__(self):
    del self.vec

cdef class CuckooMatrix:
  cdef cuckoomatrix *mat;

  def __cinit__(self):
    self.mat = new cuckoomatrix()
	
  def __dealloc__(self):
    del self.mat

  def __setitem__(self, k, double v):
    r = bytes(k[0], encoding='UTF-8')
    c = bytes(k[1], encoding='UTF-8')
    self.mat.set(r,c,v)
	  
  def __getitem__(self, k):
    r = bytes(k[0], encoding='UTF-8')
    c = bytes(k[1], encoding='UTF-8')
    return self.mat.find(r,c)	

  def get_col(self, k):
    c = bytes(k, encoding='UTF-8')
    cdef cuckoovector *v = self.mat.get_col(c)
    if v == NULL:
      return None
    else:
      return CuckooVectorView_Init(v)

  def get_or_insert_col(self, k):
    c = bytes(k, encoding='UTF-8')
    cdef cuckoovector *v = self.mat.get_or_insert_col(c)
    return CuckooVectorView_Init(v)

  def clear(self):
    self.mat.clear()

  def add(self, CuckooMatrix m):
    self.mat.add(m.mat)

  def add_scale(self, CuckooMatrix m, double scale):
    self.mat.add_scale(m.mat, scale)

  def mult_vec(self, CuckooVectorView v):
    cdef CuckooVector v_out = CuckooVector({})
    self.mat.mult_vec(v.vec, v_out.vec)
    return v_out

  def mult(self, CuckooMatrix m):
    cdef CuckooMatrix m_out = CuckooMatrix()
    self.mat.mult(m.mat, m_out.mat)
    return m_out
    
  def columns(self): 
    cdef cm_locked_table* lock = new cm_locked_table((self.mat.lock_table()))
    cdef cm_locked_table.cm_templated_iterator* iter = new cm_locked_table.cm_templated_iterator( deref(lock).begin() )
    cdef cuckoovector *v

    while deref(iter) != deref(lock).end():
      v = deref(deref(iter)).second
      yield (deref(deref(iter)).first.decode('UTF-8'), CuckooVectorView_Init(v))
      inc(deref(iter))

    del iter
    del lock
    
