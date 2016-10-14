from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint
from collections import defaultdict

api_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
wiki = "https://en.wikipedia.org/wiki/List_of_the_75_largest_cities_in_France_(2012_census)"
api_key = "AIzaSyDDpsy7cH3x2QsA2fKgU4F_OOhwxHCk3Wo"

def get_cities():
    soup = BeautifulSoup(requests.get(wiki, 'html').text, 'html.parser')
    table = soup.select("#mw-content-text table")[0]
    rows = table.select("tr")[1:11]
    return [row.select('td')[0].text for row in rows]

def get_distance(c1, c2):
    params = {'origins': c1, 'destinations': c2, 'key': api_key}
    resp = requests.get(api_url, params=params)
    return json.loads(resp.text)['rows'][0]['elements'][0]['distance']['value']


cities = get_cities()
cities_copy = cities.copy()
distances = defaultdict(lambda: {})
for c1 in cities:
    cities_copy.remove(c1)
    for c2 in cities_copy:
        distances[c1][c2] = get_distance(c1, c2)

pprint(distances)