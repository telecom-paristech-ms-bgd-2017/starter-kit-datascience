import pandas as pd
import re
import matplotlib.pyplot as plt

df = pd.read_csv("aliments.csv", sep='\t', header=0, dtype=str)

def plot(ingredient):

    sugar_df = df[['countries_fr', ingredient]].copy().dropna()
    
    sugar_df[ingredient] = sugar_df[ingredient].astype(float)
    
    sugar_df['countries_fr'] = sugar_df['countries_fr'].str.replace(
        "en:|fr:|es:|it:", "").str.lower()
    
    countries = set()
    for row in sugar_df['countries_fr'].str.split(','):
        for country in row:
            country = country.strip()
            if country:
                countries.add(country)
    
                
    replacements = {'emirato-arabes': 'émirats arabes unis',
                    'emiratos-arabes': 'émirats arabes unis',
                    'emirratos-arabes': 'émirats arabes unis',
                    'paris': 'france',
                    'polska': 'pologne',
                    'pozzallo-sicilia': 'italie',
                    'république de chine': 'république populaire de chine'}
    
    for r in replacements.keys():
       sugar_df['countries_fr'] = sugar_df['countries_fr'].map(
           lambda x: x.replace(r, replacements[r]))
       
    countries = set()
    for row in sugar_df['countries_fr'].str.split(','):
        for country in row:
            country = country.strip()
            if country:
                countries.add(country)
    
    countries = sorted(countries)
            
    sugar_dummies = pd.concat((sugar_df[[ingredient]], 
                               sugar_df['countries_fr'].str.get_dummies(
                                   sep=',')), axis=1)
    
    sugar_per_country = []
    
    for country in countries:
        sugar_per_country.append(pd.DataFrame.prod(
        sugar_dummies[[country, ingredient]], axis=1).sum(
            ) / sugar_dummies[country].sum())
    
    sugars = pd.DataFrame(
        sugar_per_country, index=countries, columns=[ingredient]).sort_values(
            by=ingredient, ascending=False)
    
    sugars.head().plot(kind='bar')
    plt.show()
    
plot('sugars_100g')
plot('fat_100g')
plot('sodium_100g')