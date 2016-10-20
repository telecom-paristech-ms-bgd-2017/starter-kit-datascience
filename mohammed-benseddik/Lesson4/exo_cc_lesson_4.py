# @ Author : BENSEDDIK Mohammed

import requests
import googlemaps
from bs4 import BeautifulSoup
import pandas as pd

# Crawling des plus grandes villes :
url_wiki = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"
r = requests.get(url_wiki)
soup = BeautifulSoup(r.text, 'html.parser')

rows = list()
columns = []
villes = []

table = soup.find("table")

for row in table.find_all("tr"):
    rows.append(row)

for row in rows:
    columns.append(row.find_all("td"))

columns.pop(0)

for column in columns:
    villes.append(column[1].text)
# correction de l'orthographe Lille depuis wiki
villes[9] = 'Lille'

# API goolemaps Distance Matrix :
API_KEY = open('googlekey.txt', 'r').read().rstrip()
INDICATOR_DURATION = 'duration'
INDICATOR_DSITANCE = 'distance'
TYPE_INDICATOR = 'value'
villes_tp = villes[:10]
print(villes_tp)

gmaps = googlemaps.Client(key=API_KEY)

distances = gmaps.distance_matrix(villes_tp, villes_tp)['rows']

clean_distances = []
for row in distances:
    clean_distances.append(
        map(lambda x: x[INDICATOR_DSITANCE][TYPE_INDICATOR], row['elements']))


clean_durations = []
for row in distances:
    clean_durations.append(
        map(lambda x: x[INDICATOR_DURATION][TYPE_INDICATOR], row['elements']))

df_distances = pd.DataFrame(
    clean_distances, index=villes_tp, columns=villes_tp)
df_durations = pd.DataFrame(
    clean_durations, index=villes_tp, columns=villes_tp)

df_distances.to_csv(INDICATOR_DSITANCE + '.csv')
df_durations.to_csv(INDICATOR_DURATION + '.csv')
