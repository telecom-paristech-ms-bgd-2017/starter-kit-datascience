# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
plt.close()

# Obtention des données
# ------------------------------------------------------

# le fichier se charge mal, option low_memory nécessaire
url = r'C:/Users/Justyna/Code-Python/aliments.csv'

#df_aliments = pd.read_csv(url, delimiter='\t', low_memory=False)

df_aliments = pd.read_csv(url, delimiter='\t', low_memory=False)



def infos_DataFrame(df):
    """
    1°) renvoie les statistiques de base sur le DF
    2°) imprime la liste des colonnes d'un DF
    3°) imprime les 20 premières valeurs
    4°) compte les valeurs nulles de chaque colonne
    5°) compte le nombre de valeurs uniques
    6°) affichage des histogrammes des colonnes numériques
    7°) sépare en deux le DF en : 1 df numérique, 1 df non-numérique
    """
    # 20 premières lignes du DF
    print(df.head(20))
    print('------------------------------------------------------')
    # Pour chaque colonne du DF, statistiques descriptives + nombre de valeurs manquantes + nombre de valeurs uniques
    for j in range(df.columns.shape[0]):
        print(df.columns[j], "( Col num", j, ") : ")
        print(df[df.columns[j]].describe())
        print("\tNombre N/A : ", df[df.columns[j]].isnull().sum())
        print('------------------------')
    print('------------------------------------------------------')

    # séparation du df en 2 : 1 df avec les colonnes numériques et 1 df sans les colonnes numériques
    df_hist = df.select_dtypes(exclude=['object'])
    df_str = df.select_dtypes(include=['object']).astype('str')
    # pour chaque colonne numérique, production d'un histogramme, affichage des valeurs > = et < 0 et si besoin affichage du nombre de valeurs manquantes
    for i in range(len(df_hist.columns)):
        print(df_hist.columns[i], " : ")
        print("\tVal sup à zéro : ", df_hist[df_hist[df_hist.columns[i]] > 0].count()[0])
        print("\tVal nulles : ", df_hist[df_hist[df_hist.columns[i]] == 0].count()[0])
        print("\tVal inf à zéro : ", df_hist[df_hist[df_hist.columns[i]] < 0].count()[0])
        print("\tNombre de valeurs uniques : ", len(np.unique(df_hist[df_hist.columns[i]])))
        # print("\tNombre N/A : ", df_hist[df_hist.columns[i]].isnull().sum())
        print('------------------------------------------------------')
        fig = plt.figure(i)
        df_hist[df_hist.columns[i]].hist()
        plt.title(df_hist.columns[i])
        plt.show()
    # pour chaque colonne non-numérique, affichage du nombre de valeurs manquantes
    for i in range(len(df_str.columns)):

        print(df_str.columns[i], " : ")
        print("\tNombre N/A : ", df_str[df_str.columns[i]].isnull().sum())
        print("\tNombre de valeurs uniques : ", len(np.unique(df_str[df_str.columns[i]])))
    return df_hist, df_str



# ---------------------------------------
# Statistiques descriptives du fichier

df_alim, df_alim_str = infos_DataFrame(df_aliments)

# L'OMS recommande de consommer 6 grammes de sel par jour.
# On va taxer les aliments qui contiennent plus de 10% de la ration de sel recommandée par jour pour cent grammes.

df_trop_sel = df_aliments[df_aliments['sodium_100g'].notnull()]

df_trop_sel.sodium_100g.hist(bins=[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,10], ylabelsize=2000, color='blue')
plt.title('Aliments salés à taxer')
plt.plot([0.6, 0.6], [0, 2000], color='red', linestyle='--', linewidth = 2)
plt.show()

df_trop_sel[df_trop_sel['sodium_100g']> 0.6].count()

# On peut taxer 1840 produits pour leur teneur en sel

df_trop_sel_taxe = df_trop_sel[df_trop_sel['sodium_100g']> 0.6]
df_trop_sel_taxe = df_trop_sel_taxe.rename(columns={'sodium_100g': 'sel>0.6%'})

# On va regarder dans quels pays ces aliments taxés sont produits
# On garde les produits dont le lieu de fabrication est renseigné
df_trop_sel_taxe_origine = df_trop_sel_taxe[df_trop_sel_taxe['manufacturing_places'].notnull()]

