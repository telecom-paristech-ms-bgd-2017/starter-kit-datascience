# -*- coding: utf-8 -*-

import pandas as pd

aliments_database = pd.read_csv("aliments.csv", sep='\t')

aliments_francais = aliments_database[
    aliments_database['countries'].isin(['France'])]

aliments_francais_with_oil_palm = aliments_francais[~aliments_francais["ingredients_from_palm_oil_n"].isnull()]

aliments_francais_with_oil_palm =  aliments_francais_with_oil_palm[aliments_francais_with_oil_palm["fat_100g"] > 0]
aliments_francais_with_oil_palm =  aliments_francais_with_oil_palm[~aliments_francais_with_oil_palm["fat_100g"].isnull()]

aliments_francais_with_oil_palm =  aliments_francais_with_oil_palm[aliments_francais_with_oil_palm["saturated-fat_100g"] >= 0]
aliments_francais_with_oil_palm =  aliments_francais_with_oil_palm[~aliments_francais_with_oil_palm["saturated-fat_100g"].isnull()]

aliments_francais_with_oil_palm["ratio_fat"] = aliments_francais_with_oil_palm[
    "saturated-fat_100g"] / aliments_francais_with_oil_palm["fat_100g"]

interdit_au_regime = aliments_francais_with_oil_palm.groupby(["brands_tags"])[
    ["sugars_100g", "fat_100g", "saturated-fat_100g", "ratio_fat"]].mean().sort_values(by="ratio_fat", ascending=True)

interdit_au_regime = regime[regime["ratio_fat"] > 0.25]

print(interdit_au_regime)