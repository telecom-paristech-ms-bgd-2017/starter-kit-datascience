#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:43:05 2016

@author: severine
"""


import pandas as pd


file = 'aliments.csv'

aliments = pd.read_csv(file, sep='\t')

labels = ['product_name', 'packaging', 'categories', 'brands', 'origins',
          'manufacturing_places']
features = ['sugars_100g', 'fat_100g', 'saturated-fat_100g',
            'sodium_100g', 'ingredients_from_palm_oil_n',
            'palmitic-acid_100g',
            'polyunsaturated-fat_100g',
            'monounsaturated-fat_100g',
            'ingredients_from_palm_oil_tags',
            'saturated-fat_100g']

def gras(data):
    data = data.sort_values(['fat_100g'],ascending=False)
    
    print (data[['product_name','fat_100g']].head())
    
    
def grassature(data2):
    data2 = data2.sort_values(['saturated-fat_100g'],ascending=False)
    print (data2[['product_name','saturated-fat_100g']].head())


def sucre(data3):
    data3 = data3.sort_values(['sugars_100g'], axis=0, ascending=False)
    print (data3[['product_name','sugars_100g']].head())

def sel(data4):
    data4 = data4.sort_values(['sodium_100g'], axis=0, ascending=False)
    print (data4[['product_name','sodium_100g']].head())
   
def ingredients_palm_oil (data5):
    data5= data5.sort_values("ingredients_from_palm_oil_n",ascending=False)
    print (data5[['product_name','ingredients_from_palm_oil_n']].head())    
    
    

sucre(aliments)
sel(aliments)
gras(aliments)
grassature(aliments)
ingredients_palm_oil(aliments)
