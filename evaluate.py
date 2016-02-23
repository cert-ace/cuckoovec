import numpy as np
import pickle
from sklearn.cross_validation import train_test_split
from sklearn.svm import *

def time_to_frame(f):
  n = [int(s) for s in f.split(':')]
  return (n[0]*(3600) + n[1]*60 + n[2]) * 30

csv = ['data/1412.csv', 'data/1413.csv']
ufile = ['UF0.npy', 'UF1.npy']
#(X,F,P) = pickle.load(open('xpf.pcl', 'rb'))
UF = None
y = np.asarray([])

for f in range(2):
  UFi = np.load(ufile[f])
  nf = UFi.shape[1]
  if UF is None:
    UF = UFi
  else:
    UF = np.hstack((UF, UFi))

  print(UFi.shape)
    
  with open(csv[f]) as lines:
    times = [l.strip().split(',')[1:3] for l in lines] 
    
    times = times[1:]

    for i in range(len(times)):
      times[i][0] = time_to_frame(times[i][0])

      if ':' in times[i][1]:
        times[i][1] = time_to_frame(times[i][1]) - 90
      else:
        times[i][1] = times[i][0] + 90

    pos = {}

    for x in times:
      for i in range(x[0], x[1]+1):
        pos[i] = 1

    yf = np.zeros(nf)

    for i in range(0,nf):
      t = X[f][0][i]

      if pos.get(t, 0) == 1:
        yf[i] = 1

    print(yf.shape)
    y = np.append(y, yf)

YY = y * 2 - 1
XX = UF.T
        
Xtrain, Xtest, Ytrain, Ytest = train_test_split(XX, YY, test_size=0.25)

svm = LinearSVC(class_weight='balanced').fit(Xtrain, Ytrain)
print(svm.score(Xtest, Ytest))


