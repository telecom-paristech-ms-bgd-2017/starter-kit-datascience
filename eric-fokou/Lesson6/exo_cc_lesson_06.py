# -*- coding: utf-8 -*-
import requests
import ijson
import json
import csv
import oauth2 as oauth
import time
from urllib2 import urlopen, Request
import operator
import pandas as pd
from collections import OrderedDict
from datetime import date
import urllib2
from bs4 import BeautifulSoup
import numpy as np
import re
from pandas import Series, DataFrame
import scipy
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from multiprocessing import Pool
import sklearn
from sklearn import preprocessing




aliments = pd.read_csv('aliments.csv', delimiter='\t')
aliments = aliments.set_index('product_name')



#corrigé --> column 0-40
#---> dropna
#--->value_counts() ----> cleaner la donnée
#.index
#.isin( biduele.index)
#panda percent by group
#pd.qcut(df,number_of_cuts)
#read csv
#lire la doc de pandas


#Note

#If you have a Series where lots of elements are repeated (i.e. the number of unique elements in the Series is a lot smaller than the length of the Series), it can be faster to convert the original Series to one of type category and then use .str.<method> or .dt.<property> on that. The performance difference comes from the fact that, for Series of type category, the string operations are done on the .categories and not on each element of the Series.

########################################################################
print aliments["sugars_100g"].value_counts()>2
print type(aliments)
plot_sugars=0
if plot_sugars:
     fig = plt.figure(figsize=(8, 6))
     
     aliments["sugars_100g"].plot(kind='hist')
     plt.show()
#print aliments.pivot()#.stack().value_counts()
#print aliments["sugars_100g"]>100
print aliments[aliments["sugars_100g"]>100]["sugars_100g"]

#150g d'eau <-> 15 cl
#
#33cl de coca <-> 35 g de sucre
#330g de coca <-> 35 g de sucre
#100g de coca <->100*35/330 g de sucre ?


result = aliments.sort(['sugars_100g'], ascending=[ 0])
print result['sugars_100g'][0:1000]
#le coca c'est
print 100*35/330
raw_input()

#print aliments.value_counts()
#print "aliments.value_counts()"
#raw_input()
print scipy.array(list(aliments.columns.values))
print "columns"
raw_input()


#le but est de trouver les aliments les plus gras, les plus sucré, les plus salé
#évidemment il faut calculer l'écart type et le sigma

aliments_with=aliments['packaging'].value_counts()>30
pack_to_keep=aliments_with[aliments_with].index

#calculer le nombre de valeurs differentes dans différentes

print aliments
print "vendrediii2"
#trier par  sugars_100g' 'sucrose_100g'
# 'glucose_100g'


#trier par 'fat_100g'
# 'saturated-fat_100g'

# print aliments['sugars_100g'].value_count()
# raw_input()

print "\n &&&&&&&&&  aliments('sugars_100g')"
#result = df.sort(['A', 'B'], ascending=[1, 0])
result = aliments.sort(['sugars_100g'], ascending=[ 0])
print result[['sugars_100g']]
#print result[['product_name','sugars_100g']]
print "\n &&&&&&&&& ````````````````````````"

print result[['countries']]

df=result.groupby(['countries'])['sugars_100g'].mean()

#print df
result['mean_sugars_per_country'] = df #Series(np.random.randn(sLength), index=df1.index)
result3 = result.sort(['mean_sugars_per_country'], ascending=[ 0]).groupby(['countries'])
result4 = result.groupby(['countries'])
#.sort(['mean_sugars_per_country'], ascending=[ 0])
#result4 = result.groupby(['countries']).sort(['mean_sugars_per_country'], ascending=[ 0])
print result3
#print result4
#df=result.groupby(['countries'])['sugars_100g'].mean()
# country * 


#print result
#raw_input()


#print scipy.array(list(aliments.columns.values))
raw_input()


df = pd.read_csv('aliments.csv',
                 delimiter="\t", error_bad_lines=False)

df.shape

df.columns

my_columns = ['code', 'product_name', 'generic_name',
              'categories', 'origins', 'manufacturing_places', 'purchase_places', 'brands',
              'stores', 'countries', 'ingredients_text', 'traces', 'main_category_fr',
              'sugars_100g', 'sucrose_100g', 'glucose_100g', 'fructose_100g', 'fat_100g']
aliments_df = df[my_columns]

aliments_df = aliments_df.dropna(subset=['sugars_100g'])

aliments_df['sugars_100g'].value_counts(sort=True)

a = aliments_df[aliments_df['sugars_100g'] < 400]
plt.plot(aliments_df[aliments_df['sugars_100g'] < 400]
         ['sugars_100g'].value_counts(sort=True),marker='*',linestyle='None')
plt.show()


pd.qcut(aliments_df['sugars_100g'], 5).value_counts()

aliments_df.groupby('brands')[['code', 'product_name', 'sugars_100g']].count(
).sort('sugars_100g', ascending=False)

aliments_df.groupby('categories')[['code', 'product_name', 'sugars_100g']].count(
).sort('sugars_100g', ascending=False)

aliments_df.set_index('product_name')

for col in my_columns:
    print()
    print(aliments_df[col].describe())

aliments_df.head(100)

aliments_df.columns = map(str.lower, aliments_df)
aliments_df.head(100)

products_salty = aliments_df[
'ingredients_text'].str.contains('SEL', regex=True)