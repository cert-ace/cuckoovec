#ifndef _CUCKOOVECTOR_HH
#define _CUCKOOVECTOR_HH

#include <cstdlib>
#include <cmath>
#include "cuckoohash_map.hh"

// Smooth over the rough bits of Cython

class cuckoovector : public cuckoohash_map<std::string, double> {	
	public:
		void inserts(std::string k, double v) {
			cuckoohash_map::insert(k, v);
		}

		void set(const std::string &k, double v) {
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
			if (this == v) return pow(norm(2),2);
			
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
			if (this == v) return scale(2);
			
			auto lt = v->lock_table();
			for (const auto& entry : lt) {
				set(entry.first, find(entry.first) + entry.second);
			}
		}

  void add_scale(cuckoovector *v, double vscale) {
			if (this == v) return scale(1.0 + vscale);
			
			auto lt = v->lock_table();
			for (const auto& entry : lt) {
				set(entry.first, find(entry.first) + vscale * entry.second);
			}
		}
};

#endif // _CUCKOOVECTOR_HH
