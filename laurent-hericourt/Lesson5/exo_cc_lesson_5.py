import pandas as pd

aliments = pd.read_csv("aliments.csv", sep="\t", na_values=['NaN', 'nan'])
data_to_analyze = ['glucose_100g', 'sugars_100g']
aliments = aliments.dropna(subset=data_to_analyze, how='all')

headers = list(aliments.columns.values)
#'sugars_100g', 'sucrose_100g', 'glucose_100g'
#'fat_100g', 'saturated-fat_100

aggregation = {
    'sugars_100g': {
        'moyenne': 'mean',
    },
    'sucrose_100g': {
        'moyenne': 'mean',
    },
    'glucose_100g': {
        'moyenne': 'mean',
    },
    'fat_100g': {
        'moyenne': 'mean',
    }
}

df_groupby_aliments = aliments.groupby([aliments['categories']]).agg(aggregation)

print(aliments[aliments['sugars_100g'].isnull()])

