def delta(m1, m2):
  d = {}
  for k in set().union(m1, m2):
    v1,v2 = [m[k] or 0 for m in [m1,m2]]
    if v1 != v2: # maybe threshold
      d[k] = v2 - v1
  return d

def deltas(M): 
  return [delta(m1,m2) for m1,m2 in zip(M[:],M[1:])] 