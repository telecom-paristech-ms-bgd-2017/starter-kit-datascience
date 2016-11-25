import pandas as pd
import numpy as np

fichier = '/home/nux/Documents/INFMDI721/Aliments/aliments.csv'
rawDF = pd.read_csv(fichier, sep='\t')

rawDF.head()

rawDF.columns[0:100]

sugarDF = rawDF[['countries_fr', 'sugars_100g']].dropna()
sugarDF = sugarDF[sugarDF['sugars_100g'] >= 0.]
sugarDF = sugarDF[sugarDF['sugars_100g'] <= 100.]
sugarDF = sugarDF[sugarDF['countries_fr'].str.contains('France')]
sugarDF.head(100)

sugarDF['cat_sugar'] = pd.cut(sugarDF['sugars_100g'], 10)
sugarDF.head()
sugarDF['cat_sugar'].value_counts()

sugarDF['cat_sugar'].value_counts()
sugarDF[sugarDF['cat_sugar'].str.endswith('10]')]
impact = 1 - float(len(sugarDF[sugarDF['cat_sugar'].str.endswith('10]')])) / len(sugarDF)
print 'The impact is of :', impact, '%'
