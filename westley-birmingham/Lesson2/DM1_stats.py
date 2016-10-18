# %matplotlib inline
# %matplotlib notebook
import notebook
from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt     # for plots
import seaborn as sns               # for plots
from scipy import stats
import statsmodels.api as sm
from sklearn import linear_model


# Exercice 1
# Question 1
gaston_df = pd.read_csv('http://www.math.uah.edu/stat/data/Galton.csv', sep=',',
                          comment='#', na_values="n/d")

gaston_df['Father'] = round(gaston_df['Father']*2.54)
gaston_df['Mother'] = round(gaston_df['Mother']*2.54)
gaston_df['Height'] = round(gaston_df['Height']*2.54)

print(gaston_df)

#theta_0 = linearmodel.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)


