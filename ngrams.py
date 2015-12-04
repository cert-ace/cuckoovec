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

# extract 1-gram,2-gram ... up to ngrams
def cum_ngrams(seq, t=1e-5):  
  l = len(seq)
  tmp = seq[l-1].copy()
  out = seq[l-1].copy()
  
  for i in range(l-2,-1,-1):
    tmp2 = {}
    
    for i1,i2 in itertools.product(seq[i].items(),tmp.items()):
      w = i1[1] * i2[1]
      if w >= t:
        tmp2[i1[0]+i2[0]] = w

    tmp = tmp2        
    out.update(tmp2)
  return out
  
if __name__ == "__main__":
  s1 = [randsparse(t) for i in range(n)]
  s2 = [randsparse(t) for i in range(n)]
  t1 = ngrams(s1)
  print(t1)
  t2 = ngrams(s2)
  v1 = CuckooVector(t1)
  v2 = CuckooVector(t2)

  # these should be close to orthogonal.
  print(v1.dot(v2))
