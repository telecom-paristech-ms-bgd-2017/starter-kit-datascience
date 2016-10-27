# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame, Series

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
molecules = ["IBUPROFENE"]

def getDrogsListOnPage(page,molecule):
	r = requests.post(url,data=
	{  
   		"page":page,
   		"affliste":0,
   		"affNumero":0,
   		"isAlphabet":0,
   		"inClauseSubst":0,
   		"nomSubstances":"",
   		"typeRecherche":0,
   		"choixRecherche":"medicament",
   		"paginationUsed":0,
   		"txtCaracteres":molecule.lower(),
   		"btnMedic.x":0,
   		"btnMedic.y":0,
   		"btnMedic":"Rechercher",
   		"radLibelle":2,
   		"radLibelleSub":4
	})

	soup = BeautifulSoup(r.text,"html.parser")
	drogList = soup.find_all(class_="standart")

	return drogList

def getDataOnDrog(drog,molecule):
	dataOnDrog = drog['title']
	dataOnDrog.replace("é","e")
	dataOnDrog.replace("è","e")
	dataOnDrog.replace("à","a")
	dico = {}

	m = re.search(molecule.upper() + "\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+),([\w\sé]*)",dataOnDrog)
	if m != None:
		brand = m.group(1)
		mg = m.group(2)
		form = m.group(4)

		dico['Brand'] = brand
		dico['Quantity'] = mg
		dico['Forme'] = form
		dico['Molecule'] = molecule

		return dico
	return None

def getDatasOnPage(page,molecule):
	drogList = getDrogsListOnPage(page,molecule)
	drogDatas = []

	for drog in drogList:
		data = getDataOnDrog(drog,molecule)
		if data != None:
			drogDatas.append(data)

	return drogDatas

def getDatasOnMolecules():
	page = 1
	results = []
	for molecule in molecules:
		datasForMoleculeOnpage = getDatasOnPage(page,molecule)

		while len(datasForMoleculeOnpage) != 0:
			results += (datasForMoleculeOnpage)
			page += 1
			datasForMoleculeOnpage = getDatasOnPage(page,molecule)

		page = 1
	return results

datasAboutDrogs = getDatasOnMolecules()
df = DataFrame(datasAboutDrogs,columns=['Brand','Quantity','Forme','Molecule'])
df.to_csv("Résumé des formes possibles.csv")