# Primitive (type-munged) interface to cuckoo hash map

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair

cdef extern from "libcuckoo/src/cuckoohash_map.hh":
  cdef cppclass CityHasher[Key]:
    const size_t operator()(const Key&)
    
cdef extern from "libcuckoo/src/cuckoovector.hh":	
  cppclass cv_locked_table "cuckoohash_map<std::string, double>::locked_table":
    cppclass cv_templated_iterator "templated_iterator<false>":
      cv_templated_iterator(cv_templated_iterator&&)
      pair[const string, double] operator*()
      cv_templated_iterator& operator++()
      bool operator==(cv_templated_iterator)
      bool operator!=(cv_templated_iterator)	
    cv_locked_table(cv_locked_table&&)	  
    cv_templated_iterator begin()
    cv_templated_iterator end()
    bool has_table_lock()
  
  cppclass cuckoovector:  
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
    cv_locked_table lock_table()
	
	# Cython bombs on "insert".
    void inserts(string k, double v)
    void set(string k, double v)
    double find(string k)
	
    double norm(int p)
    double dot(cuckoovector *v)
    void scale(double a)
    void add(cuckoovector *v)	