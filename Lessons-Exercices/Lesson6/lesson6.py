import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt
from numpy.random import randn
import statsmodels.api as sm

#aliments['packaging'].value_counts()
#aliments['brands'].value_counts()
#aliments['packaging'].dropna()
#aliments['packaging'].count()
#aliments['packaging'].value_counts()
#aliments['packaging'].value_counts() > 30
#aliments_with_packaging = aliments['packaging'].value_counts() > 30
#aliments_with_packaging.index
#aliments[aliments['packaging'].isin(aliments_with_packaging.index)]
#aliments['packaging'].count()
#aliments[aliments['packaging'].isin(aliments_with_packaging.index)]
#aliments_with_packaging
#aliments_with_packaging[aliments_with_packaging]
#packaging_to_keep = aliments_with_packaging[aliments_with_packaging].index
#aliments['packaging'].value_counts()
#packaging_to_keep = aliments_with_packaging[aliments_with_packaging].index
#packaging_to_keep
#len(packaging_to_kee)
#packaging_to_kee.shape
#packaging_to_keep.size
#aliments_with_packaging.size
#aliments['packaging'].value_counts()
#aliments[aliments['packaging'].isin(packaging_to_keep)]
#history
#aliments.columns
#aliments.columns[0:40]
#aliments['stores'].value_counts()
#aliments.columns[0:40]
#aliments['nutrition_grade_fr'].value_counts()
#battle.groupby(['stores','nutrition_grade_fr']).value_counts()
#battle.groupby(['stores','nutrition_grade_fr']).count()
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()
#battle = aliments[aliments['stores'].isin(['Biocoop','Simply'])]
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()
#aliments['stores'].value_counts()
#battle = aliments[aliments['stores'].isin(['Carrefour','Auchan','Leclerc'])]
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()
#battle.groupby(['stores'])['code'].sum()
#battle.groupby('stores')['code'].sum()
#battle.groupby('stores')['code'].count()
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()/battle.groupby('stores')['code'].count()
#battle.groupby(['stores','nutrition_grade_fr'])['code'].count()
#aliments.columns[50:70]
#aliments[u'glucose_100g']
#aliments[u'glucose_100g'].count()
#aliments[u'lactose_100g'].count()
#aliments[u'sugars_100g'].count()
#aliments[u'sugars_100g'].value_counts()
#pd.qcut(aliments[u'sugars_100g'],5)
#aliments['cat_sugars'] = pd.qcut(aliments[u'sugars_100g'],5)
#aliments['cat_sugars'] = pd.qcut(aliments[u'sugars_100g'],5,labels=['a','b','c','d','e'])
#aliments['cat_sugars']
#aliments['cat_sugars'].value_counts()
#aliments['cat_sugars'] = pd.cut(aliments[u'sugars_100g'],5,labels=['a','b','c','d','e'])
#aliments['cat_sugars'].value_counts()
