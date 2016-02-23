import itertools
import numpy as np

def cartesian(seq, grams):
  weights = [np.product([vec[w] for vec,w in zip(seq, gram)]) for gram in grams]
  return dict(zip([','.join(gram) for gram in grams], weights))
  
# form n-gram vector from a sequence of n vectors,
# each sparsely represented as a dict
# weight of each n-gram is product of weights of constituent words   
def ngrams(seq):
  grams = list(itertools.product(*[vec.keys() for vec in seq]))
  return cartesian(seq, grams)
  
# like above, except for arrays, not dicts.
def ngrams_arr(seq):
  grams = list(itertools.product(*[range(len(vec)) for vec in seq]))
  weights = [np.product([vec[w] for vec,w in zip(seq, gram)]) for gram in grams]
  return dict(zip([''.join(str(gram)) for gram in grams], weights))

# extract backward 1-gram,2-gram ... up to ngrams. Backward
# ngrams are extracted from the end of the sequence (e.g. 1-grams
# are extracted from the last time step).
def cum_ngrams(seq, t=1e-5):  
  l = len(seq)
  tmp = seq[l-1].copy()
  out = seq[l-1].copy()
  
  for i in range(l-2,-1,-1):
    tmp2 = {}
    
    for i1,i2 in itertools.product(seq[i].items(),tmp.items()):
      w = i1[1] * i2[1]
      if w >= t:
        tmp2[i1[0]+','+i2[0]] = w

    tmp = tmp2        
    out.update(tmp2)
  return out

# same as above, but for arrays
def cum_ngrams_arr(seq, t=1e-5):
  return cum_ngrams([{str(k): l[k] for k in range(len(l))} for l in seq])

# extract forward 1-gram,2-gram ... up to ngrams. Backward
# ngrams are extracted from the end of the sequence (e.g. 1-grams
# are extracted from the first time step).
def cum_fwd_ngrams(seq, t=1e-5):  
  l = len(seq)
  tmp = seq[0].copy()
  out = seq[0].copy()
  
  for i in range(1,l):
    tmp2 = {}
    
    for i1,i2 in itertools.product(seq[i].items(),tmp.items()):
      w = i1[1] * i2[1]
      if w >= t:
        tmp2[i2[0]+','+i1[0]] = w

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
