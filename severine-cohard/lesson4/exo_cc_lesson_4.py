# Scraping Google maps

# pour les 30 plus grandes villes de France, calculer les distances des unes aux autres

import googlemaps
import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

API_KEY = 'AIzaSyC5jZ5jCw8bFgXoLX5RJ5IKge7CXi4zI0Q'

gmaps = googlemaps.Client(key=API_KEY)

villes = ['Paris','Lille','Marseille','Lyon','Strasbourg','Nantes','Nice','Bordeaux','Toulouse']

distances = gmaps.distance_matrix(villes, villes)['rows']

INDICATOR = 'duration'
TYPE_INDICATOR = 'value'

clean_distances = []
for row in distances:
  clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

#clean_distances = map(lambda row: map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']) , distances)

df = DataFrame(clean_distances,index=villes,columns=villes)
df.to_csv(INDICATOR + '.csv')