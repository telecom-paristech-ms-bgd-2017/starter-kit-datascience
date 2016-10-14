# -*- coding: utf-8 -*-
"""
@author: salmon
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from numpy.linalg import svd


# Uncomment the following 2 lines for Mac OS X / Spyder for using Tex display
# import os as macosx
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

plt.close("all")
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'font.size': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (8, 6)}
plt.rcParams.update(params)

sns.set_palette("colorblind")
sns.axes_style()
sns.set_style({'legend.frameon': True})
color_blind_list = sns.color_palette("colorblind", 8)
my_orange = color_blind_list[2]
my_green = color_blind_list[1]
my_blue = color_blind_list[0]
my_purple = color_blind_list[3]


###############################################################################
# Q1: auto-mpg.data-original loading

# Load data
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/' +\
      'auto-mpg.data-original'

u_cols = ['mpg', 'cylinders', 'displacement', 'horsepower',
          'weight', 'acceleration', 'model year', 'origin', 'car name']

# for this dataset na_values are marked as NA.
data = pd.read_csv(url, sep=r"\s+", names=u_cols, na_values='NA')
print(data.shape)

data = data.dropna(axis=0, how='any')
print(data.shape)

# Testing presence/absence of missing values, aka NaN
# data.isnull().values.any()
# data.isnull().any()


###############################################################################
# Q2: OLS over a subset of the dataset

y = data['mpg']
# data.drop(['mpg'], axis=1)
X_partial = data.drop(['origin', 'car name', 'mpg'], axis=1)

# Fit regression model (with sklearn) degenerate case
skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(X_partial[:9], y[:9])

print(skl_linmod.coef_)
print(skl_linmod.intercept_)
print(skl_linmod.predict(X_partial[:9]))
print(skl_linmod.singular_)
print(skl_linmod.rank_)
# The issue occurs because 'cylinders' and 'model year' are constant columns.
# So they are redondant with the intercept_ contribution (non full rank model)


###############################################################################
# Q3: OLS over a full dataset after rescaling/centering

# Fit regression model (with sklearn)
skl_linmod = linear_model.LinearRegression()
scaler = StandardScaler().fit(X_partial)
X = scaler.transform(X_partial)
skl_linmod.fit(X, y)

print(skl_linmod.coef_)
print(skl_linmod.intercept_)
print(skl_linmod.predict(X))
print(skl_linmod.singular_)
rank_variables = np.argsort(np.abs(skl_linmod.coef_))
print(X_partial.columns[rank_variables[-2:]])


###############################################################################
# Q4: Residual

residual = skl_linmod.predict(X) - y
term_1 = np.linalg.norm(y - np.mean(y)) ** 2
term_2 = np.linalg.norm(residual) ** 2
term_3 = np.linalg.norm(skl_linmod.predict(X) - np.mean(y)) ** 2
print(np.isclose(term_1, term_2 + term_3))

# # density / histogram for visualization if needed:
# plt.figure()
# plt.hist(residual, bins=30, normed=True, align='mid')
# sns.kdeplot(residual)
# plt.title('Residual Histogram/ KDE')
# ax = plt.gca()
# ax.legend_ = None
# plt.xlabel('Residual value'), plt.ylabel('Frequency')
# plt.tight_layout()


###############################################################################
# Q5: New observation

X_new = np.array([[6, 225, 100, 3233, 15.4, 76]])
print(skl_linmod.predict(scaler.transform(X_new)))
# This gives 21.77622018, which seems a reasonable prediction knowing that
# the observed value was 22 for such a car.


###############################################################################
# Q6: Polynomial features.

poly = PolynomialFeatures(2, interaction_only=False, include_bias=False)
XX = poly.fit_transform(X)

scalerXX = StandardScaler().fit(XX)
XX = scalerXX.transform(XX)
skl_linmod.fit(XX, y)

print(skl_linmod.coef_)
print(skl_linmod.intercept_)
print(skl_linmod.predict(XX))
print(skl_linmod.singular_)
rank_variables = np.argsort(np.abs(skl_linmod.coef_))
print(rank_variables)


# BEWARE: it might lead to different interpretation if one perform the steps:
# 1) center/rescale the design matrix
# 2) create the interaction features
# 3) center/rescale the new design matrix
# or
# 1) create the interaction features
# 2) center/rescale the new design matrix.
# The most reasonable is to rather proceed as proposed above (ie 2nd choice)


###############################################################################
# Q7: Handling origins

X_partial_bis = data.drop(['car name', 'mpg'], axis=1)
X_partial_bis = pd.get_dummies(X_partial_bis, columns=['origin'],
                               drop_first=False)

scaler = StandardScaler(with_mean=False).fit(X_partial_bis)
Z = scaler.transform(X_partial_bis)

skl_linmod = linear_model.LinearRegression(fit_intercept=False)
skl_linmod.fit(Z, y)

print(skl_linmod.coef_)
print(skl_linmod.intercept_)
print(skl_linmod.predict(Z))
rank_variables = np.argsort(np.abs(skl_linmod.coef_))
print(rank_variables)

# Rem: here, it was useful to remove the intercept to deal with the redundancy
# of the 'dummy' encoding.


###############################################################################
# Q: Handling brands with some text processing

car_names = data['car name']
brands = pd.Series(car_names.str.split().str.get(0))

# A bit of cleaning:
brands = brands.str.replace('volkswagen', 'vw', case=False)
brands = brands.str.replace('vokswagen', 'vw', case=False)
brands = brands.str.replace('toyouta', 'toyota', case=False)
brands = brands.str.replace('maxda', 'mazda', case=False)
brands = brands.str.replace('chevy', 'chevrolet', case=False)
brands = brands.str.replace('chevroelt', 'chevrolet', case=False)
brands = brands.str.replace('mercedes-benz', 'mercedes', case=False)

data['brand'] = pd.Series(brands)

X_brand = data.drop(['car name', 'mpg', 'origin'], axis=1)
X_brand = pd.get_dummies(X_brand, columns=['brand'],
                         drop_first=False)

scaler = StandardScaler(with_mean=False).fit(X_brand)
X_brand_scaled = scaler.transform(X_brand)

skl_linmod = linear_model.LinearRegression(fit_intercept=False)
skl_linmod.fit(X_brand_scaled, y)

print(skl_linmod.coef_)
print(skl_linmod.intercept_)
print(skl_linmod.predict(X_brand_scaled))

# sort by positive influence:
rank_variables = np.argsort((skl_linmod.coef_))
print(X_brand.columns[rank_variables[-5:]])
print(skl_linmod.coef_[rank_variables[-5:]])

# sort by negative influence:
rank_variables = np.argsort((skl_linmod.coef_))
print(X_brand.columns[rank_variables[:5]])
print(skl_linmod.coef_[rank_variables[:5]])

# Rem: here, it was useful to remove the intercept to deal with the redundancy
# of the 'dummy' encoding.


###############################################################################
# Q8: Leverage points

U, s, V = svd(X, full_matrices=False)
proj_mat = np.dot(U, U.T)
print(np.allclose(proj_mat.dot(proj_mat), proj_mat))
print(np.allclose(proj_mat.T, proj_mat))

# Rem: Note that the centering/rescaling step does not modify the leverage.

leverage = np.diag(proj_mat)
data['Leverage'] = leverage
print(data.sort(['Leverage'], ascending=False).head(3))

print(data.describe())
# The maximum leverage has extreme 'displacement' and 'horsepower' values
# The second maximum leverage has extreme 'weight' and 'horsepower' values
# The third maximum leverage has extreme 'weight' and 'horsepower' values


# Bonus visualisation of the leverage: empirical cut-off for "large" leverage
threshold = 2.5 * (float(X.shape[1] + 1) / float(X.shape[0]))

plt.figure()
plt.plot(np.arange(X.shape[0]), leverage)
plt.plot(np.arange(X.shape[0]), threshold * np.ones(X.shape[0]))
