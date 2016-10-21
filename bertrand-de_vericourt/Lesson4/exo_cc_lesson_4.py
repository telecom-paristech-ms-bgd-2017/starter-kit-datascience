############################ SCRAP French cities ##############################

# API Google Distance >> https://developers.google.com/maps/documentation/distance-matrix/get-api-key?hl=fr

# usage possible de la lib JSON (pas utilisé ici)
import json
#json.dumps(UnArray)
# =====> me transforme l'array au format JSON.

# Pour teter les REGEX:
# aller sur regex101.com (teste les regex)   ou  emailregex.com  => récupérer un cheat sheet
#  importer la library  re
# Utile: on peut faire les trim(), les split() etc vectoriellement (pour tous les éléments)
# très UTILE: utiliser une REGEX dans un SERIE, on pourra utiliser la méthode .extract() afin de tout ordonner très rapidement.

# transformer en String se dit "caster en String"

# AMELIORATION pour chaîne de caractères avec paramètres:
# utiliser >>>> 'maString1{}maString2'.format(LeParamètre)  >>> plutôt que 'maString1' + LeParamètre + 'maString2'

# Pour ne pas avoir à réécrire les underscores par exemple: utiliser les KAMEL CASE

# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# get 30 French biggest cities names
cities_list = []
url = 'http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/'
page_cities = requests.get(url)
soup = BeautifulSoup(page_cities.text, 'html.parser')
#soup.prettify()
cities = soup.select('tbody tr')

for city in cities[1:31]:
	cities_list.append(city.select('td:nth-of-type(2)')[0].text.replace(" ", "").replace('\n', ''))
	
# get distances (on utilise des dataframes, ils sont plus manipulables que les matrices)

dfAllCities = pd.DataFrame(0, cities_list, cities_list)
f = open('maCleGG.txt', 'r')

for idx, city1 in enumerate(cities_list):

	for city2 in cities_list[idx+1:]:

		try:

			StartFrom = city1 + '+France'
			GoTo = city2 + '+France'

			YOUR_API_KEY = f.readline()
			urlDistance = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + \
				StartFrom + '&destinations=' + GoTo + '&key=' + YOUR_API_KEY

			response = requests.get(urlDistance)
			me_json = response.json()

			# in meters
			print('from ' + city1 + ' to ' + city2)
			distanceTemp = me_json['rows'][0]['elements'][0]['distance']['text']
			dfAllCities[city1][city2] = distanceTemp
			# in seconds
			TimeTemp = me_json['rows'][0]['elements'][0]['duration']['text']
			dfAllCities[city2][city1] = TimeTemp

		except ValueError as e:

			print('error ' + e)

#print(dfAllCities)

# Insert into a CSV

fileName = 'Distances_villes'
dfAllCities.to_csv(fileName)
