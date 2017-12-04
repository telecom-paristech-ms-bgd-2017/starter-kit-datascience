import requests
from bs4 import BeautifulSoup
import pandas
import time
import pandas as pd
import re
import os
from os import walk

path = "../sources/"

# url_base = 'https://www.data.gouv.fr/s/resources/depenses-d-assurance-maladie-hors-prestations-hospitalieres-donnees-nationales/20160913-134543/N201607.csv'

#   df.columns = ['act_coe',	'act_dnb',	'asu_nat',	'cpl_cod',	'dep_mon',	'exe_spe',	'exe_spe1',	'exe_stj1',
#              'l_asu_nat',	'l_cpl_cod',	'l_exe_spe',	'l_exe_spe1 ',	'l_exe_stj1',	'l_pre_spe',
#              'l_pre_spe1',	'l_pre_stj1',	'l_prs_nat',	'l_serie',	'pre_spe',	'pre_spe1',	'pre_stj1',
#              'prs_nat',	'rec_mon',	'rem_date',	'rem_mon ',	'rem_tau',	'serie',	'sns_date']



for f in reversed(next(walk(path))[2]):
    print(f)

path_tab5 = 'rpps-medecins-tab5_30211942070628.csv'
path_tab7 = 'rpps-medecins-tab7_31092067859498.csv'
path_tab5b = 'rpps-medecins-tab5_31101614232043.csv'
path_tab_r1 = 'R2015_sans_lib/R201501_sanslib.CSV'
path_desc = 'descriptif_table_R.xls'
path_tab_n7 = 'N201607.csv'

#df = pd.read_csv(url_base, delimiter=';', index_col=False, header=1, skip_blank_lines=True, na_values=["NA"])

# df_r1 = pd.read_csv(path + path_tab_r1, sep=';', na_values=["NA"], encoding='latin-1', nrows=100)
# df_n7 = pd.read_csv(path + path_tab_n7, sep=';', na_values=["NA"], encoding='latin-1', nrows=100)

#   Import Description
# df_desc_pre_spe = pd.read_excel(path_desc, sheetname=10)

# df_r1[['cpam', 'pre_spe', 'pre_spe1', 'dep_mon']][:5]
# df_desc_pre_spe[['pre_spe', 'l_pre_spe']]

# df_n7[:5]



'''
#   Import DataGouv
df_r = {}
for i in range(12):
    path_tab_r_i = '/Users/Wes/Desktop/Hackathon/R2015_sans_lib/R2015' + ('00'+str(1))[-2:] + '_sanslib.CSV'
    df_r[i] = pd.read_csv(path_tab_r_i, sep=',', na_values=["NA"], encoding='latin-1')
'''


'''
#   Import Drees Tableaux
df5 = pd.read_csv(path_tab5, sep=',', na_values=["NA"], encoding='latin-1', header=5)
df7 = pd.read_csv(path_tab7, sep=',', na_values=["NA"], encoding='latin-1', header=3)
'''

'''
df5 = df5.dropna()
df7 = df7.dropna()

list_regions = df5['SECT.ACTIVITE'].values.tolist()
list_secteur_activite = list(df5.columns.values)
'''

'''
# try pivot
for el in list_secteur_activite:
    list_secteur_activite_str = list_secteur_activite_str + ',' + el

df5_pivot = df5.pivot(list_secteur_activite).reset_index()

df5_final = pd.melt(df5_pivot, id_vars=['REGION ACTIVITE'], value_vars=list_regions)
'''


#after transpose
#df5.drop_duplicates().shape