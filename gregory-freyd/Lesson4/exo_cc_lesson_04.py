import googlemaps
import json
import numpy as np
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series
import requests
from bs4 import BeautifulSoup

# Phase 1 : gathering biggest towns from lavieimmo.com

tab_cities = []
top_cities = requests.get("http://www.lavieimmo.com/population-des-villes/classement/")

soup_cities = BeautifulSoup(top_cities.text, 'html.parser')
list_cities = soup_cities.find_all(class_="tl")

for city in list_cities:
    tab_cities = np.append(tab_cities, city.find("strong").text)

print(tab_cities)

# Phase 2 : retrieving distance and duration for trips between each town
# and storing them as csv files

API_KEY = 'AIzaSyBqSNsLlbzAIAXi8f-Enx1q1F0ITToWGTs'

gmaps = googlemaps.Client(key=API_KEY)

villes = tab_cities[0:10]

distances = gmaps.distance_matrix(villes, villes, mode="driving")['rows']

INDICATOR = 'distance'
TYPE_INDICATOR = 'value'

clean_distances = []
for row in distances:
    clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

df = DataFrame(clean_distances,index=villes,columns=villes)
df.to_csv(INDICATOR + '.csv')

INDICATOR = 'duration'
TYPE_INDICATOR = 'value'

clean_distances = []
for row in distances:
    clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

df = DataFrame(clean_distances,index=villes,columns=villes)
df.to_csv(INDICATOR + '.csv')