import pandas as pd
import numpy as np

isclean = True

n_files = 12

#dico_regions = {

base_name = "csv/R2015-"
extension_name = ".csv"

fields = ["cpam", "pre_spe", "rem_mon", "dep_mon"]
datas = pd.DataFrame(columns=fields)

if isclean != True:
    for i in range(n_files):
        print(i + 1)
        filename = base_name + str(i + 1) + extension_name
        current_raw_datas = pd.read_csv(filename, delimiter=";")
        current_datas = current_raw_datas[fields]
        current_datas["rem_mon"] = current_datas["rem_mon"].str.replace(".", "")
        current_datas["rem_mon"] = current_datas["rem_mon"].str.replace(",", ".")
        current_datas["dep_mon"] = current_datas["dep_mon"].str.replace(".", "")
        current_datas["dep_mon"] = current_datas["dep_mon"].str.replace(",", ".")
        current_datas = current_datas.astype(float)
        datas = datas.append(current_datas, ignore_index=True)
    grouped_datas = datas.groupby(["cpam", "pre_spe"])["rem_mon", "dep_mon"].mean()
    grouped_datas = grouped_datas.reset_index()
    grouped_datas.to_csv("csv/clean_datas.csv")

clean_datas = pd.read_csv("csv/clean_datas.csv", delimiter=",")
clean_datas = clean_datas.set_index("Unnamed: 0")
clean_datas["cpam"] = clean_datas["cpam"].astype(int)
clean_datas["cpam"] = clean_datas["cpam"].astype(str).str[:-1].astype(np.int64)
clean_datas = clean_datas.rename(columns={"cpam": "dep"})

rpps = pd.read_csv("csv/rpps_final.csv", delimiter=",")
rpps = rpps.groupby(["dep", "pre_spe"])["densite"].sum()
rpps = rpps.reset_index()

datas_final = pd.merge(clean_datas, rpps, how="inner")
datas_final["ratio"] = datas_final["dep_mon"] / datas_final["rem_mon"] * 100
datas_final_sorted = datas_final.sort_values(["pre_spe", "ratio"], ascending=[True, True])