# Les lieux de production sont très divers. On ajoute une colonne pays
df_trop_sel_taxe_origine['pays'] = pd.Series(df_trop_sel_taxe_origine['manufacturing_places'].apply(lambda x: x.split(',')[-1]))

# On nettoie les données pour avoir une statistique propre
df_trop_sel_taxe_origine['pays'].replace("^\s", "", regex=True, inplace=True)
df_trop_sel_taxe_origine['pays'].replace("\\.", "", inplace=True)
df_trop_sel_taxe_origine['pays'] = df_trop_sel_taxe_origine['pays'].str.lower()

df_trop_sel_taxe_origine['pays'].replace("denmark", "danemark", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("thailand", "thailande", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("thaïlande", "thailande", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("italia", "italie", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("italy", "italie", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("poland", "pologne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("francia", "france", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("fabriqué en france", "france", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("españa", "espagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("spain", "espagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("alemania", "allemagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("deutschland", "allemagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("malaysia", "malaisie", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("the netherlands", "pays-bas", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("united kingdom", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("polska", "pologne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("países bajos", "pays-bas", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("neckarsulm", "allemagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("great britain", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("unterhaching", "allemagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("valencia", "espagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("china", "chine", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("u.e", "ue", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("u.k", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("ecosse", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("murcia", "espagne", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("u.k", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("u.k", "uk", inplace=True)
df_trop_sel_taxe_origine['pays'].replace("la rioja", "espagne", inplace=True)

liste_regions = ['alsace', 'cantal', 'dijon', 'bretagne', 'nord pas de calais', 'pays de la loire',
                 'pays-de-la-loire', 'normandie', "ste fromagère d'annecy"]

liste_france = ['france']*len(liste_regions)

df_trop_sel_taxe_origine['pays'].replace(liste_regions, liste_france, inplace=True)

liste_pays = ['allemagne', 'france', 'belgique', 'uk', 'ue', 'norvège', 'pays-bas', 'pologne', 'vietnam',
              'portugal', 'espagne', 'thailande', 'vietnam', 'u.s.a', 'suisse', 'grèce', 'italie', 'india',
              'chine', 'danemark', 'japon', 'luxemburgo', 'malaisie' ]

for word in liste_pays:
    expr = ".*"+word+".*"
    df_trop_sel_taxe_origine['pays'].replace(expr, word, inplace=True, regex=True)

# on décompte les produits trop salés par pays
df_taxe_sel_pays =  df_trop_sel_taxe_origine[['pays', 'sel>0.6%']].groupby(by='pays').count().sort_values(by='sel>0.6%', ascending=False)

# on regroupe les pays qui fournissent très peu de produits (moins de 1%) sous le label "autres pays"
nb = df_taxe_sel_pays[df_taxe_sel_pays['sel>0.6%']<5].count()
print(nb)
taille = len(df_taxe_sel_pays)
df_taxe_sel_pays.iloc[taille-1, 0] = nb[0]
df_taxe_sel_pays = df_taxe_sel_pays[df_taxe_sel_pays[df_taxe_sel_pays.columns[0]]>4]

old_index = df_taxe_sel_pays.index
new_index = list(old_index[0:len(old_index)-1])
new_index.append("autres pays")
df_taxe_sel_pays = df_taxe_sel_pays.reindex(new_index)
taille = len(df_taxe_sel_pays)
df_taxe_sel_pays.iloc[taille-1,0] = nb[0]
df_taxe_sel_pays = df_taxe_sel_pays.astype(int)

# on imprime le résultat final
print(df_taxe_sel_pays)

# on trace un camembert
fig2 = plt.figure(2)
labels = 'Python', 'C++', 'Ruby', 'Java'
sizes = [215, 130, 245, 210]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = [0.2]*taille
#explode = (0.1)*taille  # explode 1st slice
plt.title('Taxe sur les aliments trop salés : répartition par pays', loc="left")
# Plot
plt.pie(df_taxe_sel_pays, labels=df_taxe_sel_pays.index, autopct='%1.1f%%', shadow=True,
        pctdistance=1.1, labeldistance=1.2, frame=False, wedgeprops=None, textprops=None, startangle=120)

plt.axis('equal')
plt.show()

