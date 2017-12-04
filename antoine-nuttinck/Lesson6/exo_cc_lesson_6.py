# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:37:01 2016

@author: Antoine
"""
import pandas as pd
import matplotlib.pyplot as plt


def findInFood(junk100g):
    alimentsDB_path = u'aliments.csv'

    alimentsDB = pd.read_csv(alimentsDB_path,
                             delimiter='\t',
                             usecols=['code',
                                      'generic_name',
                                      'product_name',
                                      junk100g,
                                      'categories_fr',
                                      'stores',
                                      'countries_fr'])
# , 'fat_100g', 'saturated-fat_100g', 'silica_100g'])

    alimentsDB.dropna(subset=['product_name', 'code'], inplace=True)
    alimentsDB = alimentsDB.set_index('code')

    # /!\ Certains aliments contiennent plus de 100g de qqc sur 100 --> cleaner
    al_cleaned = alimentsDB[alimentsDB[junk100g] < 100]
    al_cleaned.stores = al_cleaned.stores.str.upper()
    al_cleaned['countries_fr'] = al_cleaned['countries_fr'].str.upper()

    # al_cleaned.sort_values(junk100g, ascending=False, inplace=True)

    return al_cleaned


def displayAnalysis(db_column, nom_fr):

    al_concernes = findInFood(db_column)

    # enlever le sucre pour ne considérer que les autres produits sucrés
    al_concernes_filtres = al_concernes[~al_concernes['categories_fr']
                                        .str
                                        .contains(nom_fr,
                                                  case=False,
                                                  na=False)]

    print("Première analyse: \n", al_concernes_filtres.describe(), "\n")

    print("Les 10 produits qui en contiennent le plus sont:\n",
          al_concernes_filtres.sort_values(db_column,
                                           ascending=False)
                              .head(10)['product_name'], "\n")

    # selectionner les aliments qui contiennent des quantité très importantes
    al_withSoMuch = al_concernes_filtres[al_concernes_filtres[db_column] >
                                         al_concernes_filtres[db_column]
                                         .mean(skipna=True)]

    print(al_withSoMuch.describe(), "\n")

    # pour voir quelles valeurs apparaissent le plus dans une series
    print("Les catégories de produits qui sont les plus représentées",
          "au sein des produits qui en contiennent plus que la moyenne sont:\n",
          al_withSoMuch['categories_fr'].value_counts(normalize=True).head(10),
          "\n")

    # realiser des groupby() sur les pays et les distributeurs ['store']
    print("Les pays dans lesquels ces produits sont les plus vendus sont :\n",
          al_withSoMuch.groupby('countries_fr')['product_name']
          .count()
          .sort_values(ascending=False)
          .head(10), "\n")

    # cut permet de séparer les données en divisant le range entre
    # le minimum et le maximum en parts égales

    # qcut permet de séparer les données en partitions égales de
    # On peut ensuite donner des noms aux partitions avec l'argument 'labels'

    # print(pd.qcut(al_sucres_exptSucre['sugars_100g'], 3,
    # labels=["good", "medium", "bad"]))
    print("Les magasins qui vendent le plus de ces produits sont :\n")
    plt.figure()
    plt.title(nom_fr)
    al_withSoMuch.groupby('stores')['product_name'].count().sort_values(ascending=False).head(10).plot.pie(figsize=(6, 6))

displayAnalysis('sugars_100g', 'sucre')
displayAnalysis('fat_100g', 'huile')
displayAnalysis('sodium_100g', 'sel')
