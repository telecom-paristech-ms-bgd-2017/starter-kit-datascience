from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

# get distance between 30th largest city in France
key = "AIzaSyCJudelv_JghVtAj0fKKLaFK_WIcdEdiUs"
def get_distance(ville_origine, ville_destination):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + ville_origine + '&destinations=' + ville_destination + '&language=fr-FR&'+key
    jsonData = requests.get(url)
    jsonToPython = json.loads(jsonData.text)
    temp = jsonToPython['rows'][0]
    temp2 = temp['elements'][0]
    dist = temp2['distance']['value']
    return dist


cities = ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille',
          'Rennes', 'Reims', 'Le Havre', 'Saint-Etienne', 'Toulon', 'Grenoble', 'Dijon', 'Nîmes', 'Angers',
          'Villeurbanne', 'Le Mans', 'Aix-en-Provence', 'Clermont-Ferrand', 'Brest', 'Limoges', 'Tours', 'Amiens',
          'Perpignan', 'Metz']

#Create square matrix
distances_matrix = np.zeros((len(cities), len(cities)))

# Compute half the matrix since it's symetric.
# Saves us half the calls to the API
for i in range(len(cities)):
    for j in range(i,len(cities)):
        distances_matrix[i][j] = get_distance(cities[i], cities[j])

for i in range(len(cities)):
    for j in range(i, len(cities)):
        distances_matrix[j][i] = distances_matrix[i][j]

distances_df = pd.DataFrame(distances_matrix, columns=cities, index=cities)
distances_df.to_csv('distances.csv', sep=';', encoding='utf-8')
