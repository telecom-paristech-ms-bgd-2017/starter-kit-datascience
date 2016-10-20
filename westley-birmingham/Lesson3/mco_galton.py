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
from sklearn.preprocessing import StandardScaler
from statsmodels.nonparametric.kde import KDEUnivariate
from scipy.stats import gaussian_kde


# Uncomment the following 2 lines for Mac OS X / Spyder for using Tex display
# import os as macosx
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'font.size': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (8, 6)}
plt.rcParams.update(params)
plt.close("all")

sns.set_palette("colorblind")
sns.axes_style()
sns.set_style({'legend.frameon': True})
color_blind_list = sns.color_palette("colorblind", 8)
my_orange = color_blind_list[2]
my_green = color_blind_list[1]
my_blue = color_blind_list[0]
my_purple = color_blind_list[3]

###############################################################################
# One variable at a time:
plt.close("all")

###############################################################################
# Q1: Loading, cm and rounding

# Load data
url = 'http://www.math.uah.edu/stat/data/Galton.txt'
df = pd.read_csv(url, sep='\t')

# Convert inches to cm
df[['Father', 'Mother', 'Height']] = 2.54 * df[['Father', 'Mother', 'Height']]
pd.set_option('precision', 0)

# Alternative:
# df.round({'Father': 0, 'Mother': 0, 'Height': 0})

# BEWARE: the display option does not necessarily affect the underlying float
# values so, depending on the choice performed, there might be a (tiny)
# difference in the estimators obtained latter on...

###############################################################################
# Q2: Any Na in the dataframe?

null_data = df[df.isnull().any(axis=1)]
print("There are " + str(df.isnull().sum().sum()) +
      ' total missing values')


###############################################################################
# Q3: Plot height density for Mothers and Fathers

plt.figure()
kde_father = KDEUnivariate(df['Father'])
kde_father.fit(bw=2, kernel='gau')
x_grid = np.linspace(140, 210)
pdf_est_father = kde_father.evaluate(x_grid)

kde_mother = KDEUnivariate(df['Mother'])
kde_mother.fit(bw=2, kernel='gau')
x_grid = np.linspace(140, 210)
pdf_est_mother = kde_mother.evaluate(x_grid)

plt.plot(x_grid, pdf_est_father, color=my_blue, label='Father')
plt.fill_between(x_grid, 0, pdf_est_father, facecolor=my_blue, alpha=0.5)

plt.plot(x_grid, pdf_est_mother, color=my_purple, label='Mother')
plt.fill_between(x_grid, 0, pdf_est_mother, facecolor=my_purple, alpha=0.5)

plt.ylabel('Density', fontsize=18)
plt.xlabel('Height (in cm.)', fontsize=18)
plt.legend()
plt.show()


###############################################################################
# Another possibility when the data has unique observations,
# with gaussian_kde from scipy.stats

father_unique = df['Father'].groupby(df['Family']).first()
mother_unique = df['Mother'].groupby(df['Family']).first()

plt.figure()
kde_father = gaussian_kde(father_unique)
x_grid = np.linspace(140, 210)
pdf_est_father = kde_father(x_grid)

kde_mother = gaussian_kde(mother_unique)
x_grid = np.linspace(140, 210)
pdf_est_mother = kde_mother(x_grid)

plt.plot(x_grid, pdf_est_father, color=my_blue, label='Father')
plt.fill_between(x_grid, 0, pdf_est_father, facecolor=my_blue, alpha=0.5)

plt.plot(x_grid, pdf_est_mother, color=my_purple, label='Mother')
plt.fill_between(x_grid, 0, pdf_est_mother, facecolor=my_purple, alpha=0.5)

plt.ylabel('Density', fontsize=18)
plt.xlabel('Height (in cm.)', fontsize=18)
plt.legend()
plt.show()


###############################################################################
# Q4:
# Plot Father height as a function of Mother height, with OLS prediction

