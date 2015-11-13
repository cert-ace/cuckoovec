# Primitive (type-munged) interface to cuckoo hash map

from libcpp cimport bool

cdef extern from "libcuckoo/cuckoohash_map.hh" namespace "libcuckoo":
  cdef cppclass CityHasher[Key]:
    const size_t operator()(const Key&)
  
  cdef cppclass cuckoohash_map[Key, T]:
    cppclass locked_table:
        cppclass iterator
        iterator begin()
        iterator end()
        bool has_table_lock()
    
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
    const T find (const Key&)  
    const bool contains(const Key&)  
    bool insert[V](const Key&, V&&) 
    bool erase (const Key&) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type  
    bool update(const Key&, const T&)   
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type 
    bool update_fn[Updater] (const Key&, Updater) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, void>::type
    void upsert[Updater, V](const Key&, Updater, V) 
    bool rehash (size_t) 
    bool reserve (size_t) 
    #const Hash hash_function()  
    #const key_equal key_eq ()
    #reference  operator[] (const Key&) 
    #const const_reference  operator[] (const Key&)  
    void purge() 
    locked_table lock_table()