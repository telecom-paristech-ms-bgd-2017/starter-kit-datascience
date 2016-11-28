import pandas as pd
from os import path

PATH = path.dirname(path.abspath(__file__))
FILE = "/aliments.csv"

df_aliments = pd.read_csv(PATH + FILE, sep='\t')

labels = ['product_name', 'packaging', 'categories', 'brands', 'origins',
          'manufacturing_places']
features = ['sugars_100g', 'fat_100g', 'saturated-fat_100g',
            'sodium_100g', 'ingredients_from_palm_oil_n',
            'palmitic-acid_100g',
            'polyunsaturated-fat_100g',
            'monounsaturated-fat_100g',
            'ingredients_from_palm_oil_tags',
            'saturated-fat_100g']


def sugar(df):
    df = df.sort_values(['sugars_100g'], axis=0, ascending=False)
    print("### PRODUCT WITH SUGAR ###")
    print(df[['product_name', 'sugars_100g']][:5])
    print(df[['product_name', 'sugars_100g']].describe())


def sodium(df):
    df = df.sort_values(['sodium_100g'], axis=0, ascending=False)
    print('### PRODUCT WITH SODIUM ###')
    print(df[['product_name', 'packaging', 'sodium_100g']][:5])
    print(df[['product_name', 'packaging', 'sodium_100g']].describe())

print(df_aliments.columns[:20])
print(df_aliments.columns[20:40])
print(df_aliments.columns[40:60])
print(df_aliments.columns[60:80])
print(df_aliments.columns[80:100])

# sugar(df_aliments)
# sodium(df_aliments)

df_countries = df_aliments.groupby(["countries"])[
    ["sugars_100g"]].sum().sort_values(
        "countries", ascending=False)
print(df_countries)

"""df_countries = df_aliments.groupby(["countries"])[
    "countries"].count().sort_values(ascending=False)
print(df_countries)

df_packaging = df_aliments.groupby(["packaging"])[
    "packaging"].count().sort_values(ascending=False)

print(df_packaging[df_packaging > 5])
print(pd.cut(df_packaging, bins=25))

df_brands = df_aliments.groupby(["brands"])[
    "brands"].count().sort_values(ascending=False)
print(df_brands)

df_origins = df_aliments.groupby(["origins"])[
    "origins"].count().sort_values(ascending=False)
print(df_origins)

df_categories = df_aliments.groupby(["categories"])[
    "categories"].count().sort_values(ascending=False)
print(df_categories)

df_manufacturing_places = df_aliments.groupby(["manufacturing_places"])[
    "manufacturing_places"].count().sort_values(ascending=False)
print(df_manufacturing_places)"""
