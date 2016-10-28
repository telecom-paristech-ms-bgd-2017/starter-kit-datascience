import pandas as pd
import numpy as np

raw_datas = pd.read_csv("aliments.csv", delimiter="\t")
raw_datas = raw_datas.set_index("product_name")

#sugar_100g fat_100g saturated-fat_100g sodium_100g
fields = ["sugars_100g", "fat_100g", "sodium_100g"]

datas = raw_datas[["brands", "sugars_100g", "fat_100g", "saturated-fat_100g", "sodium_100g"]]
clean_datas = datas.dropna()

grouped_datas = clean_datas.groupby(["brands"])[fields].mean()
top_sugars = grouped_datas.sort_values(["sugars_100g"], ascending=False)
top_fat = grouped_datas.sort_values(["fat_100g"], ascending=False)
top_sodium = grouped_datas.sort_values(["sodium_100g"], ascending=False)


clean_datas_agg = grouped_datas
clean_datas_agg["global_avg"] = ( grouped_datas["sugars_100g"] + grouped_datas["fat_100g"]
                                 + grouped_datas["sodium_100g"] ) / 3.0

top = clean_datas_agg.sort_values(["global_avg"], ascending=False)
