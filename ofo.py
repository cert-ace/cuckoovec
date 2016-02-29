from libcuckoo import CuckooVector
import numpy as np

def with_replacement(X, Y, T):
  x = CuckooVector({})
  m = len(Y)
  
  for t in range(T):  
    i = np.random.randint(m)
    y = Y[i]
    x.reset(X[i])
    yield (x,y)
  
def pegasos(lam):  
  w = CuckooVector({})
  wx = 0
  t = 0
  
#  while True:
#    example = yield (w,wx)
#    if example == None: break
#    x,y = example
  for xy in (yield (w,wx)):
    x,y = xy
    print(x)
    print(y)
    step = 1 / (lam * (t+1))
    w.scale(1 - step * lam)
    wx = w.dot(x)
    if y * wx < 1:
      w.add_scale(x, step * y)
    t = t+1
	  
def ofo(sample, update):
  a = 0
  b = 0
  tau = 0
  
  update.send(None)
  for x,y in sample:
    w, wx = update.send((x,y))

    ypred = 1 if wx >= tau else 0 
    y = (y + 1)/2  # [-1,1] -> [0,1]
    a = a + y*ypred
    b = b + y - ypred
    tau = a/b
	
    yield (w,tau)  