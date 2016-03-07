from deltas_bin import *
from preprocess import *
from ngrams import *
from libcuckoo import CuckooVector
import mat_utils
import numpy as np
import time
import pickle

out_dir = "/home/ahefny/"

def cuckoo2dict(c):
    d = {}
    for (k,v) in c.items():
        d[k] = v

    return d

# N-gram length
n = 5

# Constructing examples
P = [] # pasts
F = [] # futures
X = []

for f in ['data/1412.bin','data/1413.bin','data/1414.bin','data/1415.bin']:
    print(f)
    R = readDetections(f)
    D = deltas(R)
    A = np.asarray(D) #Convert to Numpy array
    A.ravel()[np.where(np.abs(A).ravel() < 1e-3)] = 0.0 #Apply threshold to score deltas
    T = filterByAbsRowSum(A, 1e-3) 
    s = stringify(T)
    sn = extract_ngrams(s, n, 1e-4)

    X += sn 
    P += sn[:-n]
    F += sn[n:]

    pickle.dump((X,P,F), open(out_dir + 'xpf.pcl', 'wb', -1))   
#(X,F,P) = pickle.load(open('xpf.pcl', 'rb'))

rnd = np.random

start = time.time()

# Form an initial vector for power iteration by taking a randomly
# weighted sum of training examples.
v0 = CuckooVector({})
for x in X:
    v0.add_scale_dict(x, rnd.normal(0.0, 5.0))

U = []
Ud = []
S = []

# Compute 1000 singular vectors of future-past covariance
# by computing the eigen vectors of FP^TPF^T using power iteration
# with deflation.
for i in range(1000):
    print(i)
    mu,u = mat_utils.power_iteration_4(F, P, U, S, 10, v0)
    S.append(mu)
    U.append(u)

    # Convert new singular vector from Cuckoovec to dictionary
    # for ease of serialization
    Ud.append(cuckoo2dict(u)) 

    # Output the singular vectors produced so far every 5 iterations
    if i % 5 == 0:
        print(i)
        pickle.dump((Ud,S), open(out_dir + 'uds4vid.pcl.' + str(i % 2), 'wb'))
        end = time.time()
        duration = end-start
        print('Finished iteration ' + str(i) + ', elapsed time = ' + str(duration))

S = np.sqrt(S)


