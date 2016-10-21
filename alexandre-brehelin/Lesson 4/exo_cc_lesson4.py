

from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 


def create_data_city(nb_city):

	url = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"
	nb_city = (2 * nb_city) + 2 
	page_city = requests.get(url)
	soup = BeautifulSoup(page_city.text, 'html.parser') 	
	list_city = []
	for i in range(2,nb_city,2) :
		list_city.append(soup.select("b")[i].text.replace("\xa0",''))

	return list_city

def add_city_matrix(liste):
	liste_columns= liste
	liste_index = liste
	data_city = pd.DataFrame(index=liste, columns=liste_columns)
	return data_city



def ext_distance(origin,destination):
	
	url ='https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+'&destinations='+destination
	ext_url = requests.get(url)
	source = ext_url.json()

	distance = source["rows"][0]["elements"][0]["distance"]["text"].replace(","," ")
	return distance



ma_liste = create_data_city(30)
data_ma_liste = add_city_matrix(ma_liste)

for i in data_ma_liste.index :
	for j in data_ma_liste.columns:
		data_ma_liste.loc[i,j] = ext_distance(i,j)