import requests
import json
from bs4 import BeautifulSoup

API_KEY = 'AIzaSyBOuK5dIloWttaUKwCCoQ2apYaaWtTU840'
BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&key={2}'

#Vancouver+BC|Seattle
# Main script

def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_30_biggest_cities_france():
    url = 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'
    bs = getBeautifulSoupObjectfromUrl(url)
    table = bs.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    cities = []
    for row in rows:
        cols = row.find_all('td')
        c = cols[0]
        city = c.next.text
        cities.append(city)
    return cities


def build_cities_url(cities):
    res = cities[0]
    for i in range(1, len(cities)):
        c = cities[i]
        res += '|' + c
    return res


cities = ['Paris', 'Marseille', 'Lyon']
cities_2 = get_30_biggest_cities_france()
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
        dist = el['distance']
        res = origin, dest, dist
        results.append(res)
        print(res)
        j += 1
    i += 1



# print(g_map_res.text)
