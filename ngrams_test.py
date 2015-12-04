from cuckoovec import CuckooVector
import numpy as np
import string
from ngrams import *

vocab = [c for c in string.ascii_uppercase + string.ascii_lowercase]  # letters
n = 5 
t = 2

# form random sparse vectors from <= t random words and weights 
def randsparse(t):
  return dict(zip(np.random.choice(vocab, t), np.random.randn(t)))
   
s1 = [randsparse(t) for i in range(n)]
s2 = [randsparse(t) for i in range(n)]
t1 = ngrams(s1)
print(t1)
t2 = ngrams(s2)
v1 = CuckooVector(t1)
v2 = CuckooVector(t2)

# these should be close to orthogonal.
print(v1.dot(v2))