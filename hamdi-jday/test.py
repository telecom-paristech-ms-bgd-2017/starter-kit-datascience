# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:35:02 2016

@author: hamdi
"""

import pandas as pd
import matplotlib.pyplot as plt
import sklearn.linear_model as lm
# Load data
url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/datasets/cars.csv'
dat = pd.read_csv(url)
y=dat['dist']
X = dat[['speed']] # sklearn needs X to have 2 dim.
skl_linmod = lm.LinearRegression(fit_intercept=False)
skl_linmod.fit(X, y) # Fit regression model
fig = plt.figure(figsize=(8, 6))
plt.plot(X, y, 'o', label="Data")
plt.plot(X, skl_linmod.predict(X), 'r', label="OLS")
plt.legend(loc='upper left')
plt.show()
