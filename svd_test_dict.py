from preprocess import *
from ngrams import *
import mat_utils_dict as mat
import numpy as np
import time
import pickle
import gzip
import sys

# N-gram length
n = 5

# # Constructing examples
# print('Preprocessing Files')
# P = [] # pasts
# F = [] # futures
# X = []

# for f in ['data/1412.bin','data/1413.bin','data/1414.bin','data/1415.bin']:
#     print(f)
#     sys.stdout.flush()
#     R = readDetections(f)
#     D = deltas(R)
#     A = np.asarray(D) #Convert to Numpy array
#     A.ravel()[np.where(np.abs(A).ravel() < 1e-3)] = 0.0 #Apply threshold to score deltas
#     [idx,T] = filterByAbsRowSum(A, 1e-3) 
#     s = stringify(T)
#     sn = extract_ngrams(s, n, 1e-4)
#     snf = extract_fwd_ngrams(s, n, 1e-4)

#     idx = idx[n:]

#     X += [(idx,sn,snf)] 
#     P += sn[:-n]
#     F += snf[n:]

#     pickle.dump((X,P,F), open('xpf.pcl', 'wb'))
   
(X,F,P) = pickle.load(open('xpf.pcl', 'rb'))

rnd = np.random

print('Start')
sys.stdout.flush()

start = time.time()

# Form an initial vector for power iteration by taking a randomly
# weighted sum of training examples.
v0 = {}
for x in F:
    mat.dict_add_scale(v0, x, rnd.normal(0.0, 5.0))

U = []
Ud = []
S = []

# Compute 1000 singular vectors of future-past covariance
# by computing the eigen vectors of FP^TPF^T using power iteration
# with deflation.
for i in range(1000):
    print(i)
    sys.stdout.flush()
    mu,u = mat.power_iteration_4(F, P, U, S, 10, v0)
    S.append(mu)
    U.append(u)

    # Output the singular vectors produced so far every 5 iterations
    if i % 5 == 0:
        print(i)
        sys.stdout.flush()
        #pickle.dump((U,S), gzip.open( + '.gz', 'wb'), 0)
        checkpoint_name = 'uds4vid.' + str(i % 2)
        Uk = [k for k in U[0].keys()]
        Uv = np.asarray([[U[j][x] for x in U[0].keys()] for j in range(i+1)])
        np.save(checkpoint_name, Uv)
        pickle.dump((Uk,S), gzip.open(checkpoint_name + '.gz', 'wb'), -1)

        end = time.time()
        duration = end-start
        print('Finished iteration ' + str(i) + ', elapsed time = ' + str(duration))
        sys.stdout.flush()

S = np.sqrt(S)

