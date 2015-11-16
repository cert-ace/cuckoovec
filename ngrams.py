from cuckoovec import CuckooVector
import numpy as np
import itertools
import string

vocab = [c for c in string.ascii_uppercase + string.ascii_lowercase]  # letters
n = 5 
t = 2

# form random sparse vectors from <= t random words and weights 
def randsparse(t):
  return dict(zip(np.random.choice(vocab, t), np.random.randn(t)))
  
# form n-gram vector from a sequence of n vectors
# weight of each n-gram is product of weights of constituent words   
def ngrams(seq):
  grams = list(itertools.product(*[vec.keys() for vec in seq]))
  weights = [np.product([vec[w] for vec,w in zip(seq, gram)]) for gram in grams]
  return dict(zip([''.join(gram) for gram in grams], weights))
   
s1 = [randsparse(t) for i in range(n)]
s2 = [randsparse(t) for i in range(n)]
t1 = ngrams(s1)
print(t1)
t2 = ngrams(s2)
v1 = CuckooVector(t1)
v2 = CuckooVector(t2)

# these should be close to orthogonal.
print(v1.dot(v2))