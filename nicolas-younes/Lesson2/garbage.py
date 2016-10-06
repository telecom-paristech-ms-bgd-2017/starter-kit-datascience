import numpy as np
from sklearn import preprocessing


X = [np.arange(4)]

print(X)

poly = preprocessing.PolynomialFeatures(2)
poly.fit(X)

print(X)


