from svm import svm_primal_sgd
from cuckoovec import CuckooVector
from deltagrams import DeltaGrams
from preprocess import frame_to_index
import sys
import numpy as np
from sklearn.cross_validation import train_test_split

binfile = sys.argv[1]
activity = sys.argv[2]
X = DeltaGrams(binfile, 3)
m = len(X)

Y = np.zeros(m)
with open(activity) as lines:
  for R in [range(frame_to_index(r[0]), frame_to_index(r[1])) for r in [line.strip().split('\t') for line in lines]]:
    Y[R] = 1
Y = 2*Y - 1
#Y = 2 * np.random.rand(m) - 1   # "baseline"

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.25)

w = svm_primal_sgd(Xtrain, Ytrain, 0.1, 5000)

xv = CuckooVector({}) 
print("train errors: ", np.mean([(xv.reset(x) == None and xv.dot(w)*y > 0) for (x,y) in zip(Xtrain,Ytrain)]))
print("train errors: ", np.mean([(xv.reset(x) == None and xv.dot(w)*y > 0) for (x,y) in zip(Xtest,Ytest)]))