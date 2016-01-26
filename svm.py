from cuckoovec import CuckooVector
import numpy as np

# stochastic primal subgradient descent
# aka "pegasos"
# http://ttic.uchicago.edu/~nati/Publications/PegasosMPB.pdf

@profile
def svm_primal_sgd(X, Y, lam, T):  
  w = CuckooVector({})
  x = CuckooVector({})
  m = len(Y)
  
  for t in range(T):
    step = 1 / (lam * (t+1))
    i = np.random.randint(m)
    y = Y[i]
    x.reset(X[i])
    w.scale(1 - step * lam)
    if y * w.dot(x) < 1:
      w.add_scale(x, step * y)

  return w
  