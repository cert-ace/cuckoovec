from preprocess import *
from ngrams import *
import mat_utils_dict as mat
import numpy as np
import time
import pickle
import gzip
import sys
import os

l1_lambda_str = '1.0' if len(sys.argv) < 2 else sys.argv[1]
l1_lambda = float(l1_lambda_str)
out_dir = '/home/ahefny/acelmb/' + l1_lambda_str + '/'
#out_dir = '/media/ahefny/'

os.makedirs(out_dir, exist_ok=True)

# N-gram length
n = 5

# Constructing examples
print('Preprocessing Files')
P = [] # pasts
F = [] # futures
X = []

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

#     pickle.dump((X,P,F), open(out_dir + 'xpf.pcl', 'wb'))
#exit()
    
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
    #mu,u = mat.power_iteration_4(F, P, U, S, 10, v0)
    mu,u = mat.sparse_power_iteration_4(F, P, U, S, l1_lambda, 10, v0)
    S.append(mu)
    U.append(u)

    # Output the singular vectors produced so far every 5 iterations
    # The output consists of two files:
    # .npy: Numpy file containing singular vectors stored as a matrix (each row is a vector)
    # .gz: A gzipped pickle containing a tuple (K,S), where:
    #   K is a list of key names corresponding to coordinates in the singular vectors.
    #   S is a list of square singular values.
    if (i+1) % 5 == 0:
        print(i)
        sys.stdout.flush()
        checkpoint_name = out_dir + 'uds4vid.' + str(i % 2)
        Uk = [k for k in U[0].keys()]
        Uv = np.asarray([[U[j][x] for x in U[0].keys()] for j in range(i+1)])
        np.save(checkpoint_name, Uv)
        pickle.dump((Uk,S), gzip.open(checkpoint_name + '.gz', 'wb'), -1)

        end = time.time()
        duration = end-start
        print('Finished iteration ' + str(i) + ', elapsed time = ' + str(duration))
        sys.stdout.flush()

S = np.sqrt(S)

