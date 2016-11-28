import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

#############################################################
# Lecture et nettoyage du fichier de Janvier 2015 de la cpam
#############################################################

# Contruction de la dataframe
df = pd.read_csv(
        "/Users/lolo/Développement/Python/CoursTelecom/starter-kit-datascience/laurent-hericourt/Lesson5/R2015/R201501_sanslib.csv",
        sep=";", encoding='latin-1')

df = df.dropna()
df = df.drop(
        ["SERIE", "prs_nat", "sns_date", "asu_nat", "cpl_cod", "ben_qlt", "REM_TAU", "pre_spe", "pre_spe1", "exe_stj1",
         "top_slm", "act_dnb", "act_coe"], 1)
df['cpam'] = df[df['cpam'] < 971].apply(axis=1, func=lambda x: str(x['cpam'])[:2])


def convert_string_to_float(montant):
    new_montant = montant.replace(",", ".")
    if new_montant.count('.') > 1:
        last_point = new_montant.rfind('.')
        new_montant = new_montant[:last_point].replace(".", "") + new_montant[last_point:]

    return float(new_montant)


df['dep_mon'] = df.apply(axis=1, func=lambda x: convert_string_to_float(x['dep_mon']))

####################################################
# Groupby de ce fichier suivant différents critères
####################################################

aggregation = {
    'moyenne euros': 'mean',
    'somme euros': 'sum',
    'nombre total': 'count',
    'nombre dep': lambda x: len([elt for elt in x if elt > 0]),
    'ratio %': lambda x: 100 * len([elt for elt in x if elt > 0]) / x.count()
}

df_groupby_global = df['dep_mon'].groupby([df['cpam'], df['exe_spe']]).agg(aggregation).reset_index()

df_groupby_departement = df['dep_mon'].groupby([df['cpam']]).agg(aggregation).reset_index()

##################################################################################################
# Lecture et nettoyage du fichier de la densité des médecins par département et spécialisation
##################################################################################################

df_densite = pd.read_csv(
        "/Users/lolo/Développement/Python/CoursTelecom/starter-kit-datascience/laurent-hericourt/Lesson5/Densites_medecins_2015.csv",
        sep=";", encoding='latin-1')

regex = re.compile(r"([0-9]+)")

df_densite['departement'] = df_densite.apply(axis=1, func=lambda x: int(re.findall(regex, x['departement'])[0]))
col_4 = ['4-a', '4-b', '4-c', '4-d', '4-e', '4-f', '4-g', '4-h', '4-i']
col_7 = ['7-a', '7-b']
df_densite['4'] = df_densite.apply(axis=1, func=lambda x: sum([x[indice] for indice in col_4]))
df_densite = df_densite.drop(col_4, 1)
df_densite['7'] = df_densite.apply(axis=1, func=lambda x: sum([x[indice] for indice in col_7]))
df_densite = df_densite.drop(col_7, 1)

liste_colonnes_densite = df_densite.columns.values[1:].tolist()
df_densite_melt = pd.melt(df_densite, id_vars=['departement'], value_vars=liste_colonnes_densite)
df_densite_melt = df_densite_melt.rename(columns={'departement': 'cpam', 'variable': 'exe_spe'})

df_groupby_global['exe_spe'] = df_groupby_global['exe_spe'].apply(str)
df_densite_melt['cpam'] = df_densite_melt['cpam'].apply(str)

##################################################################################################
# Jointure des deux sources précédentes pour calculer leur corrélation
##################################################################################################

# Résultat par département et spécialité
resultat_detaille = pd.merge(df_densite_melt, df_groupby_global, how='inner', on=['cpam', 'exe_spe'])

plt.plot(resultat_detaille['value'], resultat_detaille['ratio %'], '*', label="Data")
plt.xlim(0, 50)
plt.show()

# Résultat par département
df_densite_mel_departement = df_densite_melt[df_densite_melt['exe_spe'] == "0"]

resultat_departement = pd.merge(df_densite_mel_departement, df_groupby_departement, how='inner', on=['cpam'])

value_norme = (resultat_departement['value'] - np.mean(resultat_departement['value'])) / np.std(
        resultat_departement['value'])
ratio_norme = (resultat_departement['ratio %'] - np.mean(resultat_departement['ratio %'])) / np.std(
        resultat_departement['ratio %'])

plt.plot(value_norme, ratio_norme, '*', label="Data")
plt.show()

print(np.corrcoef(value_norme, ratio_norme)[1, 0])
