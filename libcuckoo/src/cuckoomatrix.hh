#ifndef _CUCKOOMATRIX_HH
#define _CUCKOOMATRIX_HH

#include <cstdlib>
#include <cmath>
#include <memory>
#include "cuckoohash_map.hh"
#include "cuckoovector.hh"

// A matrix indexed by a pair of keys
class cuckoomatrix : public cuckoohash_map<std::string, cuckoovector*> {	
public:
  ~cuckoomatrix() {
    free_memory();
  }

  cuckoovector *get_col(const std::string &k_col) {
    cuckoovector *v = 0;    
    cuckoohash_map::find(k_col, v);
    return v;
  }
  
  cuckoovector *get_or_insert_col(const std::string &k_col) {
    cuckoovector *v;
    
    if (!cuckoohash_map::find(k_col, v)) {
      v = new cuckoovector;
      cuckoohash_map::insert(k_col, v);
    }

    return v;
  }

  void inserts(const std::string &k_row, const std::string &k_col, double v) {
    cuckoovector *c = get_or_insert_col(k_col);
    c->inserts(k_row, v);
  }

  void set(const std::string &k_row, const std::string &k_col, double v) {
    cuckoovector *c = get_or_insert_col(k_col);
    (*c)[k_row] = v;
  }
		
  double find(const std::string &k_col, const std::string &k_row) {
    cuckoovector *c;
    if(cuckoohash_map::find(k_col, c)) {
      return c->find(k_row);
    } else {
      return 0.0;
    }
  }

  void clear() {
    free_memory();
    cuckoohash_map::clear();
  }
  
  void scale(double a) {
    auto lt = lock_table();
    auto iter = lt.begin();
    while (iter != lt.end()) {
      auto entry = *iter;
      iter->second->scale(a);
      iter++;
    }
  }
			
  void add(cuckoomatrix *m) {
    if (this == m) return scale(2);
			
    auto lt = m->lock_table();
    for (const auto& entry : lt) {
      cuckoovector *c = get_or_insert_col(entry.first);
      c->add(entry.second);
    }
  }

  void add_scale(cuckoomatrix *m, double mscale) {
    if (this == m) return scale(1.0 + mscale);
			
    auto lt = m->lock_table();
    for (const auto& entry : lt) {
      cuckoovector *c = get_or_insert_col(entry.first);
      c->add_scale(entry.second, mscale);
    }
  }

  void mult(cuckoomatrix *m, cuckoomatrix *out) {
    out->clear();

    auto lt = m->lock_table();
    for (const auto& entry : lt) {
      cuckoovector *c = new cuckoovector();
      m->insert(entry.first, c);
      mult_vec(entry.second, c);
    }    
  }
  
  void mult_vec(cuckoovector *v, cuckoovector *out) {
    out->clear();

    auto lt = v->lock_table();
    for (const auto& entry : lt) {
      cuckoovector *col;
      if (cuckoohash_map::find(entry.first, col)) {
	out->add_scale(col, entry.second);
      }
    }
  }

private:
  void free_memory() {
    auto lt = lock_table();
    for (auto& entry : lt) {
      delete entry.second;
    }    
  }
};

#endif // _CUCKOOVECTOR_HH
