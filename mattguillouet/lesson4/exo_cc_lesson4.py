import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import ipdb
import json
import re

# get most populated cities

urlWiki = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'

rCity = requests.get(urlWiki)

soupCity = BeautifulSoup(rCity.content, 'html.parser')

cities = soupCity.select('table > tr > td:nth-of-type(2)')

cities = cities[:10]

cities = [re.search('[\w ]+', c.text).group() for c in cities]


# get distance with google maps api

key = 'AIzaSyBTCCWLK9crDwyC7Jej6oUaOtTzyNrXDrM'
googleApiCall = 'https://maps.google.com/maps/api/geocode/json?address={0}+France&key={1}'

origins = 'origins=' + '|'.join([c.replace(' ', '+') + '+France' for c in cities])
destinations = 'destinations=' + '|'.join([c.replace(' ', '+') + 'France' for c in cities])
googleMatrixApiCall = 'https://maps.googleapis.com/maps/api/distancematrix/json?' + origins + '&' + destinations  + '&key={0}'


rApi2 = requests.get(googleMatrixApiCall.format(key))
jsonCities = json.loads(rApi2.text)
distanceMatrix = list(map(lambda x: list(map(lambda y: y['distance']['value'], x['elements'])), jsonCities['rows']))
timeMatrix = list(map(lambda x: list(map(lambda y: y['duration']['value'], x['elements'])), jsonCities['rows']))

cityDist = pd.DataFrame(distanceMatrix, columns=cities, index=cities)
cityDist.to_csv('villes_distance.csv')

cityTime = pd.DataFrame(timeMatrix, columns=cities, index=cities)
cityTime.to_csv('villes_time.csv')

city_dist

# cityInfo = list()
# for city in cities:
#     rApi = requests.get(googleApiCall.format(city, key))
#     jsonApi = json.loads(rApi.text)
#     res = jsonApi['results'][0]
#     cityInfo.append({'city': city, 'lat': res['geometry']['location']['lat'], 'long': res['geometry']['location']['lng']})


#cityData = pd.DataFrame(cityInfo)




