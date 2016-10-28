import pandas as pd
import re
import matplotlib.pyplot as plt

df = pd.read_csv("aliments.csv", sep='\t', header=0, dtype=str)

def plot(ingredient):

    sugar_df = df[['countries_fr', ingredient]].copy().dropna()    
    sugar_df[ingredient] = sugar_df[ingredient].astype(float)
    sugar_df = sugar_df[sugar_df[ingredient] > 0]
    sugar_df['countries_fr'] = sugar_df['countries_fr'].str.replace(
        "en:|fr:|es:|it:", "").str.lower()
    
    countries = set.union(*sugar_df.countries_fr.map(
        lambda x: set(x.split(','))).values)
    countries.remove('')
                    
    replacements = {'emirato-arabes': 'émirats arabes unis',
                    'emiratos-arabes': 'émirats arabes unis',
                    'emirratos-arabes': 'émirats arabes unis',
                    'paris': 'france',
                    'polska': 'pologne',
                    'pozzallo-sicilia': 'italie',
                    'république de chine': 'république populaire de chine',
                    'åland' : 'pays-bas'}
             
    for r in replacements.keys():
        if r in countries:
            countries.remove(r)
        sugar_df['countries_fr'] = sugar_df['countries_fr'].map(
            lambda x: x.replace(r, replacements[r]))       
    countries = sorted(countries)
    
    for country in countries:
        sugar_df[country] = sugar_df[ingredient][
            sugar_df['countries_fr'].str.contains(country)]
        if (sugar_df[country]!=0).sum() < 10:
            del(sugar_df[country])
            countries.remove(country)
    sugar_df = sugar_df.fillna(0)
    
    mean_sugars = pd.DataFrame(sorted([sugar_df[country].sum() / (
        sugar_df[country]!=0).sum() for country in countries], 
                reverse=True), index=countries, columns=[ingredient])
    
   
    mean_sugars.head().plot(kind='bar')
    plt.title('Average ingredient presence per country')
    plt.show()
    
plot('sugars_100g')