from pprint import pprint
import pandas as pd
import numpy as np

product_to_ban = 'sodium'

df = pd.read_csv('aliments.csv', sep='\t')

# impacted_cols = [col for col in df.columns if product_to_ban in col]


# r = range(df.shape[0])
# impacted_brands = [df['brands'][i] for c in impacted_cols for i in r if not(np.isnan(df[c][i]))]
# pprint(set([str(b).lower() for b in impacted_brands if b]))

sodium = 'sodium_100g'
df_sod = df[df[sodium].isin([100, 9999])][[sodium, 'brands']]
df_sod_10 = df_sod.sort([sodium], ascending=True)
