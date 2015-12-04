from svm import svm_primal_sgd
from deltagrams import DeltaGrams
import sys
import numpy as np

binfile = sys.argv[1]
X = DeltaGrams(binfile, 3)
m = len(X)
Y = 2 * np.random.rand(m) - 1   # "baseline"

w = svm_primal_sgd(X, Y, 0.1, 50)