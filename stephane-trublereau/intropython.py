# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 09:39:45 2014

@author: joseph salmon
"""

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
#import os as macosx
#macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

dirname = "./srcimages/"
#dirname = "trash:///"
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


###############################################################################
#  Empirical median:

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

ax.plot([medX, medX], [0, 1.5], color=purple, linewidth=1.5, linestyle="--")
plt.xlabel(r'$y$', fontsize=18)
plt.annotate(r'$\rm{Med}_n(\mathbb{y}): \mbox{m\'ediane empirique}$',
             xy=(medX, 1), xycoords='data', xytext=(-210, +30),
             textcoords='offset points', fontsize=18, color=purple)

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaSampleMediane", imageformat)


###############################################################################
#  Trimmed mean 10%:

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

ax.plot([tmeanX, tmeanX], [0, 1.5], color='blue',
        linewidth=1.5, linestyle="--")
plt.xlabel(r'$y$', fontsize=18)
tt = "$\overline{y}_{n,%s} : \mbox{moyenne tronqu\\'ee}$" % str(alpha_trim)
plt.annotate(tt, xy=(tmeanX, 1), xycoords='data', xytext=(+22, +30),
             textcoords='offset points', fontsize=18, color='blue')

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaSampleTrimmed", imageformat)


###############################################################################
#  Empirical mean / median :

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

ax.plot([meanX, meanX], [0, 1.5], color=mc3my_brown, linewidth=1.5,
        linestyle="--")
ax.plot([medX, medX], [0, 1.5], color=purple, linewidth=1.5, linestyle="--")
ax.plot([tmeanX, tmeanX], [0, 1.5], color='blue',
        linewidth=1.5, linestyle="--")

plt.xlabel(r'$y$', fontsize=18)
plt.annotate(r'$\rm{Med}_n(\mathbb{y}): \mbox{m\'ediane empirique}$',
             xy=(medX, 1), xycoords='data', xytext=(-210, +30),
             textcoords='offset points', fontsize=18, color=purple)
plt.annotate(r'$\bar{y}_n : \mbox{moyenne empirique}$', xy=(meanX, 0.4),
             xycoords='data', xytext=(+10, +30), textcoords='offset points',
             fontsize=18, color=mc3my_brown)
plt.annotate(tt, xy=(tmeanX, 1), xycoords='data', xytext=(+22, +30),
             textcoords='offset points', fontsize=18, color='blue')

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaSampleMedianeMean", imageformat)


###############################################################################
# Standard deviation:

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

ax.plot([meanX, meanX], [0, 1.5], color=mc3my_brown, linewidth=1.5,
        linestyle="--")
plt.arrow(meanX, 1.2, -s, 0, fc=mc3my_brown, ec=mc3my_brown,
          head_width=0.05, head_length=0.1, length_includes_head=True)
plt.arrow(meanX - s, 1.2, s, 0, fc=mc3my_brown, ec=mc3my_brown,
          head_width=0.05, head_length=0.1, length_includes_head=True)
plt.arrow(meanX, 1.2, s, 0, fc=mc3my_brown, ec=mc3my_brown,
          head_width=0.05, head_length=0.1, length_includes_head=True)
plt.arrow(meanX + s, 1.2, -s, 0, fc=mc3my_brown, ec=mc3my_brown,
          head_width=0.05, head_length=0.1, length_includes_head=True)


plt.xlabel(r'$y$', fontsize=18)
plt.annotate(r'$\bar{y}_n : \mbox{moyenne empirique}$',
             xy=(meanX, 0.4), xycoords='data', xytext=(+10, +30),
             textcoords='offset points', fontsize=18, color=mc3my_brown)
plt.annotate(r'$s_n$', xy=(meanX + s * (0.4), 1), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=18,
             color=mc3my_brown)
plt.annotate(r'$s_n$', xy=(meanX - s * (0.6), 1), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=18,
             color=mc3my_brown)

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaSD", imageformat)


###############################################################################
# Mean Absolute Deviation:

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

ax.plot([medX, medX], [0, 1.5], color=purple, linewidth=1.5, linestyle="--")

plt.arrow(medX, 1.2, -MADX, 0, fc=purple, ec=purple, head_width=0.05,
          head_length=0.1, length_includes_head=True)
plt.arrow(medX - MADX, 1.2, MADX, 0, fc=purple, ec=purple, head_width=0.05,
          head_length=0.1, length_includes_head=True)
plt.arrow(medX, 1.2, MADX, 0, fc=purple, ec=purple, head_width=0.05,
          head_length=0.1, length_includes_head=True)
plt.arrow(medX + MADX, 1.2, -MADX, 0, fc=purple, ec=purple, head_width=0.05,
          head_length=0.1, length_includes_head=True)

plt.xlabel(r'$y$', fontsize=18)
plt.annotate(r'$\rm{Med}_n(\mathbb{y}): \mbox{m\'ediane empirique}$',
             xy=(medX, 0.4), xycoords='data', xytext=(+10, +30),
             textcoords='offset points', fontsize=18, color=purple)
plt.annotate(r'$\rm{MAD}_n(\mathbb{y})$', xy=(medX + MADX * (0.1), 1),
             xycoords='data', xytext=(+10, +30), textcoords='offset points',
             fontsize=14, color=purple)
plt.annotate(r'$\rm{MAD}_n(\mathbb{y})$', xy=(medX - MADX * (1.2), 1),
             xycoords='data', xytext=(+10, +30), textcoords='offset points',
             fontsize=14, color=purple)

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "GammaMAD", imageformat)


###############################################################################
# pause: close all figures
plt.close('all')


###############################################################################
# Histogram:

sns.set_style("whitegrid")
mu = 1
sigma = 3
nb_samples = 30

np.random.seed(seed=1)
rgamma = np.random.gamma
X = rgamma(mu, sigma, nb_samples)
y = np.ones(nb_samples,)
# Statistics:
meanX = np.mean(X)
minX = np.min(X)
maxX = np.max(X)
medX = np.median(X)
MADX = np.median(np.abs(X - medX))
s = np.std(X)
sorted_data = np.sort(X)

fig1 = plt.figure(figsize=(20, 6))
plt.subplots_adjust(hspace=0.3)
ax = fig1.add_subplot(211)
ax.set_ylim(0, 1.5)
range_lim = (-0.5, 7.5)  # 0, X.max()+0.3
ax.set_xlim(range_lim)
ax.get_xaxis().tick_bottom()
ax.axes.get_yaxis().set_visible(False)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0.5))
ax.spines['left'].set_color('none')

ax.scatter(X, y, color='black', s=300, c=mc3my_brown, edgecolors=mc3my_brown,
           marker='o')
plt.xlabel(r'$y$', fontsize=18)
plt.suptitle(r"$\mbox{Nombre d'\'echantillons}" + ":n={0}$".format(nb_samples),
             multialignment='center')

ax2 = fig1.add_subplot(212)
ax2.set_xlim(range_lim)
plt.hist(X, bins=10, normed=True, align='mid', color=mc3my_brown)
plt.ylabel(r'$\mbox{Fr\'equence}$', fontsize=18)
plt.xlabel(r'$y$', fontsize=18)
plt.show()

my_saving_display(fig1, dirname, "GammaHist", imageformat)

###############################################################################
# KDE: see https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
#      for more details

fig1 = plt.figure(figsize=(20, 6))
plt.subplots_adjust(hspace=0.3)
ax = fig1.add_subplot(211)
ax.set_ylim(0, 1.5)
range_lim = (-0.5, 7.5)  # 0, X.max()+0.3
ax.set_xlim(range_lim)
ax.get_xaxis().tick_bottom()
ax.axes.get_yaxis().set_visible(False)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0.5))
ax.spines['left'].set_color('none')

ax.scatter(X, y, color='black', s=300, c=mc3my_brown, edgecolors=mc3my_brown,
           marker='o')
plt.xlabel(r'$y$', fontsize=18)
plt.suptitle(r"$\mbox{Nombre d'\'echantillons}" + ":n={0}$".format(nb_samples),
             multialignment='center')

ax2 = fig1.add_subplot(212)
ax2.set_xlim(range_lim)

kde = KDEUnivariate(sorted_data)
kde.fit(bw=0.5, kernel='gau')
x_grid = np.linspace(range_lim[0], range_lim[1], 100)
pdf_est = kde.evaluate(x_grid)

# sns.kdeplot(X, color=mc3my_brown)
plt.plot(x_grid, pdf_est, color='k')
plt.fill_between(x_grid, 0, pdf_est, facecolor=mc3my_brown)
plt.ylabel(r'$\mbox{Fr\'equence}$', fontsize=18)
plt.xlabel(r'$y$', fontsize=18)
plt.show()

my_saving_display(fig1, dirname, "GammaKDE", imageformat)

###############################################################################
# CDF / fonction de repartition:

fig1 = plt.figure(figsize=(20, 6))
plt.subplots_adjust(hspace=0.3)
ax = fig1.add_subplot(211)
ax.set_ylim(0, 1.5)
ax.set_xlim(range_lim)
ax.get_xaxis().tick_bottom()
ax.axes.get_yaxis().set_visible(False)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0.5))
ax.spines['left'].set_color('none')

ax.scatter(X, y, color='black', s=300, c=mc3my_brown, edgecolors=mc3my_brown,
           marker='o')
plt.xlabel(r'$y$', fontsize=18)
plt.suptitle(r"$\mbox{Nombre d'\'echantillons}" + ":n={0}$".format(nb_samples),
             multialignment='center')

ax2 = fig1.add_subplot(212)
ax2.set_xlim(range_lim)
plt.step(sorted_data, np.arange(sorted_data.size, dtype='float') / nb_samples,
         color=mc3my_brown)
# plt.hist(X,bins=200,cumulative=True, normed=True,range=range_lim,
#    histtype='step',align='right')
plt.ylabel(r'$\mbox{Fr\'equence cumul\'ee}$', fontsize=18)
plt.xlabel(r'$y$', fontsize=18)

plt.show()

my_saving_display(fig1, dirname, "Gammaecdf", imageformat)

###############################################################################
# Quantile function:

fig1 = plt.figure(figsize=(20, 6))
plt.subplots_adjust(hspace=0.3)
ax = fig1.add_subplot(211)
ax.set_ylim(0, 1.5)
ax.set_xlim(range_lim)
ax.get_xaxis().tick_bottom()
ax.axes.get_yaxis().set_visible(False)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0.5))
ax.spines['left'].set_color('none')

ax.scatter(X, y, color='black', s=300, c=mc3my_brown, edgecolors=mc3my_brown,
           marker='o')
plt.xlabel(r'$y$', fontsize=18)
plt.suptitle(r"$\mbox{Nombre d'\'echantillons}" + ":n={0}$".format(nb_samples),
             multialignment='center')

ax2 = fig1.add_subplot(212)
ax2.set_xlim(range_lim)

##############
# First case
p = 0.44
q = np.percentile(X, p * 100)

ax2.plot([q, range_lim[0]], [p, p], color=mc3my_brown, linewidth=1.5,
         linestyle="--")
ax2.plot([q, q], [0, p], color=mc3my_brown, linewidth=1.5, linestyle="--")
ax2.annotate(r'$p=%.2f$' % p, xy=(0, p), xycoords='data', xytext=(-23, +6),
             textcoords='offset points', fontsize=18, color=mc3my_brown)
ax2.annotate(r'$F_n^\leftarrow(p)=%.2f$' % q, xy=(q, 0), xycoords='data',
             xytext=(-15, -30), textcoords='offset points', fontsize=18,
             color=mc3my_brown)

##############
# Second case
p = 0.87
q = np.percentile(X, p * 100)

ax2.plot([q, range_lim[0]], [p, p], color=mc3my_brown, linewidth=1.5,
         linestyle="--")
ax2.plot([q, q], [0, p], color=mc3my_brown, linewidth=1.5, linestyle="--")
ax2.annotate(r'$p=%.2f$' % p, xy=(0, p), xycoords='data', xytext=(-23, +6),
             textcoords='offset points', fontsize=18, color=mc3my_brown)
ax2.annotate(r'$F_n^\leftarrow(p)=%.2f$' % q, xy=(q, 0), xycoords='data',
             xytext=(-15, -30), textcoords='offset points',
             fontsize=18, color=mc3my_brown)

plt.step(sorted_data, np.arange(sorted_data.size, dtype='float') / nb_samples,
         color=mc3my_brown)
plt.ylabel(r'$\mbox{Fr\'equence cumul\'ee}$', fontsize=18)
plt.xlabel(r'$y$', fontsize=18)
plt.show()

my_saving_display(fig1, dirname, "GammaQuantiles", imageformat)


###############################################################################
# Bidimensional KDE

execfile('plotspecieskde.py')
my_saving_display(fig_kde, dirname, "KDE2D", imageformat)


###############################################################################
# Correlations figures

rng = np.random.RandomState(42)     # initializing randomness
n_samples = 90
sig_list = [-0.999, -0.8, -.4, 0, 0.4, 0.8, 0.999]
nb_sig = len(sig_list)

fig1 = plt.figure(figsize=(nb_sig, 1.5))
for i in range(nb_sig):
    MySigma = np.eye(2, 2) + np.array([[0, sig_list[i - 1]],
                                      [sig_list[i - 1], 0]])
    X = rng.multivariate_normal(np.array([0, 0]), MySigma, n_samples)
    ax = fig1.add_subplot(1, nb_sig, i + 1)
    plt.title(r" ${0}$".format(sig_list[i - 1]))
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.scatter(X[:, 0], X[:, 1], color='black', s=2, c=mc3my_brown,
               edgecolors=mc3my_brown, marker='o')
plt.tight_layout()
plt.show()


my_saving_display(fig1, dirname, "Correlations2Dessins", imageformat)

###############################################################################
# Correlations figures : negative case

rng = np.random.RandomState(42)
n_samples = 90
theta_list = [np.pi * 1 / 16, np.pi * 2 / 16,
              np.pi * 3 / 16, np.pi * 4 / 16, np.pi * 5 / 16,
              np.pi * 6 / 16, np.pi * 7 / 16]
nb_theta = len(theta_list)

fig1 = plt.figure(figsize=(nb_theta, 1.5))
D = np.diag([1, 0])
for i in range(nb_theta):
    theta = theta_list[i]
    P = np.array([[np.cos(theta), np.sin(theta)],
                 [-np.sin(theta), np.cos(theta)]])
    MySigma = np.dot(np.dot(P, D), np.transpose(P))
    X = rng.multivariate_normal(np.array([0, 0]), MySigma, n_samples)
    ax = fig1.add_subplot(1, nb_theta, i + 1)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.scatter(X[:, 0], X[:, 1], color='black', s=2, c=purple,
               edgecolors=mc3my_brown, marker='o')
    ax.set_ylim(-3, 3)
    ax.set_xlim(-3, 3)
    corr_mat = np.corrcoef(X[:, 0], X[:, 1])
    corr_mat[0, 1]
    plt.title(r"${0}$".format(corr_mat[0, 1]))

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "Correlations2Dessins_bis", imageformat)

###############################################################################
# Correlations figures : positive case

rng = np.random.RandomState(42)

fig1 = plt.figure(figsize=(nb_theta, 1.5))
for i in range(nb_theta):
    theta = -theta_list[i]
    P = np.array([[np.cos(theta), np.sin(theta)],
                 [-np.sin(theta), np.cos(theta)]])
    MySigma = np.dot(np.dot(P, D), np.transpose(P))
    X = rng.multivariate_normal(np.array([0, 0]), MySigma, n_samples)
    ax = fig1.add_subplot(1, nb_theta, i + 1)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.scatter(X[:, 0], X[:, 1], color='black', s=2, c=mc3my_brown,
               edgecolors=mc3my_brown, marker='o')
    ax.set_ylim(-3, 3)
    ax.set_xlim(-3, 3)
    corr_mat = np.corrcoef(X[:, 0], X[:, 1])
    corr_mat[0, 1]
    plt.title(r"${0}$".format(corr_mat[0, 1]))

plt.tight_layout()
plt.show()

my_saving_display(fig1, dirname, "Correlations2Dessins_bis_pos", imageformat)

###############################################################################
#  Zero correlation Example : Gaussian Mixtures

rng = np.random.RandomState(42)
n_samples = 100

fig1, ax = plt.subplots(figsize=(3, 3))
MySigma = 0.01 * np.eye(2, 2)
X1 = rng.multivariate_normal(np.array([0, 1]), MySigma, n_samples)
X2 = rng.multivariate_normal(np.array([1, 0]), MySigma, n_samples)
X3 = rng.multivariate_normal(np.array([1, 1]), MySigma, n_samples)
X4 = rng.multivariate_normal(np.array([0, 0]), MySigma, n_samples)
Z = np.vstack((X1, X2))
Y = np.vstack((X3, X4))
X = np.vstack((Z, Y))
ax.axes.get_yaxis().set_visible(False)
ax.axes.get_xaxis().set_visible(False)
ax.scatter(X[:, 0], X[:, 1], color='black', s=2, c=mc3my_brown,
           edgecolors=mc3my_brown, marker='o')
ax.set_ylim(-1, 2)
ax.set_xlim(-1, 2)
corr_mat = np.corrcoef(X[:, 0], X[:, 1])
debut_titre = r"$\mbox{Corr\'elation }$"
plt.title(debut_titre + r"$ = %.3f$" % corr_mat[0, 1])
plt.show()

my_saving_display(fig1, dirname, "Correlations_4MixtGauss", imageformat)


###############################################################################
#  Zero correlation Example : Circle

rng = np.random.RandomState(42)
n_samples = 400

fig1, ax = plt.subplots(figsize=(3, 3))
MySigma = 0.01 * np.eye(2, 2)
r = 0.8 + 0.4 * rng.rand(1, n_samples)
thetas = 2 * np.pi / n_samples * np.arange(n_samples)
P = np.transpose(np.array(np.vstack((np.cos(thetas), np.sin(thetas)))))

ax.axes.get_yaxis().set_visible(False)
ax.axes.get_xaxis().set_visible(False)
ax.scatter(np.multiply(r, P[:, 0]), r * P[:, 1], color='black', s=2,
           c=mc3my_brown, edgecolors=mc3my_brown, marker='o')
ax.set_ylim(-2, 2)
ax.set_xlim(-2, 2)
corr_mat = np.corrcoef(r * P[:, 0], r * P[:, 1])
debut_titre = r"$\mbox{Corr\'elation }$"
plt.title(debut_titre + r"$ = %.3f$" % corr_mat[0, 1])
plt.show()

my_saving_display(fig1, dirname, "Correlations_Cercle", imageformat)


###############################################################################
# Zero correlation Example : square

rng = np.random.RandomState(42)
n_samples = 400

fig1, ax = plt.subplots(figsize=(3, 3))
X1 = rng.rand(1, n_samples)
X2 = rng.rand(1, n_samples)

ax.axes.get_yaxis().set_visible(False)
ax.axes.get_xaxis().set_visible(False)
ax.scatter(X1, X2, color='black', s=2, c=mc3my_brown, edgecolors=mc3my_brown,
           marker='o')
ax.set_ylim(-1, 2)
ax.set_xlim(-1, 2)
corr_mat = np.corrcoef(X1, X2)
debut_titre = r"$\mbox{Corr\'elation }$"
plt.title(debut_titre + r"$ = %.3f$" % corr_mat[0, 1])
plt.show()

filename = "Correlations_Carre"
image_name = dirname + filename + imageformat
fig1.savefig(image_name)


##############################################################################
# Scatter plot
sns.set_style("white")
iris = sns.load_dataset("iris")
# Next two line needed for avoiding underscore issues in printing with tex...
iris_df = pd.DataFrame(iris)
iris_df.columns = ['sepal length', 'sepal width', 'petal length',
                   'petal width', 'species']

g = sns.PairGrid(iris_df, hue="species", palette="colorblind")
g.map(plt.scatter, color='white')
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)
g.add_legend()

# http://web.stanford.edu/~mwaskom/software/seaborn/tutorial/axis_grids.html

my_saving_display(plt, dirname, "scatter_matrix", imageformat)

###############################################################################
# Spectral decomposition

A = toeplitz([1, 2, 0, 2])
[Dint, Uint] = eigh(A)

idx = Dint.argsort()[::-1]
D = Dint[idx]
U = Uint[:, idx]

print(np.allclose(U.dot(np.diag(D)).dot(U.T), A))

###############################################################################
# Gaussian probability density (pdf)

x = np.linspace(-3., 3.0)
sigma2 = 1
mu = 0

fig1, ax = plt.subplots(figsize=(10, 3))
plt.plot(x, 1 / np.sqrt(2 * np.pi * sigma2) *
         np.exp(- (x - mu) ** 2 / (2 * sigma2)), linewidth=2,
         color=mc3my_brown)
plt.show()

my_saving_display(fig1, dirname, "standardNorm", imageformat)


###############################################################################
# multiple Gaussian probability density (pdf): mean varying

x = np.linspace(-5., 5.0, num=200)
sigma2_tabs = [0.2, 0.5, 1, 2, 5]
mu = 0

fig1, ax = plt.subplots(figsize=(10, 3))
for i, sigma2 in enumerate(sigma2_tabs):
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 1)
    plt.plot(x, 1 / np.sqrt(2 * np.pi * sigma2) *
             np.exp(- (x - mu) ** 2 / (2 * sigma2)), linewidth=2,
             label=r'$\mu={0},\quad   \sigma^2={1} $'.format(mu, sigma2))
    plt.legend()
    plt.show()
    my_saving_display(fig1, dirname, "standardNorm_multiple" + str(i),
                      imageformat)

###############################################################################
# multiple Gaussian probability density (pdf): std varying

fig2, ax1 = plt.subplots(figsize=(10, 3))
ax1.set_xlim(-5, 5)

sigma2 = 1
mu_tabs = [-2, -1, 0, 1, 2]

for i, mu in enumerate(mu_tabs):

    plt.plot(x, 1 / np.sqrt(2 * np.pi * sigma2) *
             np.exp(- (x - mu) ** 2 / (2 * sigma2)), linewidth=2,
             label=r'$\mu={0}, \sigma^2={1} $'.format(mu, sigma2))

    plt.legend()
    plt.show()

    my_saving_display(fig2, dirname, "standardNorm_multiple_bis" + str(i),
                      imageformat)


###############################################################################
# Gaussian probability density funciton in 2D

step = 200
mean_1 = [0, 0]


def covmat_to_scalar(sigma):
    """ convert covariance matrix to scalars"""
    sigmax = np.sqrt(sigma[0, 0])
    sigmay = np.sqrt(sigma[1, 1])
    sigmaxy = sigma[1, 0]
    return sigmax, sigmay, sigmaxy


def angle_scalar_to_covmat(theta, sig1, sig2):
    """ inverse function of the previous one"""
    rotation = np.zeros((2, 2))
    rotation[0, 0] = cos(theta)
    rotation[1, 0] = -sin(theta)
    rotation[0, 1] = sin(theta)
    rotation[1, 1] = cos(theta)
    sigma = rotation.dot(np.diag([sig1 ** 2, sig2 ** 2])).dot(rotation.T)
    return sigma

#######################
# Plot isotropic case

sig0 = np.sqrt(3)
xx = np.linspace(-10, 10, step)
yy = xx
Xg, Yg = np.meshgrid(xx, yy)
Z2_bis = plt.mlab.bivariate_normal(Xg, Yg, sigmax=sig0,
                                   sigmay=sig0, mux=mean_1[0],
                                   muy=mean_1[1], sigmaxy=0.0)

fig1 = plt.figure(dpi=90)
ax = fig1.add_subplot(111, projection='3d')
ax.plot_surface(Xg, Yg, Z2_bis, cmap='Oranges', rstride=3, cstride=3,
                alpha=0.9, linewidth=0.5)
ax.set_zlim(0, 0.06)
plt.show()

my_saving_display(fig1, dirname, "iso_gaussian", imageformat)


#######################
# Plot anisotropic case

sig1 = 1.
sig2 = 3.
thetas = [0., pi / 5., 2. * pi / 5., 3. * pi / 5., 4. * pi / 5.]

for i, theta in enumerate(thetas):

    sigma = angle_scalar_to_covmat(theta, sig1, sig2)
    sigmax, sigmay, sigmaxy = covmat_to_scalar(sigma)
    Z2_ter = plt.mlab.bivariate_normal(Xg, Yg, sigmax=sigmax,
                                       sigmay=sigmay,
                                       mux=mean_1[0], muy=mean_1[1],
                                       sigmaxy=sigmaxy)
    print(Z2_ter.max())
    fig1 = plt.figure(dpi=90)
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(Xg, Yg, Z2_ter, cmap='Oranges', rstride=3, cstride=3,
                    alpha=0.9, linewidth=0.5)
    ax.set_zlim(0, 0.06)
    plt.show()
    my_saving_display(fig1, dirname, "aniso_gaussian" + str(i), imageformat)


###############################################################################
# testing Cholevsky decomposition in numpy
A = np.random.randn(4, 4)
B = np.dot(A, np.transpose(A))
np.linalg.det(B)  # semi definite positive then
L = np.linalg.cholesky(B)
print (np.dot(L, np.transpose(L)) - B)
