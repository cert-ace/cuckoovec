# Primitive (type-munged) interface to cuckoo hash map

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair


cdef extern from "libcuckoo/src/cuckoovector.hh":
  cdef cppclass CityHasher[Key]:
    const size_t operator()(const Key&)
  
  cdef cppclass cuckoovector:
    cppclass locked_table:
        cppclass templated_iterator:
            pair[const string, double] operator*()
            templated_iterator operator++()
            bool operator==(templated_iterator)
            bool operator!=(templated_iterator)
        templated_iterator begin()
        templated_iterator end()
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
    const bool find(const string&, double&)  
    #const double find (const string&)  
    const bool contains(const string&)  
    bool insert[V](const string&, V&&) 
    bool erase (const string&) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type  
    #bool update(const string&, const double&)   
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, bool>::type 
    #bool update_fn[Updater] (const string&, Updater) 
    #std::enable_if<std::is_convertible<Updater, updater_type>::value, void>::type
    #void upsert[Updater, V](const string&, Updater, V) 
    bool rehash (size_t) 
    bool reserve (size_t) 
    #const Hash hash_function()  
    #const key_equal key_eq ()
    #reference  operator[] (const string&) 
    #const const_reference  operator[] (const string&)  
    void purge() 
    locked_table lock_table()