
import numpy as np
import matplotlib.pyplot as plt  # for plots
from matplotlib import rc
import seaborn as sns
from os import mkdir, path
from scipy import stats
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from math import cos, sin, pi
from statsmodels.nonparametric.kde import KDEUnivariate
from scipy.linalg import toeplitz
from numpy.linalg import eigh
sns.set_style("white")

# Uncomment the following command for Mac OS X / Spyder for using Tex display
# import os as macosx:
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

dirname = "../srcimages/"
# dirname = "trash:///"
if not path.exists(dirname):
    mkdir(dirname)

imageformat = '.pdf'
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'font.size': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (8, 6)}
plt.rcParams.update(params)
mc3my_brown = (0.64, 0.16, 0.16)
purple = (148. / 255, 0, 211. / 255)
plt.close("all")


###############################################################################
# display function:

def my_saving_display(fig, dirname, filename, imageformat):
    """"saving faster"""
    dirname + filename + imageformat
    image_name = dirname + filename + imageformat
    fig.savefig(image_name)


###############################################################################
# Empirical mean:

mu = 1.5
sigma = 4
nb_samples = 8

np.random.seed(seed=2)
rgamma = np.random.gamma
X = rgamma(mu, sigma, nb_samples)
y = np.ones(nb_samples,)

# Various statistics:
meanX = np.mean(X)
minX = np.min(X)
maxX = np.max(X)
medX = np.median(X)
MADX = np.median(np.abs(X - medX))
s = np.std(X)

alpha_trim = 0.15
tmeanX = stats.trim_mean(X, alpha_trim)


###############################################################################
#  Empirical mean:

fig1, ax = plt.subplots(figsize=(10, 3))
ax.set_ylim(0, 1.5)
ax.set_xlim(minX - 0.1 * np.ptp(X), maxX + 0.1 * np.ptp(X))
ax.get_xaxis().tick_bottom()
ax.axes.get_yaxis().set_visible(False)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0.5))
ax.spines['left'].set_color('none')

ax.scatter(X, y, color='black', s=300, marker='o',
           edgecolors=mc3my_brown, linewidth='1')

ax.plot([meanX, meanX], [0, 1.5], color=mc3my_brown,
        linewidth=1.5, linestyle="--")
plt.xlabel(r'$y$', fontsize=18)
plt.annotate(r'$\overline{y}_n : \mbox{moyenne empirique}$',
             xy=(meanX, 0.4), xycoords='data', xytext=(+10, +30),
             textcoords='offset points', fontsize=18, color=mc3my_brown)

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaSampleMean", imageformat)