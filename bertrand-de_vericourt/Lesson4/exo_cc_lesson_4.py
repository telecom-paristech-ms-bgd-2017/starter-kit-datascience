############################ SCRAP French cities ##############################

# API Google Distance >> https://developers.google.com/maps/documentation/distance-matrix/get-api-key?hl=fr

# usage possible de la lib JSON (pas utilisé ici)
import json
#json.dumps(UnArray)
# =====> me transforme l'array au format JSON.

# AMELIORATION pour chaîne de caractères avec paramètres:
# utiliser >>>> 'maString1{}maString2'.format(LeParamètre)  >>> plutôt que 'maString1' + LeParamètre + 'maString2'

# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

allCities = pd.DataFrame(0, cities_list, cities_list)

for idx, city1 in enumerate(cities_list):

	for city2 in cities_list[idx+1:]:

		try:

			if city1 == 'LeMans': city1 = 'Le Mans'
			if city2 == 'LeMans': city2 = 'Le Mans'
			StartFrom = city1
			GoTo = city2

			YOUR_API_KEY = 'AIzaSyCy_-e9MGpAfoFboppXEXXul1zNFQ7puqw'
			urlDistance = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + StartFrom + '&destinations=' + GoTo + '&key=' + YOUR_API_KEY

			response = requests.get(urlDistance)
			me_json = response.json()
			# in meters
			print('from ' + city1 + ' to ' + city2)
			distanceTemp = me_json['rows'][0]['elements'][0]['distance']['value']
			allCities[city1][city2] = distanceTemp
			# in seconds
			TimeTemp = me_json['rows'][0]['elements'][0]['duration']['value']
			allCities[city2][city1] = TimeTemp

		except ValueError as e:

			print('error ' + e)

print(allCities)