plt.figure()
y = df['Father']
X = df[['Mother']]
plt.plot(X, y, 'o')
plt.ylabel('Father height', fontsize=18)
plt.ylim([140, 200])
plt.xlim([140, 200])
plt.xlabel('Mother height', fontsize=18)
skl_lm = linear_model.LinearRegression()
skl_lm.fit(X, y)
plt.plot(x_grid, skl_lm.predict(x_grid.reshape(x_grid.shape[0], 1)), '-')
plt.show()
print(skl_lm.score(X, y))  # it is pretty small...


###############################################################################
# Q5: Distribution of the number of children by family (using count, but
# using mean could also be work fine)

groupby_family = df['Family'].groupby(df['Family']).count()
plt.figure()
plt.hist(groupby_family, normed=True)
plt.xlabel('Number of children', fontsize=18)
plt.ylabel('Density', fontsize=18)
plt.show()

###############################################################################
# Q6: MidParents creation

df['MidParents'] = 0.5 * (df['Father'] + 1.08 * df['Mother'])

# Remark
print("The factor 1.08 gives a rescaled women's height variable which has \
      \n the same average as the men's height. Indeed, the ratio of the \
      \n average men's height over the average women's height is " +
      str(np.mean(df['Father']) / np.mean(df['Mother'])))


###############################################################################
# Q7: Plot MidParents vs kids:

X0 = df[['MidParents']]
y = df['Height']
skl_lm = linear_model.LinearRegression()
skl_lm.fit(X0, y)
theta0 = skl_lm.intercept_
theta1 = skl_lm.coef_[0]
y_mean = y.mean()
X0_mean = (X0.mean(axis=0)).squeeze()
X0_var = X0.var(ddof=0).squeeze()
y_var = y.var(ddof=0)
theta1_manual = ((X0.squeeze() - X0_mean) * (y - y_mean)).mean() / X0_var
theta0_manual = y_mean - theta1_manual * X0_mean
print(theta1)
print(theta1_manual)

print('Are the two computations of theta1' +
      ' the same? This is {}'.format(np.isclose(theta1, theta1_manual)))

print('Are the two computations of theta0' +
      ' the same? This is {}'.format(np.isclose(theta0, theta0_manual)))


###############################################################################
# Q8: Fit regression model for MidParents, and display colors by gender

male = df['Gender'] == 'M'
female = df['Gender'] == 'F'
fig = plt.figure()
plt.plot(df['MidParents'][male], y[male], 'o', c=my_blue)
plt.plot(df['MidParents'][female], y[female], 'o', c=my_purple)
plt.plot(X0, skl_lm.predict(X0), label='Linear prediction', c='k')
plt.xlabel('MidParents', fontsize=18)
plt.ylabel('Kids height', fontsize=18)
plt.show()


###############################################################################
# Q9: Residual density estimation

nb_f = float(female.sum())
nb_m = float(male.sum())
prop_f = nb_f / (nb_f + nb_m)
prop_m = nb_m / (nb_f + nb_m)

plt.figure()
residual = y - skl_lm.predict(X0)
x_grid = np.linspace(-40, 30, num=300)
plt.title('Residual Histogram/ KDE')
plt.xlabel('Residual value')
plt.ylabel('Frequency')

kde_residual = KDEUnivariate(residual)
kde_residual.fit(bw=2, kernel='gau')
pdf_est_residual = kde_residual.evaluate(x_grid)
plt.plot(x_grid, pdf_est_residual, color='k', label='All')

kde_residual_m = KDEUnivariate(residual[male])
kde_residual_m.fit(bw=2, kernel='gau')
pdf_est_residual_m = kde_residual_m.evaluate(x_grid)
plt.plot(x_grid, prop_m * pdf_est_residual_m, color=my_blue, label='Male')

kde_residual_f = KDEUnivariate(residual[female])
kde_residual_f.fit(bw=2, kernel='gau')
pdf_est_residual_f = kde_residual_f.evaluate(x_grid)
plt.plot(x_grid, prop_f * pdf_est_residual_f, color=my_purple, label='Female')
plt.legend()
plt.show()

