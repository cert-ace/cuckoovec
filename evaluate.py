import numpy as np
import pickle
from sklearn.cross_validation import train_test_split
from sklearn.svm import *
from scipy.io import savemat
from sklearn.metrics import roc_curve

work_dir = '/home/ahefny/'
#work_dir = '/media/ahefny/Data/'

def time_to_frame(f):
  n = [int(s) for s in f.split(':')]
  return (n[0]*(3600) + n[1]*60 + n[2]) * 30

csv = ['data/1412.csv', 'data/1413.csv']
ufile = [work_dir+'UF0.npy', work_dir+'UF1.npy']
(X,F,P) = pickle.load(open(work_dir+'xpf.pcl', 'rb'))
UF = None
y = np.asarray([])

for f in range(len(csv)):
  # Concatenate projected data
  UFi = np.load(ufile[f])
  nf = UFi.shape[1]
  if UF is None:
    UF = UFi
  else:
    UF = np.hstack((UF, UFi))

  print(UFi.shape)
    
  # Process CSV files to extract labels. First extract a list of time
  # intervals in the format [begin_frame, end_frame]
  with open(csv[f]) as lines:
    times = [l.strip().split(',')[1:3] for l in lines] 
    
    times = times[1:]

    for i in range(len(times)):
      # Convert time stamp to frame number
      times[i][0] = time_to_frame(times[i][0])

      # If there is an end time stamp, convert it to frame number.
      # Otherwise, assume 90 frames (30 seconds) after start time.
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
      t = X[f][0][i]

      if pos.get(t, 0) == 1:
        yf[i] = 1

    print(yf.shape)
    y = np.append(y, yf)

####################################################################################
## Create classifiers based on the training data
####################################################################################
YY = y * 2 - 1
XX = UF.T
        
Xtrain, Xtest, Ytrain, Ytest = train_test_split(XX, YY, test_size=0.25)

# Linear SVM 
svm = LinearSVC().fit(Xtrain, Ytrain)
print(svm.score(Xtest, Ytest))
Yh = svm.decision_function(Xtest)

# Linear SVM with class balancing
svm_bal = LinearSVC(class_weight='balanced').fit(Xtrain, Ytrain)
print(svm_bal.score(Xtest, Ytest))
Yh_bal = svm_bal.decision_function(Xtest)

# Compute and save ROC curves
savemat(work_dir+'roc.mat', {'roc' : roc_curve(Ytest, Yh), 'roc_bal' : roc_curve(Ytest, Yh_bal)})


