import pickle
import gzip
import numpy as np
import mat_utils_dict as mat

#work_dir = '/home/ahefny/'
work_dir = '/media/ahefny/Data/'

# Load dataset ('xpf.pcl' is produced by svd_test_dict)
(X,F,P) = pickle.load(open(work_dir + 'xpf.pcl', 'rb'))

# Load singular vectors
(k,S) = pickle.load(gzip.open(work_dir + 'uds4vid.0.gz', 'rb'))
v = np.load(work_dir + 'uds4vid.0.npy')
n = len(S)
d = v.shape[1]

# Convert singular vectors to dictionary format
U = []
for i in range(n):
    U.append({k[j] : v[i,j] for j in range(d)})

# Project futures using singular vectors    
UF = []
for s in range(len(X)):
    Fs = X[s][2]
    N = len(Fs)
    UF.append(np.asarray([[mat.dict_dot(Fs[i], U[j]) for i in range(N)] for j in range(n)]))
    np.save(work_dir + 'UF{0}'.format(s), UF[s])
    
    
