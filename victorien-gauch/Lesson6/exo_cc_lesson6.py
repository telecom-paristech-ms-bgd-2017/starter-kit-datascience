import pandas as pd
import numpy as np

df = pd.read_csv('aliments.csv', '\t', low_memory=False)

#Affiche toutes les colonnes pour pouvoir repérer celles qui nous intéressent.
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
fat= df[df['fat_100g'] <= 100]
fat= fat.sort_values('fat_100g', ascending=False)
print(fat[['product_name','fat_100g']].head(20))

# On cherche les aliments un taux d'alcool supérieur à 40°
alcohol = df[df['alcohol_100g'] >= 40]
alcohol = alcohol.sort_values('alcohol_100g', ascending=False)
print(alcohol[['product_name','alcohol_100g']].head(20))

# On cherche les aliments avec un taux de graisse saturées de moins de 100
satured_fat = df[df['saturated-fat_100g'] <= 100]
satured_fat= satured_fat.sort_values('saturated-fat_100g', ascending=False)
print(satured_fat[['product_name','saturated-fat_100g']].head(20))

# On cherche les aliments avec un taux de taurine de moins de 0.5%
taurine = df[df['taurine_100g'] < 0.5]
taurine = taurine.sort_values('taurine_100g', ascending=False)
print(taurine[['product_name','taurine_100g']].head(20))

# On compte le nombre d'éléments qui ont un packaging et on les groupent par type de packaging
df_packaging = df['packaging'].value_counts()
print(df_packaging.head(20))


