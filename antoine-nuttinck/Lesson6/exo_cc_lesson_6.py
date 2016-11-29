# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:37:01 2016

@author: Antoine
"""
import pandas as pd

alimentsDB_path = u'D:\Antoine\Documents\MS Big Data\Kit Big Data\/aliments.csv'

alimentsDB = pd.read_csv(alimentsDB_path,
                         delimiter='\t',
                         usecols=['code',
                                  'generic_name',
                                  'product_name',
                                  'sugars_100g',
                                  'categories_fr'])
# , 'fat_100g', 'saturated-fat_100g', 'silica_100g'])

alimentsDB.dropna(subset=['product_name', 'code'], inplace=True)
alimentsDB = alimentsDB.set_index('code')
alimentsDB.sort_values('sugars_100g', ascending=False, inplace=True)

# pour voir quelles valeurs apparaissent le plus dans une series
print(alimentsDB['categories_fr'].value_counts(normalize=True))

# enlever le sucre pour ne considérer que les autres produits sucrés
al_sucres_only = alimentsDB[alimentsDB['sugars_100g'] >
                            alimentsDB['sugars_100g'].mean(skipna=True)]  # numeric_only=True

# /!\ Certains aliments contiennent plus de 100g de sucre sur 100 --> cleaner
al_sucres_cleaned = al_sucres_only[al_sucres_only['sugars_100g'] < 100]

# enlever le sucre pour ne considérer que les autres produits sucrés
al_sucres_exptSucre = al_sucres_cleaned[al_sucres_cleaned['categories_fr']
                                        .str.contains('sucre', na=False)]

# realiser des groupby() sur les marques, les pays ou les distributeurs ['store']...

# qcut permet de séparer les données en partitions égales de 
# On peut ensuite donner des noms à ces partitions grâce à l'argument 'labels'

# cut permet de séparer les données en divisant le range entre le minimum et le maximum en parts égales

print(alimentsDB.describe())


aliments_gras = pd.read_csv(u'D:\Antoine\Documents\MS Big Data\Kit Big Data\/aliments.csv', 
                       delimiter='\t',
                       usecols=['generic_name', 'product_name', 'fat_100g', 'saturated-fat_100g'])

aliments_sales = pd.read_csv(u'D:\Antoine\Documents\MS Big Data\Kit Big Data\/aliments.csv', 
                       delimiter='\t',
                       usecols=['generic_name', 'product_name', 'sodium_100g'])
