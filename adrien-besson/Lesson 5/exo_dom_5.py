# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame, Series

regions = ['provence_alpes_cote_d_azur','aquitaine','ile_de_france']
versions = [{"Version":"INTENS TYPE 2","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide+type+2-2013.html"}
	,{"Version":"INTENS","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2013.html"},
	{"Version":"LIFE","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide-2013.html"},
	{"Version":"LIFE TYPE 2","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide+type+2-2013.html"},
	{"Version":"ZEN","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide-2013.html"},
	{"Version":"ZEN TYPE 2","URL":"http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide+type+2-2013.html"}]

def getArgusPrices():
	dico = {}

	for version in versions:
		url = version['URL']

		r = requests.get(url=url)
		soup = BeautifulSoup(r.text,"html.parser")

		nom = version['Version']
		dico[nom] = float(soup.find_all(class_="bGrey9L")[0].text.strip().replace(" ","").replace("€",""))

	return dico

def getPropertiesOfCar(properties):
	dico = {}
	for prop in properties:
		if prop.text.lower() == "prix":
			priceString = prop.parent.find_all(class_="value")[0].text.strip()
			m = re.search('(\d* *\d*),?(\d*)',priceString)
			if m == None:
				dico['Prix'] = None
			else:
				dico['Prix'] = float(m.group(1).replace(" ",""))

		if prop.text.lower() == "kilométrage":
			kmString = prop.parent.find_all(class_="value")[0].text.strip()
			m = re.search('(\d* \d*)',kmString)
			if m == None:
				dico['Km'] = None
			else:
				dico['Km'] = float(m.group(1).replace(" ",""))

		if prop.text.lower() == "année-modèle":
			yearString = prop.parent.find_all(class_="value")[0].text.strip()
			dico['Year'] = int(yearString)

		if prop.text.lower() == "description :":
			description = prop.parent.find_all(class_="value")[0].text.strip()
			m = re.search('(LIFE|INTENS|ZEN) *(TYPE *2)?',description.upper())
			if m == None:
				dico['Version'] = None
			else:
				dico['Version'] = m.group(0).strip()
			
			m = re.search("(0|\+33)[1-9]([-. ]?[0-9]{2}){4}",description)
			if m == None:
				dico['Phone'] = None
			else:
				dico['Phone'] = m.group(0)
	return dico

def getData(article,region,argus):
	pro = (len(article.find_all(class_="ispro")) > 0)

	urlArticle = "http:" + article['href']

	rarticle = requests.get(url=urlArticle)
	soupArticle = BeautifulSoup(rarticle.text,"html.parser")
	propertiesArticle = soupArticle.find_all(class_="property")

	dico = getPropertiesOfCar(propertiesArticle)
	dico['Pro'] = pro
	dico['Region'] = region
	dico['Lien vers l\'annonce'] = urlArticle

	if dico['Version'] == None:
		dico['Argus'] = None
	else:
		dico['Argus'] = argus[dico['Version']]
		dico['Prix plus haut que l\'Argus'] = dico['Prix'] > dico['Argus']

	return dico

def getArticlesForRegionAndPage(region,page,argus):
	url = "https://www.leboncoin.fr/voitures/offres/" + region + "/?o=" + str(page) + "&brd=Renault&mdl=Zoe"
	r = requests.get(url=url)
	soup = BeautifulSoup(r.text,"html.parser")

	articles = soup.find_all(class_='list_item')
	data = []

	for item in map(lambda x: getData(x,region,argus),articles):
		data.append(item)
	return data

def getArticlesForRegion(region,argus):
	datas = getArticlesForRegionAndPage(region,1,argus)
	tmp = getArticlesForRegionAndPage(region,2,argus)

	page = 2
	while len(tmp) > 0:
		datas += tmp
		page += 1

		tmp = getArticlesForRegionAndPage(region,page,argus)

	return datas

def getArticles():
	datas = []
	argus = getArgusPrices()

	for item in map(lambda x: getArticlesForRegion(x,argus),regions):
		datas += item

	return DataFrame(datas,columns=['Region','Prix','Version','Year','Km','Phone','Pro','Argus','Prix plus haut que l\'Argus','Lien vers l\'annonce'])

def annonces():
	annonces = getArticles()
	annonces.to_csv("Résultat de la recherche.csv")
	print(annonces)
	return

annonces()