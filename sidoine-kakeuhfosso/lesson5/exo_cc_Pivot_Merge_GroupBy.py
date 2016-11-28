# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb

#MERGE
insee1 = pd.read_csv('base-cc-evol-struct-pop-2011.csv')
insee2 = pd.read_csv('base-cc-rev-fisc-loc-menage-10.csv')

def strip_corse(val):
    if type(val) == int:
        return val
    if val == 'nan':
        return -1
    return int(re.sub('(A|B)', '0',val))

insee1['code insee'] = insee1['code insee'].apply(strip_corse)
insee2['CODGEO'] = insee2['CODGEO'].apply(strip_corse)


#PIVOT
releves = [
         ['lundi','temperature',28]
         ,['lundi','ensoleillement',4]
         ,['lundi','pollution',5]
         ,['lundi','pluie',100]
         ,['mardi','temperature',28]
         ,['mardi','ensoleillement',4]
         ,['mardi','pollution',5]
         ,['mardi','pluie',100]
         ,['mercredi','temperature',28]
         ,['mercredi','ensoleillement',4]
         ,['mercredi','pollution',5]
         ,['mercredi','pluie',100]
         ,['jeudi','temperature',28]
         ,['jeudi','ensoleillement',4]
         ,['jeudi','pollution',5]
         ,['jeudi','pluie',100]
         ,['vendredi','temperature',28]
         ,['vendredi','ensoleillement',4]
         ,['vendredi','pollution',5]
         ,['vendredi','pluie',100]
         ]

cities_data  = DataFrame(releves, columns=['day','observation','value'])
cities_data_wide = cities_data.pivot('day','observation','value')
cities_data_wide = cities_data.pivot('day','observation','value').reset_index()
observations =[ u'ensoleillement', u'pluie', u'pollution', u'temperature']
pd.melt(cities_data_wide, id_vars=['day'], value_vars=observations)


#GROUP BY


cameras = pd.read_csv('Camera.csv', sep=';')
cameras = cameras.ix[1:]
cameras_clean = cameras.set_index('Model').astype(float)
cameras_clean = cameras_clean.rename(columns={u'Weight (inc. batteries)':'weight'})


brand = cameras['Model'].apply(lambda x: x.split(' ')[0])
cameras_clean['brand'] = brand
cameras_clean.groupby('brand')['weight'].mean()
cameras_clean.groupby('brand')[u'Max resolution', u'Low resolution', u'Effective pixels'].sum()
cameras_clean.groupby('brand').agg({'weight': np.mean, 'Max resolution':np.sum})
cameras_clean.groupby(lambda x: x.split(' ')[0]).agg({'weight': np.mean, 'Max resolution':np.sum})

def top_n(df, n=5, column="Max resolution"):
    return df.sort(column,ascending=False)[:n]

cameras_clean.groupby(lambda x: x.split(' ')[0]).apply(top_n)