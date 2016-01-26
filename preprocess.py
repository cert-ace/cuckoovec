import os, sys, glob
import numpy as np
import struct
from ngrams import cum_ngrams

# 30 frames a second?
def frame_to_index(f):
  n = [int(s) for s in f.split(':')]
  return n[0]*30^2 + n[1]*30 + n[2]
  
def filterByAbsRowSum(data, t):
  return data[np.array([np.sum(np.abs(row)) > t for row in data])]

# Create seperate feature for positive and negative deltas.
def sepSign(data):
  Tpos = data.copy()
  Tneg = -data.copy()
  p = Tpos.ravel()
  p[np.where(p < 0.0)] = 0.0
  n[np.where(n < 0.0)] = 0.0
  return np.hstack((p,n))

def stringify_row(row):
  out = {}
  idx = np.where(row > 0)[0]
  for (i,x) in zip(idx,row[idx]):
    out['+'+str(i)] = x

  idx = np.where(row < 0)[0]
  for (i,x) in zip(idx,row[idx]):
    out[str(-i)] = -x

  # null-word to capture shorter n-grams
  #out['_'] = 1.0
    
  return out
    
# Convert a sparse matrix to a list of strings. Each row is replaced with
# a string representing non-zero coordinates.
def stringify(data):
  return [stringify_row(x) for x in data]

def extract_ngrams(sdata, n, threshold):  
  l = len(sdata)-n
  out = [None] * l

  for i in range(l):
    print(i)
    out[i] = cum_ngrams(sdata[i:i+n], threshold)

  return out
  
  #return [cum_ngrams(sdata[i:i+n]) for i in range(len(sdata)-n)]
