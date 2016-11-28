import pandas as pd
import numpy as np
import re

#Importing the file
df = pd.read_csv('aliments.csv', delimiter="\t", error_bad_lines=False)

liste = df.columns.values.tolist()
x=[]
for s in liste :
    if "fat" in s :
        x.append(s)
    elif "sugar" in s :
        x.append(s)
    elif "ose" in s:
        x.append(s)

#Creating data_list
liste_bad =  ['code', 'product_name', 'generic_name', 'categories', 'packaging', 'origins',
              'manufacturing_places', 'purchase_places', 'brands',
              'stores', 'countries', 'ingredients_text', 'traces', 'main_category_fr'] + x

data = df[liste_bad]

#Regroupement par certaines catégories
data["metric"] = np.mean(data[x], axis = 0)
worst_aliments = data.sort_values(["metric"], ascending = False)

data['fat_100g'].value_counts()
fat_aliments = data['fat_100g'].value_counts() > 100
fat_aliments.value_counts()
dir = fat_aliments.sort_values(ascending = True).index
aliments = data[data['fat_100g'].isin(dir)]

grouped = data.groupby(['brands'])[liste_bad].mean()
classement = aliments[aliments['brands'] .isin(['Simply', 'Carrefour', 'Auchan'])]
classement.groupby(['brands','fat_100g'])['code'].count()
classement.groupby(['brands','fat_100g'])['code'].count()/classement.groupby('brands')['code'].count()
