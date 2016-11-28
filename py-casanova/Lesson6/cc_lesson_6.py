#! /usr/bin/python3.5
# -*- coding: utf8 -*-

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re

# FAT, SUGAR, SODIUM

aliments = pd.read_csv('aliments.csv', delimiter='\t')

for col in aliments.columns:
    print(col)

aliments['countries'].value_counts()
aliments['brands'].value_counts()

# Filtering out non significant brands with mask index
aliments_brand_significant = aliments['brands'].value_counts() > 10
brand_mask = aliments_brand_significant[aliments_brand_significant].index
aliments = aliments[aliments['brands'].isin(brand_mask)]

def top_n(column, n=5):
    return aliments.sort(column, ascending=False)[:n]

top_n('fat_100g')['product_name']

def rank(content, column):
	grouped = aliments.groupby(column)[
    	'fat_100g', 'sugars_100g', 'sodium_100g'].mean()
	return grouped[content].sort_values(ascending=False)

col_criteria = ['fat_100g', 'sugars_100g', 'sodium_100g']

for col in col_criteria:
	print(rank(col, 'main_category'))

for col in col_criteria:
	print(rank(col, 'brands'))

"""
fat = pd.pivot_table(aliments, values='fat_100g',
                     index='countries', aggfunc='mean')
"""

# OTHER EXAMPLES

aliments = pd.read_csv('aliments.csv', delimiter='\t')

aliments = aliments.set_index('product_name')
print(aliments.columns)

aliments['packaging'].value_counts()
aliments['packaging'].dropna()

# Removing items with non significant packaging category
aliments_with_packaging = aliments['packaging'].value_counts() > 30
aliments_with_packaging[aliments_with_packaging].index
aliments[aliments['packaging'].isin(
    aliments_with_packaging[aliments_with_packaging].index)]

#aliments['stores'].value_counts()
#aliments['nutrition_grade_fr'].value_counts()
aliments.groupby(['stores', 'nutrition_grade_fr'])

aliments[aliments['stores'].isin(['Biocoop', 'Simply'])]['code'].count()

# Quantiles
pd.qcut(aliments['sugars_100g'], 5)
aliments['cat_sugars'] = pd.qcut(aliments['sugars_100g'], 5, labels=[
                                 'a', 'b', 'c', 'd', 'e'])
aliments['cat_sugars'].value_counts()

#aliments = aliments.drop_duplicates('product_name')

# TRACES: building dummies

aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True)
aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True).to_csv('traces.csv')

aliments_with_traces = aliments.dropna(subset=['traces'])

traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
traces = set.union(*traces_iter)

dummies = DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns=traces)

for i, tr in enumerate(aliments_with_traces.traces):
     dummies.ix[i, tr.split(',')] = 1

dummies_nutrition = pd.get_dummies(aliments.dropna(subset=['nutrition_grade_fr'])['nutrition_grade_fr'])
