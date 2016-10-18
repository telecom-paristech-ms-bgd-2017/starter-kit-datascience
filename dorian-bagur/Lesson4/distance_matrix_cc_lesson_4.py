import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd


def transformCities(cities):
    result = cities[0]
    for city in cities[1:]:
        result += "|"
        words = city.split(' ')
        result += words[0]
        for word in words[1:]:
            result += "+" + word
    return result


def extractCities(soup):
    citiesTable = soup.find('table').find_all("tr")
    cities = []
    for idx in range(1, 8):
        city = citiesTable[idx].find('b')
        if city is not None:
            cities.append(city.find('a').text)
    return cities


def getCities():
    url = ("https://fr.wikipedia.org/wiki/Liste_des_communes_de_France" +
           "_les_plus_peupl%C3%A9es")
    print(url)
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    return extractCities(soup)


def getDistanceMatrix():
    cities = getCities()
    url = ("https://maps.googleapis.com/maps/api/distancematrix/json?" +
           "origins=" + transformCities(cities) +
           "&destinations=" + transformCities(cities) +
           "&key=AIzaSyCdoGKZQr48MVd_1eUEU48umzFgXGZfsCs"
           )
    print(url)
    res = requests.get(url)
    res = res.json()
    df_distance = pd.DataFrame(columns=cities, index=cities)
    for idx1, row in enumerate(res['rows']):
        for idx2, column in enumerate(row['elements']):
            df_distance[cities[idx1]][cities[idx2]] = column[
                'distance']['text']
    df_duration = pd.DataFrame(columns=cities, index=cities)
    for idx1, row in enumerate(res['rows']):
        for idx2, column in enumerate(row['elements']):
            df_duration[cities[idx1]][cities[idx2]] = column[
                'duration']['text']

    print(df_distance)
    print(df_duration)


getDistanceMatrix()
