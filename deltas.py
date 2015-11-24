import os, sys, glob
import numpy as np

from scipy.misc import imsave

def delta(m1, m2):
  d = {}
  for k in set().union(m1, m2):
    v1,v2 = [m[k] or 0 for m in [m1,m2]]
    if v1 != v2: # maybe threshold
      d[k] = v2 - v1
  return d

def deltas(M): 
  return [delta(m1,m2) for m1,m2 in zip(M[:],M[1:])] 
  
def readDetections(folder):
  T = {}
  for name in glob.glob(folder + '/result_*.txt'):
    i = name.split('_')[1].split('.')[0]
    print(i)
    with open(os.path.join(folder, name)) as file:
      T[int(i)] = {chunks[3]: float(chunks[0]) for chunks in [line.split('\t') for line in file if line]}
  return T
  

folder = sys.argv[1]
T = readDetections(folder)
M = [v for (i,v) in sorted(T.items())]
templateNames = set().union(*M)
D = deltas(M)
A = np.asmatrix([[d.get(name) or 0 for name in templateNames] for d in D])
#A = np.array()
imsave('deltas.png', A)
