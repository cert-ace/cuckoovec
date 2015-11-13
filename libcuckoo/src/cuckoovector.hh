#ifndef _CUCKOO_VECTOR_HH
#define _CUCKOO_VECTOR_HH

#include "cuckoohash_map.hh"

class cuckoo_vector : public cuckoohash_map<std::string, double> {
public:
	cuckoo_vector() { 
		cuckoohash_map<std::string, double>();
	}
	
	~cuckoo_vector() { 
		~cuckoohash_map<std::string, double>();
	}
}

#endif // _CUCKOO_VECTOR_HH