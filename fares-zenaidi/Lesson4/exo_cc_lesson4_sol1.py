# @ author : ZENAIDI Fares
# coding = utf8

from bs4 import BeautifulSoup
import requests
import numpy as np
import json
from pandas import DataFrame, Series
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
# Part II - Use the Google Map's Distance Matrix API                                                                   #
########################################################################################################################
def get_distance_matrix():
    top_cities = extract_top_cities(30)[:7]
    adapted_top_cities = adapt_to_api_syntax(top_cities)  # Only the 7 biggest cities

    # i) Read from file the API_KEY
    with open('Google_API_Key', mode='r') as f:
        api_key = f.read()

    # ii) Requests the Distance Matrix API
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&keys={}' \
          .format(adapted_top_cities, adapted_top_cities, api_key)

    r = requests.get(url)
    res = json.loads(r.text)  # Convert the json-response into a dictionary of key-value pairs
    df_distances = DataFrame(index=top_cities, columns=top_cities)  # DF modeling the distance matrix

    for idx1, line in enumerate(res['rows']):
        for idx2, column in enumerate(line['elements']):
            df_distances[top_cities[idx1]][top_cities[idx2]] = column['distance']['text']

    print(df_distances)


get_distance_matrix()


