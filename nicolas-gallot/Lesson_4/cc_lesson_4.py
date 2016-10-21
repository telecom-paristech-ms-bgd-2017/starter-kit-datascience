import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re

API_KEY = 'AIzaSyBOuK5dIloWttaUKwCCoQ2apYaaWtTU840'
BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}'
URL_CITIES_RANKING = 'http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/'

#Vancouver+BC|Seattle
# Main script

def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_biggest_cities_france(bumber):
    url = URL_CITIES_RANKING
    bs = getBeautifulSoupObjectfromUrl(url)
    table = bs.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    cities = []
    for r in range(1, bumber+1):
        row = rows[r]
        cols = row.find_all('td')
        c = cols[1]
        cities.append(c.text.strip().replace("-", "+"))
    return cities


def build_cities_url(cities):
    res = cities[0]
    for i in range(1, len(cities)):
        c = cities[i]
        res += '|' + c
    return res

cities = get_biggest_cities_france(10)
cities_url = build_cities_url(cities)
g_map_res = requests.get(BASE_URL.format(cities_url, cities_url, API_KEY))
json = json.loads(g_map_res.text)
rows = json['rows']

i = 0

results = []
for r in rows:
    origin = cities[i]
    elts = r['elements']
    j = 0
    for el in elts:
        dest = cities[j]
        dist = el['distance']['value']
        res = origin, dest, dist
        results.append(res)
        j += 1
    i += 1

print(results)
