import pandas as pd
import numpy as np

isclean = True




filename = "csv/R2015-1.csv"
fields = ["cpam", "pre_spe", "rem_mon", "dep_mon"]
datas = pd.DataFrame(columns=fields)



raw_datas = pd.read_csv(filename, delimiter=";")
datas = current_raw_datas[fields]
datas["rem_mon"] = current_datas["rem_mon"].str.replace(".", "")
datas["rem_mon"] = current_datas["rem_mon"].str.replace(",", ".")
datas["dep_mon"] = current_datas["dep_mon"].str.replace(".", "")
datas["dep_mon"] = current_datas["dep_mon"].str.replace(",", ".")
datas = current_datas.astype(float)


grouped_datas = datas.groupby(["cpam", "pre_spe"])["rem_mon", "dep_mon"].mean()
grouped_datas = grouped_datas.reset_index()
grouped_datas.to_csv("csv/clean_datas.csv")

clean= pd.read_csv("csv/clean_datas.csv", delimiter=",")
clean= clean_datas.set_index("Unnamed: 0")
clean"cpam"] = clean_datas["cpam"].astype(int)
clean["cpam"] = clean_datas["cpam"].astype(str).str[:-1].astype(np.int64)
clean= clean_datas.rename(columns={"cpam": "dep"})

rpps = pd.read_csv("csv/rpps_final.csv", delimiter=",")
rpps = rpps.groupby(["dep", "pre_spe"])["densite"].sum()
rpps = rpps.reset_index()

final = pd.merge(clean_datas, rpps, how="inner")
final["ratio"] = datas_final["dep_mon"] / datas_final["rem_mon"] * 100
final_sorted = datas_final.sort_values(["pre_spe", "ratio"], ascending=[True, True])

