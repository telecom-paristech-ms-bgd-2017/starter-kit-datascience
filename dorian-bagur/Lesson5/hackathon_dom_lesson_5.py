import pandas as pd
from os import path

PATH = path.dirname(path.abspath(__file__))
FILE_MEDECINS_REGIONS = "/Hackathon_data/effectifs_medecins_par_regions.csv"
FILE_MEDECINS_SPECIALITE = ("/Hackathon_data/"
                            "effectifs_medecins_par_specialite.csv")
FILE_POPULATION_2014 = "/Hackathon_data/nb_2014.csv"

# df_medecins_regions = pd.read_csv(PATH + FILE_MEDECINS_REGIONS)
df_medecins_specialite = pd.read_csv(PATH + FILE_MEDECINS_SPECIALITE, header=5,
                                     skiprows=2)
df_population = pd.read_csv(PATH + FILE_POPULATION_2014, header=0,
                            index_col=["dpt"])

print(df_population[:1])
print(df_medecins_specialite[:1])
