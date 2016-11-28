import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns
from pandas.tools.plotting import radviz, scatter_matrix
import collections
 #%matplotlib inline

# https://www.data.gouv.fr/fr/datasets/honoraires-des-professionnels-de-sante-liberaux/
path = "Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls"

data = pd.read_excel(path, sheetname=[1, 2, 3, 4, 5, 6])

df = data[2]

# enlever les nan
df = df.replace('nc', np.nan).dropna()

# extraire les codes numeriques
df = df[df['DEPARTEMENT'].str.contains('- ')]
df = df[df['SPECIALISTES'].str.contains('- ')]

dep = pd.DataFrame([[x] + x.split('- ') for x in df['DEPARTEMENT']],
                       columns=['DEPARTEMENT', 'num_dep', 'name_dep'])

spec = pd.DataFrame([[x] + x.split('- ') for x in df['SPECIALISTES']],
                        columns=['SPECIALISTES', 'num_spec', 'name_spec'])

df = pd.concat([df, dep, spec], axis=1, join='inner')

# ne garder que les lignes avec EFFECTIF > 0
df = df[df['EFFECTIFS'] > 0]

dat = df[['num_spec', 'NOMBRE DE DEPASSEMENTS',
              'DEPASSEMENT MOYEN (euros)', 'DEPASSEMENTS (euros)', 'EFFECTIFS']]
corr_mat = dat.corr()

plt.figure(figsize=(9,9))
sns.heatmap(corr_mat, square=True, vmax=0.8)


print '########################## DEPASSEMENT PAR SPECIALITE #####################################'
print ''
grouped_by_spec = df[['name_spec', 'DEPASSEMENT MOYEN (euros)']].groupby(['name_spec']).mean()
grouped_by_spec = grouped_by_spec.sort_values('DEPASSEMENT MOYEN (euros)',ascending=False)
print grouped_by_spec.head(15)
print ''
print '############################DEPASSEMENT PAR DEP ##################################'
print ''
grouped_by_dep = df[['num_dep', 'DEPASSEMENT MOYEN (euros)']].groupby(['num_dep']).mean()
grouped_by_dep = grouped_by_dep.sort_values('DEPASSEMENT MOYEN (euros)',ascending=False)
print grouped_by_dep.head(15)
print ''
print '##################################################################################'

#Fichier Densité

#!/usr/bin/env python
#-*- coding: utf-8 -*-

path = "densite2014.csv"
df_densite = pd.read_csv(path,encoding='latin-1', skiprows=[0, 1, 2, 3, 5])
df_densite = df_densite[df_densite['SPECIALITE'].str.contains('- ')]

noms = list(df_densite.columns.values)


print '###################### DENSITE PAR DEP ##################################################'
print ''
df_densite_dep = df_densite[['SPECIALITE',noms[1]]].sort_values(noms[1],ascending=False)
print df_densite_dep.head(15)
print '##################### DENSITE PAR SPECIALITE ############################################'
print ''
df_densite_specialite = df_densite.mean()[2:]
print df_densite_specialite.sort_values().head(15)
print '##################################################################################'
print ''