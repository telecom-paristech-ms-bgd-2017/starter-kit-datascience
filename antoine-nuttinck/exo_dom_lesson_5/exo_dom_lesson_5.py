# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:28:29 2016

@author: Antoine
"""

import pandas as pd

# Dans un terminal file -bi filename.csv pour connaître l'encoding
# Ici les fichiers sont encodés en iso8859-1

path_secu = "D:\Antoine\Documents\MS Big Data\Kit Big Data\exo_dom_lesson_5" + \
                "\\R201512.csv"
secu_col_extract = ["cpam", "region", "pre_spe", "exe_spe", "dep_mon"]
path_dens = "D:\Antoine\Documents\MS Big Data\Kit Big Data\exo_dom_lesson_5\\" \
            + "rpps-medecins-tab7_30165051197645.csv"
data_secu = pd.read_csv(path_secu,
                        sep=";",
                        dtype=str,
                        usecols=secu_col_extract,
                        nrows=500000,
                        decimal=",",
                        thousands = ".",
                        encoding="iso8859-1")
data_secu.describe()
data_dens = pd.read_csv(path_dens,
                        sep=";",
                        header=3,  # index_col=0,
                        dtype=float,
                        converters={'SPECIALITE': str},
                        encoding="iso8859-1",
                        error_bad_lines=False)

# \b([0-8][0-9]|97*[0-5]|976|2[A-B])(?= - )
dep_df = data_dens['SPECIALITE'].str.extract(r'\b(?P<n_dep>[0-8][0-9]|97*[0-5]|976|2[A-B])*(?P<l_dep>.*)', expand=False).dropna()
# enlever les tirets dans le dataframe dep_df /s-/s?
data_dens['departement'] = dep_df['l_dep']
data_dens.dropna(inplace=True)

data_dens['dep_idx'] = dep_df['n_dep'].str.replace('2A', '20') \
                                .str.replace('2B', '20') \
                                .dropna()
                                # type(int)

data_dens_melted = pd.melt(data_dens, id_vars='dep_idx', var_name='spécialité', value_name='Densité de médecins')

data_dens_idx = data_dens_melted.groupby(('dep_idx', 'spécialité')).sum()

# pour merger sur 2 columns : créer un multindex en faisant par exemple de groupby
# puis merger sur l'index

# utiliser la table de correspondance qui se trouve dans Github dans
# fichiers_supplementaires.rpps/correspondance_rpp

# group by departement et spécialité

# merger par la clé avec la table de la densité des médecins
# inner join car il peut ne pas avoir de dépassement d'honoraire 
# ds un département alors qu'il y a une densité de médecins

# Pour lancer ipython avec matplotlib dans un terminal : ipython --matplotlib

# Voir plotly pour la vizualisation

# Utiliser scatter matrix pour essayer de deviner les relations entre les différentes variables
