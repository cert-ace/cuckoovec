import os, sys, glob
import numpy as np
import matplotlib.pyplot as plt
import struct

from preprocess import *

from scipy.misc import imsave
  
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
A = filterByAbsRowSum(A, threshold)

print(A.shape)
imsave('deltas.png', A)

plt.figure()
plt.plot(y, '-x')
plt.xticks(np.arange(len(y)), x)
plt.savefig('graph.png')
