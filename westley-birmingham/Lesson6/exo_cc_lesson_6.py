import pandas as pd

path_aliments = 'aliments.csv'
path_traces = 'traces.csv'

aliments = pd.read_csv(path_aliments, delimiter='\t')
#aliments = aliments.dropna()
#aliments[['cities','countries','countries_fr','traces']]

#aliments[aliments['countries' == 'France']]['cities','countries','countries_fr','traces']

aliments_france = aliments[aliments['countries'] == 'France']
aliments_france_pepsi = aliments_france[aliments_france['product_name'] == 'Pepsi']
aliments_france = aliments[aliments['nutrition-score-fr_100g'] != 'NaN']

aliments_france_pepsi[aliments_france_pepsi['nutrition-score-fr_100g'] < 0.0]

traces = pd.read_csv(path_traces, delimiter='\t')
#traces = traces.dropna()


aliments['product_name'].value_counts()
aliments_count = aliments['product_name'].value_counts() > 10
aliments_count[aliments_count]
aliments_keep = aliments[aliments['product_name'].isin(aliments_count[aliments_count].index)]

aliments[aliments['product_name'].isin(aliments_count[aliments_count].index)].groupby('product_name')['nutrition-score-fr_100g'].count()

aliments[aliments['nutrition-score-fr_100g'] != 'NaN'].groupby(['countries', 'product_name']).mean()
aliments[aliments['nutrition-score-fr_100g'] != 'NaN'].groupby(['countries', 'product_name']).mean()
