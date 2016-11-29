import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
# Exercice aliments

# Un sportif souhaite augmenter la part de protéines dans son alimentation
# Sur la base des aliments disponibles dans le fichier, nous allons l'aider
# à sélectionner les aliments qui apportent des protéines avec une qualité
# nutritionnelle correcte en se basant sur des compositions nutritionnelles
# classiques (sucres, lipides, sel).
# Ainsi il sera retenu les aliments présentant moins de 10% de sucres, moins
# de 1% de sel et moins de 20% de lipides.

df = pd.read_csv("aliments.csv", sep='\t')

# Sélection des aliments répondant aux critères énoncés
df2 = df[(df[u'sodium_100g']<1) & (df[u'sugars_100g']<10) & (df[u'fat_100g']<20)]
df2 = df2[[u'product_name', u'sodium_100g', u'sugars_100g', u'fat_100g', u'proteins_100g']]
# Suppression des aliments dont une des valeurs est manquante ne permmettant pas
# de faire un choix éclairé
df2 = df2.dropna()

# Classement des résultats par ordre de pourcentage de protéine décroissant
print("Liste des aliments classés par meilleur taux de protéines, ayant un taux de sodium, "
      "sucres, lipides inférieurs respectivement à 1%, 10%, 20% :"
      "", df2.sort_values(u'proteins_100g', ascending=False))

# Les aliments arrivant en tête de cette liste sont :
# Pané savoyard façon tartiflette, des poudres (levures, poudre d'oeufs) barre hyperprotéinée,
# fromage allégé, gésiers de canards, jambon, poulet, lentilles

# Pour l'aider dans son choix futur nous lui fournissons la liste complète en
# répartissant équitablement les aliments sous 5 catégories, les plus intéressants
# en terme de taux de protéines se voyant attribuer la note 'A'
df2['proteins_grade'] = pd.qcut(df2[u'proteins_100g'], 5, labels=['E','D','C','B','A'])
print("Liste des aliments sélctionnés notés selon leur taux de protéine ('A' étant le plus fort taux) :",
      df2.sort_values(u'proteins_100g', ascending=False))
