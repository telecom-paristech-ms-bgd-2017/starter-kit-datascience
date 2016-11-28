# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:00:12 2016

@author: arthurouaknine
"""


from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import pandas as pd
import googlemaps
import pandas as pd
from pandas import DataFrame, Series


API_KEY = 'AIzaSyDhBfdYTWeAuPBLPjftqvc0zFqY1dXFL58'

villes = ['Paris','Marseille','Lyon','Strasbourg','Lille','Nantes']
# A compléter : liste des 30 villes les plus peuplées
# Scrapping wikipedia ou fichier INSEE

gmaps = googlemaps.Client(key=API_KEY)

distances = gmaps.distance_matrix(villes,villes)['rows']

#json.load(result_from_api)
clean_distances = []
for row in distances:
    clean_distances.append(map(lambda x: int(x['distance']['text'].replace(' km','').replace(' m','').replace(',','')), row['elements']))

dfDistances = DataFrame(clean_distances,index=villes,columns=villes)
