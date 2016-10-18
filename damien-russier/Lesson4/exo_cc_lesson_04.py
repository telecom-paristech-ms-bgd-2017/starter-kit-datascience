# -*- coding: utf-8 -*-
'''
Created on 6 oct. 2016

@author: utilisateur
'''

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os

'''
https://github.com/googlemaps/google-maps-services-python
sudo pip install -U googlemaps

import googlemaps
distances = gmaps.distances(villes)

json editor online
'''

# Appel de Google Maps Distance Matrix API
key = os.environ.get('GMAPSAPI_KEY')


def get_villes(n=30):
    url = 'http://www.insee.fr/fr/themes/tableau.asp?reg_id=0&ref_id=nattef01214'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tmp = soup.find_all(class_="etendue-ligne")
    villes = []
    count = 0
    for t in tmp:
        # print t.text
        villes.append(t.text)
        count += 1
        if (count >= n):
            break
    return villes

villes = get_villes()

distances = pd.DataFrame()
distances_ = []
for v1 in villes:
    lst = []
    for v2 in villes:
        url = "https://maps.googleapis.com/maps/api/distancematrix/" +\
        "json?units=imperial&origins=" +\
        v1 + "&destinations=" + v2 + "&key=" + key
        r = requests.get(url)
        data = r.json()
        # print data
        strg = "Distance %15s %15s : " % (v1, v2)
        try:
            dist = data['rows'][0]['elements'][0]['distance']['value']
            dist /= 1000.
            strg += "%11.2f km" % (dist)
        except KeyError:
            dist = None
            strg += "no value found"
        # print strg
        distances = distances.append({'ville1': v1,
                                      'ville2': v2,
                                      'distance': dist},
                                     ignore_index=True)
        lst.append(dist)
    distances_.append(lst)

df = pd.DataFrame(distances_, index=villes, columns=villes)
df.to_csv('distances.csv', encoding="utf-8")
