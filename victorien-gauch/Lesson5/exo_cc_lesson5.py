import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import re

pages = [1,2,3]

def getContent(page):
	params = {
		"page" : page, 
		"affliste" : 0,
		"affNumero" : 0,
		"isAlphabet" : 0,
		"inClauseSubst" : 0,
		"nomSubstances" : "",
		"typeRecherche" : 0,
		"choixRecherche" : "medicament",
		"paginationUsed" : 0,
		"txtCaracteres" : "ibuprofene",
		"btnMedic.x" : 0,
		"btnMedic.y" : 0,
		"btnMedic" : "Rechercher",
		"radLibelle" : 2,
		"radLibelleSub" : 4
	}
	r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php', data = params)
	soup = BeautifulSoup(r.text,'html.parser')
	liste1 = []

	for el1 in soup.find_all(class_='standart'):
		liste1.append(el1.get('title'))

	return liste1


def getAllContentPages():
	liste2 = []
	for page in pages:

		liste1 = getContent(page)
		for el2 in liste1:
			dico = {}
			regex = re.search('(IBUPROFENE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+),([\w\sé]*)',el2)
			if regex == None:
				continue
			else:
				dico['marque'] = regex.group(2).strip()
				dico['molecule'] = regex.group(1).strip()
				dico['forme'] = regex.group(5).strip()
				dico['quantite'] = regex.group(3).strip() + ' ' + regex.group(4).strip()
			
			liste2.append(dico)
	return DataFrame(liste2)

def generate_csv(listeMedocs):
	listeMedocs.to_csv('Médicaments.csv')

liste2 = getAllContentPages()
generate_csv(liste2)


