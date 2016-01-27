from svm import svm_primal_sgd
import numpy as np
from sklearn.cross_validation import train_test_split

m = 2000
n = 5
X = np.random.randn(m,n)
wstar = np.random.randn(n)
Y = np.sign(X.dot(wstar))

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.25)
w = np.zeros(n)
for k,v in svm_primal_sgd([{str(i): x[i] for i in range(n)} for x in Xtrain], Ytrain, 0.1, 1000).items():
  w[int(k)] = v

print([wstar, w])
print("train corr: ", np.mean(np.sign(Xtrain.dot(w))*Ytrain))
print("test corr: ", np.mean(np.sign(Xtest.dot(w))*Ytest))