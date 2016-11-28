# -*- coding: utf-8 -*-
"""
Author Nux

###############################################################################
### Depassement d'honoraires : variable dep_mon
### Cette notion ne concerne que les honoraires des medecins.
###############################################################################

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

###############################################################################
###   Chargement densites medecins par departement
###############################################################################

d_Med_DF = pd.read_csv('/home/nux/Documents/INFMDI721/Exo_sante/\
rpps-medecinsCSV.csv', sep=',', header=4)

# Dept 1 = ix 22, Dept fin = ix122
medecins = d_Med_DF.ix[22:122]
#d_Med_DEP_DF_altered = df.row.str.extract("(?P<num_dep>\d{2}|\d{3})\s?-\s?(?P<Nom_dep>[A-Za-z-' ]*)")

# Split de la premiere colonne pour isoler numéro de departement
df = pd.Series(medecins['SPECIALITE'])
df2 = df.str.split(' - ', expand=True)
df2.rename(columns={0: 'Num_dep', 1: 'Nom_dep'}, inplace=True)
medecins = pd.concat([df2, medecins], axis=1)
#medecins = pd.concat([medecins['Num_dep'].astype(int), medecins], axis=1)
# on a une colonne Num_dep
#print(d_Med_DEP_DF.head())

###############################################################################
###   Chargement densites de population par département
###############################################################################

d_pop_DF = pd.read_csv('/home/nux/Documents/INFMDI721/Exo_sante/estim-pop-dep-2015.csv',\
                       sep=',', header=4, usecols=[0, 7])

for i in range(9):
    d_pop_DF.iloc[i, 0] = '0' + d_pop_DF.get_value(index=i, col='Unnamed: 0')

d_pop_DF = d_pop_DF.set_index('Unnamed: 0')


###############################################################################
###   Chargement depassement d'honoraires par caisse d'assurance maladie
###############################################################################

dep_mon = pd.read_csv('/home/nux/Documents/INFMDI721/Exo_sante/\
R2015_sans_lib/R201501_sanslib.CSV', sep=';', header=0,\
usecols=['cpam', 'dep_mon'], low_memory=False, thousands='.', decimal=',')


###############################################################################
###   Match CAM - departements : chargement d'un fichier RNIAM_RGSLM
###############################################################################

CAMtoDpt = pd.read_csv('/home/nux/Documents/INFMDI721/Exo_sante/\
DAMIR-master/fichiers_supplementaires/population_protegee/\
RNIAM_RGSLM_JANVIER2014.csv', header=4, usecols=['cpam', 'dpt'], engine='python', skipfooter=4)
#print(match_cam_dep_DF.head())


###############################################################################
### Ajout des num de département sur le DF des dépassements d'honoraires
###############################################################################

# Transtypage et complétion des numéros de département dans CAMtoDpt
CAMtoDpt = pd.concat([CAMtoDpt['cpam'], CAMtoDpt['dpt'].astype(str)], axis=1)

for i in range(9):
    CAMtoDpt.iloc[i, 1] = '0' + CAMtoDpt.get_value(index=i, col='dpt')

# Merge sur numéro de CAM
dep_mon = pd.merge(dep_mon, CAMtoDpt, on='cpam')

###############################################################################
### Merge : ajout des numéros de département sur le fichier des dépassements
### d'honoraires.
###############################################################################

# Merge sur numéro de département : pour un département du fichier medecins,
# on associe la somme des dépassements d'honoraires du département concerné.
# dep_mon = pd.merge(medecins, dep_mon, left_on='Num_dep', right_on='dpt')

medecins['depassement dpt'] = np.zeros(len(medecins), dtype=np.int)
medecins = medecins.set_index('Num_dep')

# Somme des honoraires par département
for s in medecins.index.values:
    medecins.ix[s, 'depassement dpt'] = dep_mon.groupby('dpt')['dep_mon'].sum()[s]

###############################################################################
### Plot en parallèle des colonnes dépassement et densité de médecins
###############################################################################

# Pour pondérer les dépassements d'honoraires par la densité de population par
# département, on joint la densite de population par departement.
medecins = pd.concat([medecins, d_pop_DF], axis=1)

# Ordre ascendant du montant des dépassements d'honoraires
medecins['dep unitaire'] = medecins['depassement dpt'] / medecins['Total']
medecins = medecins.sort(['dep unitaire'])

# Correlation
corr = pearsonr(medecins['Generalistes'], medecins['dep unitaire'])[0]

# Plot
fig = plt.figure(figsize=(8, 6))
plt.plot(np.arange(1, 102), medecins['dep unitaire'], 'b')
plt.plot(np.arange(1, 102), medecins['Generalistes'] / 20, 'k')
plt.legend(loc='upper left')
plt.text(6, 15, r'correlation: $0,23$', fontsize=15)
plt.show()
