import pandas as pd
import re
import requests
from bs4 import BeautifulSoup


colToUse = ['cpam', 'region', 'dep_mon']
depensesAssuranceM = pd.read_csv("/users/arthurouaknine/Documents/KitDS/R2015/R201512.CSV",
                                 error_bad_lines=False, sep=';', encoding="ISO-8859-1",
                                 decimal=',', usecols=colToUse, nrows=1000000, dtype={'dep_mon': str})
# t = pd.Series(depensesAssuranceM.iloc[:,1].values.ravel()).unique()

densiteMedecins = pd.read_csv("/users/arthurouaknine/Documents/KitDS/rpps-medecins-tab7_30170492770795.csv", \
                              error_bad_lines=False, sep=';',
                              encoding="ISO-8859-1", header=3)

# On drop les NA et on supprime les données qui ne nous intéressent pas
densiteMedecins = densiteMedecins.dropna(axis=0)
densiteMedecins = densiteMedecins.iloc[22:, :]

# Cleaning des données pour qu'elles puissent matcher
densiteMedecins['SPECIALITE'] = densiteMedecins.iloc[:, 0].str.slice_replace(3) \
                                .str.strip().str.replace('A', '0').str \
                                .replace('B', '0').astype(int)
depensesAssuranceM['region'] = depensesAssuranceM.iloc[:, 1].astype(int)
depensesAssuranceM['dep_mon'] = depensesAssuranceM.iloc[:, 2].str \
                                .replace('.', '').str.replace(',', '.').astype(float)

# regCentime = re.compile('[0-9]{1,3},[0-9]{3}')

# On somme les dépassements d'honoraires
densiteMedecins = densiteMedecins.rename(columns={'SPECIALITE':'region'})
depensesParRegion = depensesAssuranceM.groupby(['region'])['dep_mon'].sum()

depensesParRegionClean = pd.DataFrame()
depensesParRegion = pd.DataFrame(depensesParRegion)
depensesParRegionClean['region'] = pd.DataFrame(depensesParRegion.index)
depensesParRegion.index = range(len(depensesParRegion))
depensesParRegionClean['dep_mon'] = depensesParRegion['dep_mon']

# Fusion des deux tables
# On a le montant des honoraires par region et les densités de médecins spé
depensesEtDensiteParRegion = pd.merge(depensesParRegionClean, densiteMedecins,\
                                        how='outer', on='region')

subData = depensesEtDensiteParRegion  # .iloc[:,1:]
subData = subData.dropna(axis=0)
# Premiere etude des correlation : depassement d'honoraires et spé
print(subData.corr()['dep_mon'])
# Corrélations positives + fortes : Rhumatologie, Cardiologie, Chirurgie faciliale
# Corrélations négatives + fortes : Oncologie, Médecine Interne, Médecine du travail


##### GET THE MIN MAX #####
#if subData['dep_mon'] == subData['dep_mon'].min():
 #   depassementMin = subData['dep_mon'].index

#print("La somme du dépassement d'honoraire la plus faible est : "\
 #       +str(subData['dep_mon'].min()))



# On remarque que le département 11 (Aude) est celui avec le plus de dépassements
# Le département 6 (Alpes-Maritimes) est celui où il y en a le moins
subData.iloc[4:6, :]
print()
# Pour presque toutes les spécialités, la densité est la plus faible pour
# le département faisant le moins de dépassement





# To crawl wiki https://www.mediawiki.org/wiki/API:Main_page
# plus simple ? http://www.geopopulation.com/france/departements/classement-departements-superficie/
path = "/users/arthurouaknine/Documents/KitDS/base-cc-evol-struct-pop-2013.csv"
populationFile = pd.read_csv(path,
                             error_bad_lines=False, sep=';', header=5,
                             encoding="ISO-8859-1")
populationData = populationFile[['DEP', 'P13_POP', 'P13_POP0014', 'P13_POP1529',
                                 'P13_POP3044', 'P13_POP4559', 'P13_POP6074',
                                 'P13_POP7589', 'P13_POP90P']]
populationData.columns = ['region', 'popTotale', 'pop_0_14', 'pop_15_29',
                          'pop_30_44', 'pop_45_59', 'pop_60_74',
                          'pop_75_89', 'pop_90']
populationData['region'] = populationData['region'].astype(str).str \
                            .replace('A', '0').str.replace('B', '0')
populationData = populationData.groupby(['region'])['region', 'popTotale',
                                                    'pop_0_14', 'pop_15_29',
                                                    'pop_30_44', 'pop_45_59',
                                                    'pop_60_74', 'pop_75_89',
                                                    'pop_90'].sum()
# Crawling de la surface des départements
url = 'http://www.geopopulation.com/france/departements/ \
        classement-departements-superficie/'
result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')

km2ParDep = []
for element in soup.find_all('tr'):
    oneLine = []
    if element != [] and len(element) != 0:
        if re.search(r'([0-9]{2,3}|2[A|B])', element.find_all(class_='column-4')[0].text) is not None:
            oneLine.append(re.search(r'([0-9]{2,3}|2[A|B])',element
                            .find_all(class_='column-4')[0].text).group(0))
            oneLine.append(element.find_all(class_='column-5')[0].text
                                        .replace('\xa0', '').replace(' ', ''))
        km2ParDep.append(oneLine)
print(km2ParDep)

#Pour éviter le crawling a chaque fois
# faire une fonction qui créé un fichier cache si il n'existe pas déjà

# Work in progress

# To Do
# Calculer la densité de population
# Relier avec les autres data
# boucler sur l'ensemble des fichiers
# Attention aux différentes variables temporaires
# Attention prendre en compte la part remboursée par la sécu (fichier R)
