import os, sys, glob
import numpy as np
import matplotlib.pyplot as plt
import struct

from scipy.misc import imsave

def delta(m1, m2):
  return [v2-v1 for v1,v2 in zip(m1,m2)]

def deltas(M): 
  return [delta(m1,m2) for m1,m2 in zip(M[:],M[1:])] 
  
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
  
folder = sys.argv[1]
T = readDetections(folder)
D = deltas(T)
A = np.asmatrix(D)

x = ['-1', '0', '1e-10', '1e-08', '1e-06', '1e-05', '1e-4', '1e-3',
     '0.01', '0.1', '1.0', '10.0']

y = [A[np.array([np.sum(np.abs(row)) > float(xx) for row in A])].shape[0]
     for xx in x]

#print(y)

threshold = -1
A = A[np.array([np.sum(np.abs(row)) > threshold for row in A])]

print(A.shape)
imsave('deltas.png', A)

plt.figure()
plt.plot(y, '-x')
plt.xticks(np.arange(len(y)), x)
plt.savefig('graph.png')
