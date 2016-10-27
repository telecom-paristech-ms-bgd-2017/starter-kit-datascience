import requests
from bs4 import BeautifulSoup
import json


# Récupérer la liste des villes les plus peuplées :
# http://www.insee.fr/fr/themes/tableau.asp?reg_id=0&ref_id=nattef01214

# Exemples :
# 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Paris&destinations=Lille&mode=bicycling&language=fr-FR&key=AIzaSyAzcmCrJq0jvquzkIMB7ur8DszJHyI1G3c'
# 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=AIzaSyAzcmCrJq0jvquzkIMB7ur8DszJHyI1G3c'


# def extractVilles():
#     return 0


def extractDistancevilles(ORIGINS, DESTINATIONS):
    API_KEY = getMyToken()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + str(ORIGINS) + '&destinations=' + str(DESTINATIONS) + '&mode=bicycling&language=fr-FR&key=' +str(API_KEY)
    result = requests.get(url)
    #res = json.loads(result.json()['rows'][0]['distance']['value'])
    ress = json.load(result.json()['rows'][0]['elements']['distance'])
    # map(lambda x: x[], res)
    print(ress)

def getMyToken():
    return open('/Users/Wes/CloudStation/Big Data/Master Spe BGD/6 - INFMDI 721 - Kit Big data/token_google.txt', 'r').read()


extractDistancevilles('Paris', 'Lille')


#json.load(resul.json())

# Retrait des espaces avant et après la chaine de caractères :
# string.strip()