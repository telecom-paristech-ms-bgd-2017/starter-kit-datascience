import requests

import json

from bs4 import BeautifulSoup

import googlemaps

import pandas as pd

from multiprocessing import Pool



def getSoup(url):

request = requests.get(url)

result_soup = BeautifulSoup(request.text,'html.parser')

return result_soup



def getTable(soup):

table = soup.find(class_ = "wikitable sortable")

return table



def gettBody(table):

body = table.find("tbody")

return body



def getTr(body):

tr_list = body.find_all("tr")

return tr_list[1:32]



def getCityName(tr_list):

cities = []

for tr in tr_list:

cities.append(tr.find("td").text)

return cities



API_KEY = input("API Key : ")



# cities = getCityName(getTr(getTable(getSoup("https://en.wikipedia.org/wiki/List_of_the_75_largest_cities_in_France_(2012_census)"))))

cities = ['Paris','Marseille']

gmaps = googlemaps.Client(API_KEY)

distances = gmaps.distance_matrix(cities, cities)["rows"]



INDICATOR = 'distance'

TYPE_INDICATOR = 'value'

clean_distances = []

p = Pool(4)



for row in distances:

clean_distances.append(list(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements'])))



print(clean_distances)

df = pd.DataFrame(clean_distances, index = ['Paris','Marseille'], columns = ['Paris','Marseille'])

df.to_csv(INDICATOR.format('.csv'))


