import requests
from bs4 import BeautifulSoup
import pandas as pd

# Récupérer la liste des villes les plus peuplées :
# http://www.insee.fr/fr/themes/tableau.asp?reg_id=0&ref_id=nattef01214

# Exemples :
# 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Paris&destinations=Lille&mode=bicycling&language=fr-FR&key=AIzaSyAzcmCrJq0jvquzkIMB7ur8DszJHyI1G3c'
# 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=AIzaSyAzcmCrJq0jvquzkIMB7ur8DszJHyI1G3c'


#       API GoogleMap


url_source_villes = 'http://www.insee.fr/fr/ffc/figure/NATTEF01214.xls'


def getMyToken():
    return open('/Users/Wes/CloudStation/big_data/MSBGD/6-INFMDI721-Kit_Big_data/token_google.txt', 'r').read()


def extractDistancevilles(ORIGINS, DESTINATIONS):
    API_KEY = getMyToken()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + str(ORIGINS) + '&destinations=' + str(
        DESTINATIONS) + '&mode=driving&language=fr-FR&key=' + str(API_KEY)
    result = requests.get(url).json()
    if result.get('rows')[0].get('elements')[0].get('status') == "OK":
        return result.get('rows')[0].get('elements')[0].get('distance').get('value')
    return 0


def extractVilles(source_ville):
    df_ville = pd.read_excel(source_ville, skiprows=2, index_col=0)
    df_ville = df_ville.dropna()
    return df_ville


def add_distance(df_ville):
    for el in df_ville.index:
        df_ville[el] = 0
        for sub_el in df_ville.index:
            df_ville[el].loc[df_ville[el].index == sub_el] = extractDistancevilles(el.replace(" ", "+"),
                                                                                   sub_el.replace(" ", "+"))
            print('[' + el + sub_el + '] : ' + extractDistancevilles(el, sub_el))



df_ville_pop = extractVilles(url_source_villes)
df_ville_pop = add_distance(df_ville_pop)
df_ville_pop.to_csv('distance_ville_population.csv')

print(df_ville_pop)



# Retrait des espaces avant et après la chaine de caractères :
# string.strip()
