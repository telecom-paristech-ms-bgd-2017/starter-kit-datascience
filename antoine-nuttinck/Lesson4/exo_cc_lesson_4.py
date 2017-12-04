# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:02:38 2016

@author: Antoine
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

url_cities = "http://lespoir.jimdo.com/2015/03/05/" +  \
            "classement-des-plus-grandes-villes-de-france-source-insee"

result = requests.get(url_cities)
soup = BeautifulSoup(result.content, 'html.parser')
a = soup.find_all(class_='xl65')

cities_list = []
for i in range(1, 30, 3):
    cities_list.append(str(a[i].text.split(' ')[12]).replace('u\'', '')
                                                    .replace('\n', ''))

# Alternative : wrapper Google maps: import googlemaps

with open('API_GoogleMap.txt', 'r') as APIfile:
    API_KEY = APIfile.read().replace('\n', '')

api_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

sep = '|'
cities_str = sep.join(cities_list)
orig = '&origins=' + cities_str.replace(' ', '+')
dest = '&destinations=' + cities_str.replace(' ', '+')
endurl = '&mode=driving&language=fr-FR'
my_key = '&key=' + API_KEY
complete_url = api_url + orig + dest + endurl + my_key

r = requests.get(complete_url)

if(r.ok):
    for mesure in ['distance', 'duration']:
        matDist = json.loads(r.text or r.content)
        if(matDist['status'] == "OK"):
            cleanDistance = list(map(lambda row: map(
                                    lambda x: x[mesure]['value'],
                                    row['elements']), matDist['rows']))
            matrixDistance = pd.DataFrame(cleanDistance,
                                          index=cities_list,
                                          columns=cities_list)
            print("Matrix of " + mesure + " between cities in France :\n",
                  matrixDistance)
            matrixDistance.to_csv(mesure + "_matrix_french_cities.csv")
        else:
            print(matDist['status'])

else:
    print('Connexion to Google Map API failed.')
