# -*- coding: utf8 -*-
import pandas as pd


PATH = '/home/lorraine/ProjetDataSciences/starter-kit-datascience/lorraine-nyembi/Lesson6/'
FILE = 'aliments.csv'

df_aliments = pd.read_csv(PATH + FILE, sep='\t')

labels = ['product_name', 'packaging', 'categories', 'brands', 'origins',
          'manufacturing_places']
features = ['sugars_100g', 'fat_100g', 'saturated-fat_100g',
            'sodium_100g', 'ingredients_from_palm_oil_n',
            'palmitic-acid_100g',
            'polyunsaturated-fat_100g',
            'monounsaturated-fat_100g',
            'ingredients_from_palm_oil_tags',
            'saturated-fat_100g']

def fat(df):
    df = df.sort_values(['fat_100g'],ascending=False)
    print('****************PRODUITS GRAS****************')
    print(df[['product_name', 'packaging', 'fat_100g']].tail(5))
    print(df[['product_name', 'packaging', 'fat_100g']].describe())
    
def saturatefat(df):
    df = df.sort_values(['saturated-fat_100g'],ascending=False)
    print('****************PRODUITS GRAS SATURES****************')
    print(df[['product_name', 'packaging', 'saturated-fat_100g']].tail(5))
    print(df[['product_name', 'packaging', 'saturated-fat_100g']].describe())

def sugar(df):
    df = df.sort_values(['sugars_100g'], axis=0, ascending=False)
    print("**************PRODUITS AVEC DU SUCRE****************")
    print(df[['product_name', 'sugars_100g']].tail(5))
    print(df[['product_name', 'sugars_100g']].describe())


def sodium(df):
    df = df.sort_values(['sodium_100g'], axis=0, ascending=False)
    print('****************PRODUITS AVEC DU SODIUM****************')
    print(df[['product_name', 'packaging', 'sodium_100g']].tail(5))
    print(df[['product_name', 'packaging', 'sodium_100g']].describe())


print(df_aliments.columns[:20])
print(df_aliments.columns[20:40])
print(df_aliments.columns[40:60])
print(df_aliments.columns[60:80])
print(df_aliments.columns[80:100])

sugar(df_aliments)
sodium(df_aliments)
fat(df_aliments)
saturatefat(df_aliments)



