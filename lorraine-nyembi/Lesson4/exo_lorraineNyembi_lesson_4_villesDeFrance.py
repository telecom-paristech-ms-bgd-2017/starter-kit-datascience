# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine
"""

import googlemaps
from bs4 import BeautifulSoup
import requests
#import numpy as np
#import pandas as pandas
from pandas import DataFrame

MY_API_KEY = 'AIzaSyBssSgXreMk6aVrlF8YVc1JzSEAWDfW-4c'  # distance API google maps

def loadtopcities(nombreDeVilles):
	url = "http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
	results = requests.get(url)
	soup = BeautifulSoup(results.text,"html.parser")
	tab = soup.find_all("tr")
	array = []

	for i in range(1, nombreDeVilles+1):
		array.append(tab[i].find_all("td")[1].text.replace("\n","").strip())

	return array

def getCitiesDistances(topCities):
	gmaps = googlemaps.Client(key=MY_API_KEY)
	distances = gmaps.distance_matrix(topCities,topCities)['rows']

	INDICATOR = "duration"
	TYPE_INDICATOR = "value"
	clean_distances = []
	for row in distances:
		clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

	df = DataFrame(clean_distances,index=topCities,columns=topCities)

	return df

df = getCitiesDistances(loadtopcities(10))
df.to_csv("indicateurs_distances_villes.csv")