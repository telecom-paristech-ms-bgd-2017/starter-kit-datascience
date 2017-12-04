from bs4 import BeautifulSoup
import requests
import numpy as np
import json
from pandas import DataFrame, Series
import googlemaps
# import multiprocessing from pool


#######################################################################################################################
# Part I - Scrapping on the url_wiki below to extract the biggest cities in France in terms of nb. of inhabitants     #
#######################################################################################################################
def extract_top_cities(nb_cities):
    url_wiki = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'
    response = requests.get(url_wiki)
    soup = BeautifulSoup(response.text, 'html.parser')
    top_cities_track = soup.select('#mw-content-text > table:nth-of-type(1) > tr')
    top_cities = []
    for i in (np.arange(nb_cities) + 1):
        top_cities.append(top_cities_track[i].select('td:nth-of-type(2)')[0].select('a')[0]['title'])
    return top_cities


def adapt_to_api_syntax(top_cities):
    res = top_cities[0]
    for city in top_cities[1:]:
        res += '|' + city
    return res


########################################################################################################################
# Part II - Use a Google Map's Distance Matrix API wrapper                                                             #
########################################################################################################################
# Wrapper -> https://github.com/googlemaps/google-maps-services-python
# i) Read from file the API_KEY
#with open('Google_API_Key', mode='r') as f:
#    api_key = f.read()

gmaps = googlemaps.Client(key='AIzaSyCHGkWQ86fKTvUNYvzuqGCzmSBUAW3BhpU')

villes = ['Paris','Lille','Marseille','Lyon','Strasbourg','Nantes','Nice','Bordeaux','Toulouse']

distances = gmaps.distance_matrix(villes, villes)['rows']
print(len(distances))
INDICATOR = 'duration'
TYPE_INDICATOR = 'value'

clean_distances = []
for row in distances:
  clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

print(len(clean_distances))
#clean_distances = map(lambda row: map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']) , distances)

df = DataFrame(clean_distances,index=villes,columns=villes)
print(df)
#df.to_csv(INDICATOR + '.csv')
