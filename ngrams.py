import itertools
import numpy as np

def cartesian(seq, grams):
  weights = [np.product([vec[w] for vec,w in zip(seq, gram)]) for gram in grams]
  return dict(zip([''.join(gram) for gram in grams], weights))
  
# form n-gram vector from a sequence of n vectors, each sparsely represented as a dict
# weight of each n-gram is product of weights of constituent words   
def ngrams(seq):
  grams = list(itertools.product(*[vec.keys() for vec in seq]))
  return cartesian(seq, grams)
  
# like above, except for arrays, not dicts.
def ngrams_arr(seq):
  grams = list(itertools.product(*[range(len(vec)) for vec in seq]))
  weights = [np.product([vec[w] for vec,w in zip(seq, gram)]) for gram in grams]
  return dict(zip([''.join(str(gram)) for gram in grams], weights))  