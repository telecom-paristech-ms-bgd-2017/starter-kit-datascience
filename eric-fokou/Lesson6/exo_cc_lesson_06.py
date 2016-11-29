
# coding: utf-8

# In[126]:

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


# In[127]:

aliments = pd.read_csv('aliments.csv', delimiter='\t')

#aliments['packaging'].value_counts()

#aliments['brands'].value_counts()
#aliments['packaging'].dropna()
aliments['packaging'].count()
aliments['packaging'].value_counts()
(aliments['packaging'].value_counts() > 30)[:5]


# In[128]:


aliments_with_packaging = aliments['packaging'].value_counts() > 30
print aliments_with_packaging.shape
aliments_with_packaging_limit = aliments_with_packaging[aliments_with_packaging]
print aliments_with_packaging_limit.shape


# ### Donc on conserve les aliments avec les emballages les plus utilisés

# In[129]:

print aliments['packaging'].shape
aliments = aliments[aliments['packaging'].isin(aliments_with_packaging_limit.index)]
print aliments['packaging'].shape


# In[130]:

aliments['stores'].value_counts()[:5]


# In[131]:

aliments['nutrition_grade_fr'].value_counts()


# In[132]:

battle = aliments[aliments['stores'].isin(['Carrefour','Auchan','Leclerc'])]
battle.iloc[:5]['stores']


# In[133]:

battle.groupby(['stores','nutrition_grade_fr'])['code'].count()


# In[134]:

battle.groupby('stores')['code'].count()


# In[135]:

battle.groupby(['stores','nutrition_grade_fr'])['code'].count()/battle.groupby('stores')['code'].count()


# In[137]:

aliments.columns[50:70]


# In[141]:

aliments[u'lactose_100g'].count()


# In[144]:

aliments[u'lactose_100g'].unique()


# In[145]:

aliments[u'sugars_100g'].count()


# In[147]:

aliments[u'sugars_100g'].value_counts()[:10]


# In[150]:

# Quantile-based discretization function
aliments['cat_sugars'] = pd.qcut(aliments[u'sugars_100g'],5)
aliments['cat_sugars'][:10]


# In[151]:

aliments['cat_sugars'] = pd.qcut(aliments[u'sugars_100g'],5,labels=['a','b','c','d','e'])
aliments['cat_sugars'][:10]


# In[152]:

aliments['cat_sugars'].value_counts()


# In[155]:

# The cut function can be useful for going from a continuous variable to a categorical variable. 
# For example, cut could convert ages to groups of age ranges
aliments['cat_sugars_cut'] = pd.cut(aliments[u'sugars_100g'],5,labels=['a','b','c','d','e'])
aliments['cat_sugars_cut'][:10]


# In[156]:

aliments['cat_sugars_cut'].value_counts()


# In[ ]:



