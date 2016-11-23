import pandas as pd
from os import path
import requests
from bs4 import BeautifulSoup
import time
import unicodedata
import glob

PATH = path.dirname(path.abspath(__file__))
FILE_MEDECINS = "/Hackathon_data/effectifs_medecins_regions_specialites.csv"
FILE_POPULATION = "/Hackathon_data/nb_2014.csv"
FILE_INSEE = "/Hackathon_data/region_dept.csv"
URL_POPULATION = ("https://raw.githubusercontent.com/SGMAP-AGD/DAMIR/master/" +
                  "fichiers_supplementaires/population%20prot%C3%A9g%C3%A9e/" +
                  "nb_2014.csv")
URL_INSEE = "http://www.insee.fr/fr/methodes/nomenclatures/cog/cog.asp"
PATH_R2014 = PATH + "/../Other/R2014/"
FILES_R2014 = glob.glob(PATH_R2014 + "*.CSV")
NB_FILES_R = 2


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return nfkd_form.encode('ASCII', 'ignore').decode('UTF-8')


def getRegionFromDepartment(dpt):
    payload = {"nivgeo": "dep", "codgeo": dpt}
    res = requests.get(URL_INSEE, params=payload)
    soup = BeautifulSoup(res.text, "html.parser")
    return {
        "dpt": dpt,
        "region": soup.find(class_="presentation").find("a")
        .text.split(" - ")[1]
        }

# Latin1 encoding for accents
df_medecins = pd.read_csv(PATH + FILE_MEDECINS, header=5, encoding="latin1",
                          index_col=["SPECIALITE"])
# Rename index
df_medecins.index.names = ["region"]
# First line is index header
df_medecins = df_medecins[1:]
# Remove accents from region names
df_medecins.index = df_medecins.index.map(remove_accents)

# Load data from csv or download it from the web
if not path.isfile(PATH + FILE_POPULATION):
    res = requests.get(URL_POPULATION)
    f = open(PATH + FILE_POPULATION, 'w')
    f.write(res.text)
    f.close()

df_population = pd.read_csv(PATH + FILE_POPULATION, header=0)
# Le département du Nord a un code erroné
df_population["dpt"] = df_population["dpt"].str.replace("5N", "59")

# Load data from csv or download it from the web
if path.isfile(PATH + FILE_INSEE):
    df_region = pd.read_csv(PATH + FILE_INSEE, header=0, index_col=0)
else:
    start_time = time.time()
    dept_region_dict = list(map(getRegionFromDepartment, df_population["dpt"]))
    df_region = pd.DataFrame.from_dict(dept_region_dict)
    df_region.to_csv(PATH + FILE_INSEE)
    print("execution time: %s seconds" % (time.time() - start_time))

# put region inside population dataframe
df_population = df_population.merge(df_region, on="dpt", how="left")
# departments are useless since we only consider regions
df_population = df_population.drop(["dpt", "l_dpt"], axis=1)
# les régions ne doivent pas comporter d'accents pour être normalisées au mieux
df_population["region"] = df_population["region"].apply(remove_accents)
# on somme la densité des catégories de population par région pour obtenir
# un dataframe avec un index qui sera la région
df_population = df_population.groupby("region").sum()

# Charger les données de tous les fichiers dans un seul dataframe
df_R = pd.DataFrame()
for k, file_R in enumerate(FILES_R2014):
    df = pd.read_csv(file_R, sep=";", header=0, encoding="latin1")
    df_R = pd.concat([df_R, df], axis=0)
    if k >= NB_FILES_R - 1:
        break

# set region properly
df_R = df_R.merge(df_region, on="dpt", how="left")
print(df_R.groupby("region_y")["dep_mon"].sum())
print(df_R.dtypes)
df_R["region"] = df_R["region_y"].apply(remove_accents)

# Peut-on établir un lien entre la densité de médecins par spécialité
# et par territoire et la pratique du dépassement d'honoraires ?


# Est-ce dans les territoires où la densité est la plus forte que les médecins
# pratiquent le moins les dépassement d'honoraires ?
df_population_all = df_population.sum(axis=1).sort_values(0, ascending=False)
print("Régions où la densité est la plus forte: ", df_population_all[:5])
df_dep_hon = df_R.groupby("region")["dep_mon"].sum().sort_values(
    "dep_mon", ascending=True)
print("Régions où le dépassement d'honoraires est plus faible: ",
      df_dep_hon[:5])


# Est ce que la densité de certains médecins / praticiens est corrélée
# à la densité de population pour certaines classes d'ages
# (bebe/pediatre, personnes agées / infirmiers etc...) ?
df_babies_pediatre = pd.concat([df_population["0 à 4 ans"],
                                df_medecins["Pédiatrie"]], axis=1)
correlation_babies_pediatre = df_babies_pediatre.corr(method='pearson',
                                                      min_periods=1)
print("Correlation between babies density and pédiatre =",
      correlation_babies_pediatre["0 à 4 ans"]["Pédiatrie"],
      "\nWe can conclude theres is not any correlation between it")

# on considère la densité de la population plus probablement active par région
df_active = df_population.ix[:, '20 à 24 ans':'60 à 64 ans'].sum(axis=1)
df_active_work = pd.concat([df_active,
                            df_medecins["Médecine du travail"]], axis=1)
correlation_active_work = df_active_work.corr(method='pearson', min_periods=1)
print("Correlation between active density and 'médecine du travail' =",
      correlation_active_work[0]["Médecine du travail"],
      "\nWe can conclude theres is not any correlation between it")


# librairie pyplot
# graphes de distribution
# scatter matrix: distribution relative par rapport à chacune des variables
# corrélations
