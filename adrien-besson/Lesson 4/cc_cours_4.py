# coding: utf-8

import googlemaps
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pandas
from pandas import DataFrame, Series

KEY = "AIzaSyC25MB-QEpUPRlhXh8wQ9wl5XORb8RReek"

def loadtopcities(nbVille):
	url = "http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
	r = requests.get(url)
	soup = BeautifulSoup(r.text,"html.parser")
	tab = soup.find_all("tr")
	array = []

	for i in range(1,nbVille+1):
		array.append(tab[i].find_all("td")[1].text.replace("\n","").strip())

	return array

def getDistances(topCities):
	gmaps = googlemaps.Client(key=KEY)
	distances = gmaps.distance_matrix(topCities,topCities)['rows']

	INDICATOR = "duration"
	TYPE_INDICATOR = "value"
	clean_distances = []
	for row in distances:
		clean_distances.append(map(lambda x: x[INDICATOR][TYPE_INDICATOR], row['elements']))

	df = DataFrame(clean_distances,index=topCities,columns=topCities)

	return df

df = getDistances(loadtopcities(10))
df.to_csv("distances_villes.csv")