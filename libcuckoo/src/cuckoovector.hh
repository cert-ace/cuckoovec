#ifndef _CUCKOOVECTOR_HH
#define _CUCKOOVECTOR_HH

#include <cstdlib>
#include <cmath>
#include "cuckoohash_map.hh"

// Cython can't deal with default template arguments; this fills them in.
// locked_table is a private class, which complicates the Cython
// This manages all the locking for the single-threaded Python 
class cuckoovector : public cuckoohash_map<std::string, double> {	
	public:
		void inserts(std::string k, double v) {
			cuckoohash_map::insert(k, v);
		}

		void set(std::string k, double v) {
			(*this)[k] = v;
		}
		
		double find(std::string k) { 
			double v = 0.0;
			cuckoohash_map::find(k, v);
			return v;
		}
		
		double norm(int p) {
			double nrm = 0.0;
			auto lt = lock_table();
			for (const auto& entry : lt) {
				nrm = nrm + pow(fabs(entry.second), p);
			}
			return pow(nrm, 1.0/p);
        }
		
		double dot(cuckoovector *v) {
			double dt = 0.0;
			auto lt = lock_table();
			for (const auto& entry : lt) {
				dt = fma(entry.second, v->find(entry.first), dt);
			}
			return dt;
		}
            
		void scale(double a) {
			auto lt = lock_table();
			auto iter = lt.begin();
			while (iter != lt.end()) {
				auto entry = *iter;
				iter->second = a * iter->second;
				iter++;
			}
		}
			
		void add(cuckoovector *v) {
			auto lt = v->lock_table();
			for (const auto& entry : lt) {
				set(entry.first, find(entry.first) + entry.second);
			}
		}
};

#endif // _CUCKOOVECTOR_HH