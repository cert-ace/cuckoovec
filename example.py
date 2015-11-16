from cuckoovec import CuckooVector
import numpy as np
import itertools

def randsparse(d, t):
  m = {}
  for _ in itertools.repeat(None, t):
    k = str(np.random.randint(0, d))
    m[k] = (m.get(k) or 0.0) + np.random.rand()
  return m
  
def densify(m, d):
  a = np.zeros([d])
  for k,v in iter(m.items()):
    a[int(k)] = v
  return a    
  
# Evaluate accuracy of low-dimensional linear algebra operations

d = 10000000 # high dimension
t = 500000 # number of actual features 

m1 = randsparse(d, t)
m2 = randsparse(d, t)
v1 = densify(m1, d)
v2 = densify(m2, d)
cv1 = CuckooVector(m1)
cv2 = CuckooVector(m2)
  
print("2-norms: ")
print(np.linalg.norm(v1))
print(cv1.norm(2))
print(np.linalg.norm(v2))
print(cv2.norm(2))

print("dots: ")
print(np.dot(v1,v2))
print(cv1.dot(cv2))

v1 = v1 + v2
cv1.add(cv2)
print("2-norm of sums: ")
print(np.linalg.norm(v1))
print(cv1.norm(2))
dist = 0
for k in set().union(m1, m2):
  dist = dist + (abs(v1[int(k)] - cv1[k])) 
print("1-distance between sums: ")
print(dist)