from deltas_bin import *
from preprocess import *
from ngrams import *
from cuckoovec import CuckooVector
import mat_utils
import numpy as np

n = 5

R = readDetections('/media/ahefny/Data/Research/ace/1413.bin')
D = deltas(R)
A = np.asarray(D)
A.ravel()[np.where(np.abs(A).ravel() < 1e-3)] = 0.0
T = filterByAbsRowSum(A, 1e-3)
s = stringify(T)
sn = extract_ngrams(s, n, 1e-4)

"""
X = [None] * len(sn)
for i in range(len(sn)):
    print("Creating vector " + str(i))
    X[i] = CuckooVector(sn[i])
"""

X = [CuckooVector(x) for x in sn[0:100]]

P = X[:-n]
F = X[n:]

rnd = np.random

v0 = CuckooVector({})
for x in X:
    v0.add_scale(x, rnd.normal(0.0, 5.0))

U = []
S = []

for i in range(10):
    print(i)
    mu,u = mat_utils.power_iteration_4(F, P, U, S, 10, v0)
    S.append(mu)
    U.append(u)

