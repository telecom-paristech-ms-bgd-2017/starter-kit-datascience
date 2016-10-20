#! /usr/bin/python3.5

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from os import getenv
import os.path as osp

# Distance ville à ville sur les n plus grandes villes de France

# List n villes


def get_cities(nb_cities):
    url_wiki = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'
    results = requests.get(url_wiki)
    soup = BeautifulSoup(results.text, 'html.parser')

    origin = []
    for i, city in enumerate(soup.table.find_all('td')):
        if(i % 12 == 0):
            try:
                origin.append(soup.table.find_all('td')[i + 1].find('a').text)
            except:
                pass

    return origin[0:nb_cities]


# API google maps
# https://maps.googleapis.com/maps/api/distancematrix/output?parameters

# nb_cities: limited for free use
nb_cities = 10

origins = get_cities(nb_cities)

origins_str = '|'.join(origins)
destinations_str = origins_str

key_path = osp.join(getenv('HOME'), 'github/googlekey')
try:
    file = open(key_path, 'r')
except:
    print("Error while opening ~/github/googlekey file: please get a personal googlekey and save it in ~/github/googlekey")
YOUR_API_KEY = file.readline()[0:39]

api_url = 'https://maps.googleapis.com/maps/api/distancematrix/'
url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + origins_str + \
    '&destinations=' + destinations_str + \
    '&mode=driving&language=fr-FR&key=' + YOUR_API_KEY

data_json = requests.get(url)
data = data_json.json()

dist = np.zeros([nb_cities, nb_cities])
for i, row_dest in enumerate(data['rows']):
    for j, row_orig in enumerate(data['rows'][i]['elements']):
        dist[i, j] = data['rows'][i]['elements'][j]['distance']['value']

df = pd.DataFrame(dist)
df.columns = origins
df.index = origins
df.to_csv('./cities.csv')