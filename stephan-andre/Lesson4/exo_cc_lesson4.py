# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:10:42 2016

@author: Stephan
"""
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

#distances entre les 30 villes les plus peuplées de France
def get_distance(ville_origine, ville_destination):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + ville_origine + '&destinations=' + ville_destination + '&language=fr-FR&key=AIzaSyA2hd2XS6kZr6sUL0eTdYWCfNnoY22QFuE'
    jsonData = requests.get(url)
    jsonToPython = json.loads(jsonData.text)
    temp = jsonToPython['rows'][0]
    temp2 = temp['elements'][0]
    dist = temp2['distance']['value']
    return dist

villes = ['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Strasbourg','Montpellier','Bordeaux','Lille','Rennes','Reims','Le Havre','Saint-Etienne','Toulon','Grenoble','Dijon','Nîmes','Angers','Villeurbanne','Le Mans','Aix-en-Provence','Clermont-Ferrand','Brest','Limoges','Tours','Amiens','Perpignan','Metz']

distance_matrice = np.zeros((len(villes), len(villes)))

for i in range(len(villes)):
    for j in range(len(villes)):
        distance_matrice[i][j] = get_distance(villes[i], villes[j])
        
matrice = pd.DataFrame(distance_matrice, columns = villes, index = villes)
matrice.to_csv('dvilles.csv', sep=';', encoding='utf-8')