# Gaussianity does not seem a reasonable assumption, bi-modal residuals due to
# gender differences

###############################################################################
# Q10: Inverting the model

skl_lm = linear_model.LinearRegression()
skl_lm.fit(df[['Height']], df['MidParents'])
alpha0 = skl_lm.intercept_
alpha1 = skl_lm.coef_[0]
alpha0_manual = X0_mean + y_mean / X0_mean * X0_var / y_var * (theta0 - y_mean)
alpha1_manual = X0_var / y_var * theta1_manual
print(alpha1)
print(alpha1_manual)

print('Are the two computations of alpha1' +
      ' the same? This is {}'.format(np.isclose(alpha1, alpha1_manual)))

print('Are the two computations of alpha0' +
      ' the same? This is {}'.format(np.isclose(alpha0, alpha0_manual)))


###############################################################################
# Q11: OLS with the 2 features 'Father', 'Mother'

X1 = df[['Father', 'Mother']]

# Fit regression model
skl_lm = linear_model.LinearRegression()
skl_lm.fit(X1, y)
results = skl_lm.coef_

###############################################################################
# Q12: 3D visualization

XX = np.arange(np.min(X1['Father']) - 2, np.max(X1['Father']) + 2, 0.5)
YY = np.arange(np.min(X1['Mother']) - 2, np.max(X1['Mother']) + 2, 0.5)
YY = np.arange(np.min(y) - 2, np.max(y) + 2, 0.5)
xx, yy = np.meshgrid(XX, YY)
zz = results[0] * xx + results[1] * yy + skl_lm.intercept_


fig = plt.figure()
ax = Axes3D(fig)

ax.set_zlim(np.min(y) - 2, np.max(y) + 2)
ax.set_xlabel('Father')
ax.set_ylabel('Mother')
ax.set_zlabel('Child')
ax.plot_wireframe(xx, yy, zz, rstride=10, cstride=10, alpha=0.3)
ax.plot(X1['Father'], X1['Mother'], y, 'o')

plt.show()

###############################################################################
# Q13: Residuals sum of squares

residual = y - skl_lm.predict(X1)
print(np.linalg.norm(residual) ** 2)


###############################################################################
# Q14: Residuals density estimation / visualisation

plt.figure()
x_grid = np.linspace(-40, 30, num=300)
plt.title('Residual Histogram/ KDE')
plt.xlabel('Residual value')
plt.ylabel('Frequency')

kde_residual = KDEUnivariate(residual.sort_values(ascending=0))
kde_residual.fit(bw=2, kernel='gau')
pdf_est_residual = kde_residual.evaluate(x_grid)
plt.plot(x_grid, pdf_est_residual, color='k', label='All')

kde_residual_m = KDEUnivariate(residual[male].sort_values(ascending=0))
kde_residual_m.fit(bw=2, kernel='gau')
pdf_est_residual_m = kde_residual_m.evaluate(x_grid)
plt.plot(x_grid, prop_m * pdf_est_residual_m, color=my_blue, label='Male')

kde_residual_f = KDEUnivariate(residual[female].sort_values(ascending=0))
kde_residual_f.fit(bw=2, kernel='gau')
pdf_est_residual_f = kde_residual_f.evaluate(x_grid)
plt.plot(x_grid, prop_f * pdf_est_residual_f, color=my_purple, label='Female')
plt.legend()
plt.show()

# same problem as before: one can still observe the bi-modality due to the
# genders


###############################################################################
# Q15: Feature Importance

print(results[0])
print(results[1])
print('Without normalization the main effect is due' +
      ' to {}'.format(X1.columns[np.argmax(results)]))

X2 = StandardScaler().fit_transform(X1)

# Fit regression model
skl_lm = linear_model.LinearRegression()
skl_lm.fit(X2, y)
results_norm = skl_lm.coef_

print(results_norm[0])
print(results_norm[1])
print('With normalization the main effect is due' +
      ' to {}'.format(X1.columns[np.argmax(results_norm)]))
