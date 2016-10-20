import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import re

regions = ['ile_de_france','provence_alpes_cote_d_azur','aquitaine']
pages = [1, 2]

def get_data(region,page):
	
	url = requests.get('https://www.leboncoin.fr/voitures/offres/' + region + '/?o=' + str(page) + '&brd=Renault&mdl=Zoe')
	soup = BeautifulSoup(url.text,'html.parser')
	
	links = []
	
	list_cars= map(lambda x: 'https:' + x['href'] , soup.find_all(class_="list_item"))
	for link in list_cars:
		links.append(link)

	return links

def get_item_content(link):
	
	dico = {}
	result = requests.get(link)
	soup = BeautifulSoup(result.text, 'html.parser')
	car_properties = soup.find_all(class_='property')

	for car_property in car_properties:
		if car_property.text.lower() == 'prix':
			
			value = car_property.parent.find(class_='value').text.strip()
			regex = re.search('(\d* *\d*),?(\d*)',value)
			if regex == None:
				dico['Prix'] = None
			else:
				dico['Prix'] = float(regex.group(1).replace(' ',''))

		if car_property.text.lower() == 'année-modèle':
			value = car_property.parent.find(class_='value').text.strip()
			dico['Année'] = int(value)

		if car_property.text.lower() == 'kilométrage':
			value = car_property.parent.find(class_='value').text.strip()
			regex = re.search('(\d* \d*)',value)
			if regex == None:
				dico['Km'] = None
			else:
				dico['Km'] = float(regex.group(1).replace(' ',''))

		if car_property.text.lower() == 'description :':
			value = car_property.parent.find_all(class_='value')[0].text.strip()
			regex = re.search('(0|\+33)[1-9]([-. ]?[0-9]{2}){4}',value)
			if regex == None:
				dico['Phone'] = None
			else:
				dico['Phone'] = regex.group(0)

			regex = re.search('(LIFE|INTENS|ZEN)',value.upper())
			if regex == None:
				dico['Version'] = None
			else:
				dico['Version'] = regex.group(0).strip()

	isPro = (len(soup.find_all(class_="ispro")) > 0)
	if isPro == True:
		dico['Pro'] = 'Véhicule professionnel'
	else:
		dico['Pro'] = 'Véhicule particulier'
	
	return dico
	
def get_All_content(links):
	liste = []
	
	for link in links:
		liste.append(get_item_content(link))
	return DataFrame(liste)

def generate_csv(dataframe):
	dataframe.to_csv("Renault Zoé.csv")


all_links = []

for region in regions:
		for page in pages:
			all_links += get_data(region,page)

listeCars = get_All_content(all_links)
generate_csv(listeCars)






