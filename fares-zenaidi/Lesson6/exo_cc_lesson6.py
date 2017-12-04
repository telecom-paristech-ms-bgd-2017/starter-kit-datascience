import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re

# Loading of the aliments of the csv file
aliments = pd.read_csv('aliments.csv', delimiter='\t', low_memory=False)

# Solution 1 - Metric used: aliments with a bad nutrition grade
alimentsNutGrade = aliments.dropna(subset=['product_name', 'nutrition_grade_fr'])
alimentsNutGrade = aliments.set_index('product_name')
print("Total number of aliments: {} \n".format(aliments.shape[0]))
bad = alimentsNutGrade['nutrition_grade_fr'].isin(['c', 'd', 'e'])
# Selection of the aliments wich have a bad nutrition grade
badAliments = alimentsNutGrade[bad]
print("Number of aliments with a bad nutrition grade: {} \n".format(badAliments.shape[0]))
# Stores where a lot of bad aliments can be bought
badStores = (badAliments.groupby('stores').count())['code'].sort_values(ascending=False)
print("The top 10 stores that sell a lot of bad nutrition are: {} \n".format(badStores.ix[:10]))


# Solution 2 - Other metric (based on the composition of the aliments)
alimentsComposition = aliments.set_index('product_name')
columnsList = aliments.columns.values.tolist()
columnsOfInterest = []
for col in columnsList:
    if "ose" in col:
        columnsOfInterest.append(col)
    elif "fat" in col:
        columnsOfInterest.append(col)
    elif "sugar" in col:
        columnsOfInterest.append(col)

print("Columns of interests : {} \n".format(columnsOfInterest))

for col in columnsOfInterest[:]:
    print("Top 10 Bad aliments for {}".format(col.split("_")[0]))
    print(alimentsComposition[col].sort_values(ascending=False)[:10])
    print("")
