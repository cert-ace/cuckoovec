import os, sys, glob
import numpy as np
import struct
from ngrams import cum_ngrams

def delta(m1, m2):
  return [v2-v1 for v1,v2 in zip(m1,m2)]

# Converts a doubly indexed list of scores (e.g. the output of readDetections)
# to a double indexed list of score differences. 
# score_diff[t][template] = M[t+1][template]-M[t][template]
def deltas(M): 
  return [delta(m1,m2) for m1,m2 in zip(M[:],M[1:])] 
  
# Reads data from a binary result file. Returns a two dimensional list of scores.
# First dimension is the frame id. Second dimension is the template id. 
def readDetections(folder):  
  with open(folder, 'rb') as input:
    num_templates = struct.unpack('<H', input.read(2))[0]
    num_frames = struct.unpack('<I', input.read(4))[0]

    T = num_frames * [None]
    f = 0
    
    print(num_frames)
    print(num_templates)

    input.read(16)

    b = input.read(4)
    while len(b) > 0:
      T[f] = num_templates * [None]
      i = struct.unpack('<I', b)[0]
      print(i)
      for t in range(num_templates):
        T[f][t] = struct.unpack('<d', input.read(8))[0] # Read confidence
        input.read(4) # Read position      

      f += 1
      b = input.read(4)

  return T

# Removes rows from amatrix whose absolute sum is below a given threshold.
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
    
# Convert a sparse matrix to a string dictionaries. Each row is replaced with
# a dictionary representing non-zero coordinates. Dictionary key indicate whether 
# the value of the coordinate ispositive or negative.
# Example output: {'+0': 0.9, '-3': 0.5}
def stringify(data):
  return [stringify_row(x) for x in data]

# Extract ngrams up to length n from stringified data (output of stringify). 
# Each frame is represented by a string encoding a prefix of template changes.
# The "threshold" parameter is used to prune intermediate prefixes.
def extract_ngrams(sdata, n, threshold):  
  l = len(sdata)-n
  out = [None] * l

  for i in range(l):
    print(i)
    out[i] = cum_ngrams(sdata[i:i+n], threshold)

  return out
  
  #return [cum_ngrams(sdata[i:i+n]) for i in range(len(sdata)-n)]