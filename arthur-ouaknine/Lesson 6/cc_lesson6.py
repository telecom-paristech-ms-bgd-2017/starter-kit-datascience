# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:43:57 2016

@author: arthurouaknine
"""
import pandas as pd
path = '/users/arthurouaknine/Documents/starter-kit-datascience/Lessons-Exercices/Lesson4/aliments.csv'

data = pd.read_csv(path, error_bad_lines=False, sep='\t', header=0, encoding="utf-8")

# dataClean = data.dropna(axis=0)

subData = data[['product_name','categories','categories_tags','categories_fr',
                'ingredients_from_palm_oil_n','ingredients_from_palm_oil',
                'ingredients_from_palm_oil_tags','ingredients_that_may_be_from_palm_oil_n',
                'ingredients_that_may_be_from_palm_oil','sugars_100g',
                'glucose_100g', 'fat_100g', 'saturated-fat_100g', 'countries_fr']]

resumeQuant = subData[['product_name','sugars_100g','glucose_100g','fat_100g',
                       'saturated-fat_100g']] #.fillna(0)
sucreMean = resumeQuant['sugars_100g'].std()
test = resumeQuant.groupby(['product_name'])['sugars_100g'].count()

sucreAnalysis = subData[['countries_fr', 'sugars_100g']].dropna()
sucreAnalysis = sucreAnalysis[sucreAnalysis['sugars_100g'] >= 0.]
sucreAnalysis = sucreAnalysis[sucreAnalysis['sugars_100g'] <= 100.]
sucreAnalysis = sucreAnalysis[sucreAnalysis['countries_fr'].str.contains('France')]


sucreAnalysis['cat_sugar'] = pd.cut(sucreAnalysis['sugars_100g'], 5)
sucreAnalysis.head()
sucreAnalysis['cat_sugar'].value_counts()

sucreAnalysis['cat_sugar'].value_counts()
sucreAnalysis[sucreAnalysis['cat_sugar'].str.endswith('10]')]
impact = 1 - float(len(sucreAnalysis[sucreAnalysis['cat_sugar'].str.endswith('10]')])) / len(sucreAnalysis)
print('Impact calculé :', impact, '%')


# Pour les champs qualitatif, parfois peu d'occurence
# Necessite une analyse plus approfondie (split par ,)
# Utilisation de clé trace (voir cours précédent)

# Astuce : possibiité de faire un calcul entre deux dataframe qui ne sont
# pas de même taille mais qui sont indexés de la meme façon
