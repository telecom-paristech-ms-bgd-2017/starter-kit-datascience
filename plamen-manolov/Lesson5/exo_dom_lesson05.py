# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns
from pandas.tools.plotting import radviz, scatter_matrix
import collections
#import binning



#importation des données#

path = "http://www.ameli.fr/fileadmin/user_upload/documents/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2014.xls"
data = pd.read_excel(path,sheetname=[1,2,3,4,5,6])
df = data[2]

#supression des NaN
df = df.replace('nc','NaN').dropna()

#extraction code Numérique
df = df[df['DEPARTEMENT'].str.contains('- ')]
#df = df[df['SPECIALISTES'].str.contains('- ')]
df = df[df['Spécialistes'].str.contains('- ')]

dep = pd.DataFrame([[x] + x.split('- ') for x in df['DEPARTEMENT']], columns=['DEPARTEMENT', 'num_dep', 'name_dep'])

#spec = pd.DataFrame([[x] + x.split('- ') for x in df['SPECIALISTES']], columns=['SPECIALISTES', 'num_spec', 'name_spec'])
spec = pd.DataFrame([[x] + x.split('- ') for x in df['Spécialistes']], columns=['Spécialistes', 'num_spec', 'name_spec'])




df = pd.concat([df, dep, spec], axis=1, join='inner')

df['num_dep'] = df['num_dep'].str.replace('^0', '').str.replace('B', '.5').str.replace('A', '.25').astype('float')

df['num_spec'] = df['num_spec'].replace('^0', '').astype('float')


df['DEPASSEMENTS (Euros)'] = df['DEPASSEMENTS (Euros)'].astype('float')


# ne garder que les lignes avec EFFECTIF > 0
df = df[df['EFFECTIFS'] > 0]

columns = ['num_spec', 'NOMBRE DE DEPASSEMENTS','DEPASSEMENT MOYEN (euros)', 'DEPASSEMENTS (euros)', 'EFFECTIFS']

dat = df[columns]

plt.style.use('ggplot')
scatter_matrix(dat, diagonal='kde', figsize=(15,13))

#correlation entre les variables
#corr_mat = dat.corr()
#plt.figure(figsize=(9,9))
#sns.heatmap(corr_mat, square=True, vmax=0.8)


#plt.figure(figsize=(12,12))
#radviz(dat, 'num_spec')


#visualisation par spécialité

groups = df.groupby(['name_spec'])
plt.figure(figsize=(12,12))
plt.title("spécialistés")
plt.xlabel('effectifs moyen (departements)')
plt.ylabel('depassement moyen')
x = []
y = []
for name,group in groups:
    moy_eff = group['EFFECTIFS'].mean()
    moy_dep = group['DEPASSEMENTS (Euros)'].mean()
    x.append(moy_eff)
    y.append(moy_dep)
    plt.plot(moy_eff, moy_dep, 'o', label=name)


#bins = np.linspace(min(x),max(x),9)
#count = np.binning_1D(bins,x,5,2,1)
#binning = np.binning_1D(bins,x,5,2,y)

#smooth = binning/count
#plt.plot(bins,smooth,'r',lw=2)


c = np.column_stack((np.asarray(x),np.asarray(y)))
data = pd.DataFrame(c, columns=['Effectifs en moyens','Depassements moyens'])

sns.jointplot('Effectifs en moyens','Depassements moyens', data=data, kind="reg", color="r", size=10)
