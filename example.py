print("a")
from cuckoovec import CuckooVector
import numpy as np
import itertools

def randsparse(d = 10000, t = 5):
  m = {}
  for _ in itertools.repeat(None, t):
    k = str(np.random.randint(0, d))
    m[k] = (m.get(k) or 0.0) + np.random.rand()
  return m
  
def densify(m, d = 10000):
  a = np.array(d)
  for k,v in iter(m.items()):
    a[int(k)] = v
  return a    
  
# Evaluate accuracy of low-dimensional linear algebra operations

print("fish")
m1 = randsparse()
m2 = randsparse()
print(m1)
v1 = densify(m1)
v2 = densify(m2)
cv1 = CuckooVector(m1)
cv2 = CuckooVector(m2)
print(v1.dot(v2))
print(cv1.dot(cv2))
