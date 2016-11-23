import googlemaps
import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

def get_google_token():
    with open('token.txt') as f:
        return f.read()

API_KEY = get_google_token()

gmaps = googlemaps.Client(key=API_KEY)

villes = ['Paris','Lille','Marseille','Lyon','Strasbourg','Nantes','Nice','Bordeaux','Toulouse']

distances = gmaps.distance_matrix(villes, villes)['rows']

INDICATOR_duration = 'duration'
INDICATOR_distance = 'distance'
TYPE_INDICATOR = 'value'

clean_durations = []
clean_distances = []
for row in distances:
  clean_durations.append(map(lambda x: x[INDICATOR_duration][TYPE_INDICATOR], row['elements']))
  clean_distances.append(map(lambda x: x[INDICATOR_distance][TYPE_INDICATOR], row['elements']))

#clean_distances = map(lambda row: map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']) , distances)

df = DataFrame(clean_durations,index=villes,columns=villes)
df.to_csv(INDICATOR_duration + '.csv')

df = DataFrame(clean_distances,index=villes,columns=villes)
df.to_csv(INDICATOR_distance + '.csv')

