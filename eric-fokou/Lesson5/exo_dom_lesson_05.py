
# coding: utf-8

# ### Hackathon

# *** Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et la pratique du dépassement d'honoraires ? ***
# 
# ***Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ? ***
# 
# ***Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?***

# In[222]:

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from pandas.tools.plotting import radviz, scatter_matrix
from scipy.stats import gaussian_kde
from os import mkdir, path
import scipy.stats
from scipy.stats import pearsonr
from scipy.stats import norm
get_ipython().magic(u'matplotlib inline')
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
dirname = "srcimages/"
if not path.exists(dirname):
    mkdir(dirname)
imageformat = '.jpg'


def my_saving_display(fig, dirname, filename, imageformat):
    """saving faster"""
    dirname + filename + imageformat
    image_name = dirname + filename + imageformat
    fig.savefig(image_name)


# *** loading of data ***

# In[223]:

depassement_honoraires = "Data/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2013.xls"
densite_medecins_specialite = "Data/Medecins.csv"

df_depassement_honoraires = pd.read_excel(depassement_honoraires, sheetname=2, na_values='nc',encoding='utf-8')
df_densite_medecins_specialite = pd.read_csv(densite_medecins_specialite,encoding='utf-8')


# *** affichage du schema ***

# In[224]:

print "df_depassement_honoraires\n"
print df_depassement_honoraires.dtypes
print df_depassement_honoraires.shape
print 
print "df_densite_medecins_specialite\n"
print df_densite_medecins_specialite.dtypes
print df_densite_medecins_specialite.shape


# ### Traitement des donnees dépassement d'honoraires

# ***suppression des valeurs null***

# In[225]:

df_depassement_honoraires = df_depassement_honoraires.dropna(subset=['DEPASSEMENTS (euros)'])
print(df_depassement_honoraires.shape)


# In[226]:

df_depassement_honoraires


# *** nettoyage des champs SPECIALISTES et  DEPARTEMENT***

# In[227]:

df_depassement_honoraires['SPECIALISTES'] = df_depassement_honoraires['SPECIALISTES'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))
df_depassement_honoraires['DEPARTEMENT'] = df_depassement_honoraires['DEPARTEMENT'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))

df_depassement_honoraires['SPECIALISTES'] = df_depassement_honoraires['SPECIALISTES'].str.extract('[\d]+- ([\w\s-]+)', expand=False)
df_depassement_honoraires['DEPARTEMENT'] = df_depassement_honoraires['DEPARTEMENT'].str.extract('[\d]+- ([\w\s-]+)', expand=False)


# In[228]:

df_depassement_honoraires = df_depassement_honoraires.dropna(subset=['SPECIALISTES'])
df_depassement_honoraires = df_depassement_honoraires.dropna(subset=['DEPARTEMENT'])
df_depassement_honoraires


# In[229]:

df_depassement_honoraires = df_depassement_honoraires.set_index(['SPECIALISTES', 'DEPARTEMENT'])
df_depassement_honoraires.ix[0:20]
df_depassement_honoraires_clean = df_depassement_honoraires["DEPASSEMENTS (euros)"]
df_depassement_honoraires_clean.to_csv('Data\df_depassement_honoraires.csv',header = True)


# In[230]:

#df_depassement_honoraires_clean.plot(kind='pie', subplots=True, figsize=(20, 15))


# ### Traitement des donnees densite medecins specialite 

# *** suppression des valeurs null ***

# In[231]:

df_densite_medecins_specialite = df_densite_medecins_specialite.dropna(subset=['effectifs'])
print(df_densite_medecins_specialite.shape)


# In[232]:

df_densite_medecins_specialite


# *** nettoyage des champs SPECIALISTES et zone_inscription ***

# In[233]:

df_densite_medecins_specialite['zone_inscription'] = df_densite_medecins_specialite['zone_inscription'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))
df_densite_medecins_specialite['specialite'] = df_densite_medecins_specialite['specialite'].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))

df_densite_medecins_specialite['zone_inscription'] = df_densite_medecins_specialite['zone_inscription'].str.extract('[\d]+ - ([\w\s-]+)', expand=False)


# In[234]:

df_densite_medecins_specialite = df_densite_medecins_specialite.dropna(subset=['specialite'])
df_densite_medecins_specialite = df_densite_medecins_specialite.dropna(subset=['zone_inscription'])
df_densite_medecins_specialite = df_densite_medecins_specialite.set_index(['specialite', 'zone_inscription'])
df_densite_medecins_specialite_clean = df_densite_medecins_specialite["effectifs"]
df_densite_medecins_specialite_clean.to_csv('Data\Medecin_clean.csv',header = True)
df_densite_medecins_specialite_clean.ix[0:20]


# In[ ]:



