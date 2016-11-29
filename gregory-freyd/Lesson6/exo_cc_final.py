import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


df = pd.read_csv("aliments.csv", sep='\t')
#df = df.set_index('')
#df = df.dropna()
#df['sodium_100g'].astype(float)
#aliments_with_sodium = df['sodium_100g'].value_counts()>30
#aliments_with_sodium = aliments_with_sodium[aliments_with_sodium].index
#print(aliments_with_sodium)
df2 = df[(df[u'sodium_100g']<1) & (df[u'sugars_100g']<20) & (df[u'fat_100g']<20)]
df2 = df2[[u'product_name', u'sodium_100g', u'sugars_100g', u'fat_100g', u'proteins_100g']]
#print(df.columns[60:80])
df2 = df2.dropna()

print("*****", df2.sort_values(u'proteins_100g', ascending=False))
#Pané savoyard façon tartiflette, des poudres (levures, poudre d'oeufs) barre protéinée, fromage allégé, gésiers de canards, jambon, poulet, lentilles

df2['proteins_grade'] = pd.qcut(df2[u'proteins_100g'], 5, labels=['E','D','C','B','A'])
print("-------", df2.sort_values(u'proteins_100g', ascending=False))

#saturated-fat_100g

#print("---", df.sort_values('sodium_100g', ascending=True)[['product_name', 'sodium_100g']])
#print(df['sodium_100g'].describe())
#print(df.columns)
#for column in df.columns:
#    print(column)
#print(df['sugars_100g'][30:40], df["countries"][30:40])



