#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pandas as pd
import numpy as np



path = "/Users/CharlotteEli/Documents/Cours/KitDataSciences/aliments.csv"

data = pd.read_csv(path,sep='\t')

print '############# SUGARS ###################'
data_sugar = data.sort_values("sugars_100g",ascending=False)
print data_sugar[['product_name','sugars_100g']].head()

print '############# ADDITIVES ###################'
data_additives_tags = data.sort_values("additives_tags",ascending=False)
print data_additives_tags[['product_name','additives_tags']].head()

print '############# PALM OIL ###################'
data_ingredients_from_palm_oil_n = data.sort_values("ingredients_from_palm_oil_n",ascending=False)
print data_ingredients_from_palm_oil_n[['product_name','ingredients_from_palm_oil_n']].head()
    
print '############# FAT ###################'
data_fat_100g= data[data["fat_100g"]<=100]
data_fat_100g= data_fat_100g.sort_values("fat_100g",ascending=False)
print data_fat_100g[['product_name','fat_100g']].head()

print '############# SODIUM ###################'
data_sodium_100g= data[data["sodium_100g"]<=100]
data_sodium_100g= data_sodium_100g.sort_values("sodium_100g",ascending=False)
print data_sodium_100g[['product_name','sodium_100g']].head()

print '############# SATURATED FAT ###################'
data_saturatedfat_100g= data[data["saturated-fat_100g"]<=100]
data_saturatedfat_100g= data_saturatedfat_100g.sort_values("saturated-fat_100g",ascending=False)
print data_saturatedfat_100g[['product_name','saturated-fat_100g']].head()

print '############# Omega 3 ###################'
data_omega3fat_100g= data[data["omega-3-fat_100g"]<=100]
data_omega3fat_100g= data_omega3fat_100g.sort_values("omega-3-fat_100g",ascending=False)
print data_omega3fat_100g[['product_name','omega-3-fat_100g']].head()




#healthy
#nutrition-score-fr_100g
#omega-3-fat_100g
#omega-9-fat_100g