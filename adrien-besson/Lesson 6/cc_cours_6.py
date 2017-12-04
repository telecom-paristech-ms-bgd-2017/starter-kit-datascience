# coding: utf-8

import pandas as pd
import re

df = pd.read_csv("aliments.csv", delimiter='\t', low_memory=False)
df_select = df[['sugars_100g','fat_100g','product_name','generic_name','origins']]
df_select = df_select.fillna(0)
df_select['Gras_Sucre_100g'] = df_select['sugars_100g'] + df_select['fat_100g']
df_select = df_select[df_select['generic_name'] != 0]
df_select = df_select[df_select['Gras_Sucre_100g'] > 22.0]
df_select = df_select[df_select['Gras_Sucre_100g'] < 100.0]
df_select = df_select[df_select['origins'] != 0]

df_select[df_select['origins'] == "fabriqué en France"] = "France"
df_select[df_select['origins'] == "Fabriqué en France"] = "France"
df_select[df_select['origins'] == "france"] = "France"
df_select[df_select['origins'] == "Fabriqué en France"] = "France"
df_select[df_select['origins'] == "Agricultura UE,Agricultura no UE"] = "UE"
df_select[df_select['origins'] == "Union Européenne"] = "UE"
df_select[df_select['origins'] == "élaboré en France"] = "France"
df_select[df_select['origins'] == "España"] = "Espagne"

print(df_select['origins'].value_counts()[:10])