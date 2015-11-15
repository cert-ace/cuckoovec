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
		
		double find(std::string k) { 
			double v = 0.0;
			cuckoohash_map::find(k, v);
			return v;
		}
		
		double norm(int p) {
			double nrm = 0.0;
			auto lt = lock_table();
			for (const auto& entry : lt) {
				nrm = nrm + pow(abs(entry.second), p);
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
            
		void add(double a, cuckoovector *v) {
			auto lt = lock_table();
			for (auto& entry : lt) {
				entry.second = a * entry.second + v->find(entry.first);
			}
		}
};

#endif // _CUCKOOVECTOR_HH