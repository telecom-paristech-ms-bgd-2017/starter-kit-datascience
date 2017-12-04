import pandas as pd
import numpy as np

df = pd.read_csv('aliments.csv', '\t', low_memory=False)

#On remplace les cases vides par des 0
df = df.fillna(0)

#On affiche toutes les colonnes pour repérer celles qui nous intéressent.
columns = list(df.columns.values)
print(columns)

# On cherche les aliments avec le taux de sucre le plus élevé
sugar = df.sort_values('sugars_100g',ascending=False)
print(sugar[['product_name','sugars_100g']].head(20))

# On cherche les aliments qui ont un taux de sodium < 100
sodium = df[df['sodium_100g'] <= 100]
sodium = sodium.sort_values('sodium_100g', ascending=False)
print(sodium[['product_name', 'sodium_100g']].head(20))

# On cherche les aliments avec un taux de graisse de moins de 100
fat = df[df['fat_100g'] <= 100]
fat = fat.sort_values('fat_100g', ascending=False)
print(fat[['product_name','fat_100g']].head(20))

# On cherche les aliments avec un taux de cholesterol de moins de 100%
cholesterol = df[df['cholesterol_100g'] <= 1]
cholesterol = cholesterol.sort_values('cholesterol_100g', ascending=False)
print(cholesterol[['product_name','cholesterol_100g']].head(20))


print()
print('##### Pays qui fabriquent les aliments les plus gras #####')
countries_fat = df[['countries', 'fat_100g']]
countries_fat = countries_fat[countries_fat['countries'] != 0]
print(countries_fat['countries'].value_counts().head())

print()
print('##### Pays qui fabriquent les aliments les plus sucrés #####')
countries_sugars = df[['countries', 'sugars_100g']]
countries_sugars = countries_sugars[countries_sugars['countries'] != 0]
print(countries_sugars['countries'].value_counts().head())


