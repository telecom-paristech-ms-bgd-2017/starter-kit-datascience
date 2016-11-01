# @ Author BENSEDDIK Mohammed

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
%matplotlib inline

df = pd.read_csv('/Users/Bense/Desktop/aliments.csv',
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
         ['sugars_100g'].value_counts(sort=True))
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
