import pickle
import gzip
import numpy as np
import mat_utils_dict as mat

(X,F,P) = pickle.load(open('xpf.pcl', 'rb'))

(k,S) = pickle.load(gzip.open('uds4vid.0.gz', 'rb'))
v = np.load('uds4vid.0.npy')
n = len(S)
d = v.shape[1]

U = []
for i in range(n):
    U.append({k[j] : v[i,j] for j in range(d)})

UF = []
for s in range(len(X)):
    Fs = X[s][1]
    N = len(Fs)
    UF.append(np.asarray([[mat.dict_dot(Fs[i], U[j]) for i in range(N)] for j in range(n)]))
    
