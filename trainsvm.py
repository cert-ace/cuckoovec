#from svm import svm_primal_sgd
from ofo import *
from libcuckoo import CuckooVector
from deltagrams import DeltaGrams
from preprocess import frame_to_index
import sys
import numpy as np
from sklearn.cross_validation import train_test_split

binfile = sys.argv[1]
activity = sys.argv[2]
X = DeltaGrams(binfile, 30)
m = len(X)

Y = np.zeros(m)
with open(activity) as lines:
  for R in [range(frame_to_index(r[0]), frame_to_index(r[1])) for r in [line.strip().split('\t') for line in lines]]:
    Y[R] = 1
print(np.mean(Y))
Y = 2*Y - 1

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.25)

w = 0
thresh = 0
for w,thresh in ofo(with_replacement(Xtrain, Ytrain, 10000), pegasos(0.01)):
  print(thresh)
  
#w = svm_primal_sgd(Xtrain, Ytrain, 0.01, 10000)

def weightedError(w, Xt, Yt, thresh = 0):
   xv = CuckooVector({})
   return (1 + np.mean([(xv.reset(x) == None and np.sign(xv.dot(w) - thresh)*y) for (x,y) in zip(Xt,Yt)]))/2
   
print("train errors: ", weightedError(w, Xtrain, Ytrain))
print("test errors: ", weightedError(w, Xtest, Ytest))