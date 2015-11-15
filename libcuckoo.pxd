# Primitive (type-munged) interface to cuckoo hash map

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair

cdef extern from "<iterator>" namespace "std" nogil:
  cdef cppclass iterator[Tag, T]:
    T operator*()
    iterator[Tag, T] operator++()
    bool operator==(iterator)
    bool operator!=(iterator)   	
  cdef cppclass bidirectional_iterator_tag
	
cdef extern from "libcuckoo/src/cuckoohash_map.hh":
  cdef cppclass CityHasher[Key]:
    const size_t operator()(const Key&)
  
  
  cdef cppclass cuckoohash_map[Key, T, Hash, Pred, Alloc, SLOT_PER_BUCKET]:
#    cppclass locked_table:
#      iterator[bidirectional_iterator_tag, pair[const Key&, T]] begin()
#      iterator[bidirectional_iterator_tag, pair[const Key&, T]] end()
#      bool has_table_lock()
#        cppclass templated_iterator:
#            pair[const string, double] operator*()
#            templated_iterator operator++()
#            bool operator==(templated_iterator)
#            bool operator!=(templated_iterator)
           
    cuckoohash_map() except +    
    cuckoohash_map(size_t, double, size_t) except +
    void clear()
    size_t size()
    bool empty()
    const size_t hashpower()  
    const size_t bucket_count()  
    const double load_factor()  
    void minimum_load_factor(const double) 
    double minimum_load_factor() 
    void maximum_hashpower(size_t) 
    size_t maximum_hashpower() 
    const bool find(const Key&, T&)  
    #const T find (const Key&)  
    const bool contains(const Key&)  
    bool insert[V](const Key&, V&&) 
    bool erase (const Key&) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type  
    #bool update(const Key&, const double&)   
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type 
    #bool update_fn[Updater] (const Key&, Updater) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, void>::type
    #void upsert[Updater, V](const Key&, Updater, V) 
    bool rehash (size_t) 
    bool reserve (size_t) 
    #const Hash hash_function()  
    #const key_equal key_eq ()
    #reference  operator[] (const Key&) 
    #const const_reference  operator[] (const Key&)  
    void purge() 
    #locked_table lock_table()

cdef extern from "libcuckoo/src/cuckoovector.hh":	
  cdef cppclass cuckoovector:
    cuckoovector() except +    
    void clear()
    size_t size()
    bool empty()
    const size_t hashpower()  
    const size_t bucket_count()  
    const double load_factor()  
    void minimum_load_factor(const double) 
    double minimum_load_factor() 
    void maximum_hashpower(size_t) 
    size_t maximum_hashpower() 
    const bool find(const string&, double&)  
    #const T find (const Key&)  
    const bool contains(const string&)  
    #bool insert[V](const string&, V&&)
    bool insert(const string&, double&&)	
    bool erase (const string&) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type  
    #bool update(const Key&, const double&)   
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type 
    #bool update_fn[Updater] (const Key&, Updater) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, void>::type
    #void upsert[Updater, V](const Key&, Updater, V) 
    bool rehash (size_t) 
    bool reserve (size_t) 
    #const Hash hash_function()  
    #const key_equal key_eq ()
    #reference  operator[] (const Key&) 
    #const const_reference  operator[] (const Key&)  
    void purge() 
    #cuckoohash_map.locked_table lock_table()
	
	# Cython bombs on "insert".
    void inserts(string k, double v)
    double find(string k)
    double norm(int p)
	
	# Cython/cpp can't handle pointer dereferencing.
    double dot(cuckoovector *v)
    void add(double a, cuckoovector *v)
	
#  cdef cppclass veciterator:
#    pair[const string, double] operator*()
#    veciterator operator++()
#    bool operator==(veciterator)
#    bool operator!=(veciterator)