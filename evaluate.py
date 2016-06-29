import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn.svm import *
from scipy.io import savemat
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier

work_dir = '/home/ahefny/'
#work_dir = '/media/ahefny/Data/'

def time_to_frame(f):
  n = [int(s) for s in f.split(':')]
  return (n[0]*(3600) + n[1]*60 + n[2]) * 30

# Reads a pair of data files.
# uf_file contains projected n-gram features (see project_data.py),
# fid_file is an array of frame ids.
# csv_file contains time stamped evaluations.
def read_data(uf_file, fid_file, csv_file):
  # Concatenate projected data
  UFi = np.load(uf_file)
  FIDi = np.load(fid_file)
  nf = UFi.shape[1]

  assert FIDi.shape[0] == nf
  
  # Process CSV files to extract labels. First extract a list of time
  # intervals in the format [begin_frame, end_frame]
  with open(csv_file) as lines:
    times = [l.strip().split(',')[1:3] for l in lines]  
    times = times[1:]

    for i in range(len(times)):
      # Convert time stamp to frame number
      times[i][0] = time_to_frame(times[i][0])

      # If there is an end time stamp, convert it to frame number.
      # Otherwise, assume 90 frames (3 seconds) after start time.
      if ':' in times[i][1]:
        times[i][1] = time_to_frame(times[i][1])
      else:
        times[i][1] = times[i][0] + 90

    # Convert the list of positive time intervals to positive time indicator dictionary
    # s.t. pos[t] == 1 iff t is inone of thepositive intervals.
    pos = {}

    for x in times:
      for i in range(x[0], x[1]+1):
        pos[i] = 1

    # Using the created dictionary create a vector of labels 
    yf = np.zeros(nf)

    for i in range(0,nf):
      t = FIDi[i]

      if pos.get(t, 0) == 1:
        yf[i] = 1

    yf = yf * 2 - 1;
    return (UFi, yf)

def read_data_files(uf_files, fid_files, csv_files):
  assert len(uf_files) == len(fid_files)
  assert len(csv_files) == len(fid_files)
  
  UF = None
  y = np.asarray([])

  for f in range(len(uf_files)):
    # Concatenate projected data
    (UFi, yf) = read_data(uf_files[f], fid_files[f], csv_files[f])  

    if UF is None:
      UF = UFi
    else:
      UF = np.hstack((UF, UFi))

    print(UFi.shape)  
    print(yf.shape)
    y = np.append(y, yf)

  XX = UF.T

  return(XX, YY)  
  
csv_files = ['data/1412.csv', 'data/1413.csv', 'data/1414.csv', 'data/1415.csv']
ufiles = [work_dir+'UF0.npy', work_dir+'UF1.npy', work_dir+'UF2.npy', work_dir+'UF3.npy']
fid_files = [work_dir+'FID0.npy', work_dir+'FID1.npy', work_dir+'FID2.npy', work_dir+'FID3.npy']

# Read data
folds = [read_data(x[0],x[1],x[2]) for x in zip(ufiles, fid_files, csv_files)]

shuffle = True
chunk = 1
num_folds = 4

chunk_bds = list(range(0,N,chunk)) + [N]
chunk_start = np.asarray(chunk_bds[:-1])
chunk_end = np.asarray(chunk_bds[1:])

if shuffle:
  X = np.hstack([x[0] for x in folds])
  Y = np.hstack([x[1] for x in folds])
  N = X.shape[1]
  M = len(chunk_start)
  idx = np.random.permutation(M)
  chunk_start = chunk_start[idx]
  chunk_end = chunk_end[idx]
  
  #p = list(range(0,N,int(np.ceil(N/4))))
  #if p[-1] != N-1: p.append(N-1)
  
  folds = []
  for i in range(0,num_folds):
    Xi = np.hstack([X[:,chunk_start[j]:chunk_end[j]] for j in range(i,M,num_folds)])
    Yi = np.hstack([Y[chunk_start[j]:chunk_end[j]] for j in range(i,M,num_folds)])
    folds.append((Xi, Yi))

svm = LinearSVC()
svm_bal = LinearSVC(class_weight='balanced')
clf = RandomForestClassifier(n_estimators=20,max_features=10)

classifiers = {
  'svm' : (lambda x,y: svm.fit(x,y), lambda x: svm.decision_function(x)),
  'svm_bal' : (lambda x,y: svm_bal.fit(x,y), lambda x: svm_bal.decision_function(x)),
  'tree' : (lambda x,y: clf.fit(x,y), lambda x: clf.predict_proba(x)[:,1])
  }

auc = {}

for fold in range(0,len(folds)):
  print('Fold ' + str(fold))
  train_parts = folds[:fold] + folds[fold+1:]
  test_part = folds[fold]

  Xtrain = np.hstack([x[0] for x in train_parts]).T
  Ytrain = np.hstack(x[1] for x in train_parts)
  Xtest = test_part[0].T
  Ytest = test_part[1]

  roc = {}
  
  # Train and evaluate classifiers
  for (name,func) in classifiers.items():
    func[0](Xtrain, Ytrain)

    Yh = func[1](Xtest)
    roc[name] = roc_curve(Ytest, Yh)
    auc_score = roc_auc_score(Ytest, Yh)

    if fold == 0:
      auc[name] = [auc_score]
    else:
      auc[name].append(auc_score)

  # Evaluate classifiers
  print(svm.score(Xtest, Ytest))
  Yh = svm.decision_function(Xtest)
  print(svm_bal.score(Xtest, Ytest))
  Yh_bal = svm_bal.decision_function(Xtest)
  print(clf.score(Xtest, Ytest))
  Yh_tr = clf.predict_proba(Xtest)[:,1]

  # Compute and save ROC curves
  savemat(work_dir+'roc.mat', roc)

  plt.figure()
  plt.plot(np.asarray([0,1]), np.asarray([0,1]), 'k--')
  plt.hold(True)
  plt.plot(roc['svm'][0], roc['svm'][1])
  plt.plot(roc['svm_bal'][0], roc['svm_bal'][1])
  plt.plot(roc['tree'][0], roc['tree'][1])
  plt.hold(False)
  plt.savefig('roc_{0}.png'.format(fold))

avg_auc = dict((k,sum(v)/num_folds) for (k,v) in auc.items())

print(avg_auc)
