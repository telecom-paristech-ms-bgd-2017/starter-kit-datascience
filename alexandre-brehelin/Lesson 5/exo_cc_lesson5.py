#Exercie médicament
#Prendre levotyroxine ou ibuprofène
#sur le site national des médicaments
#utiliser requete post et trouver les détails par regex 
 
from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def patterT(x,resultat) :

	patter_ibu = ("[A-Z]{10}\s*([A-Z]+)")
	find = re.compile(patter_ibu).search(resultat[x].text.strip())
	mod = find.group()

	patter_dose = ("([0-9]{3}\s*([a-z]+)|[0-9]{1}\s*(%))|[0-9]{2}\s*([a-z]{2}\W*[a-z]{2})")
	find_dose = re.compile(patter_dose).search(resultat[x].text.strip())
	dose = find_dose.group()

	patter_type = (",(.+)|%(.+)")
	find_type = re.compile(patter_type).search(resultat[x].text.strip())
	type_m = find_type.group().replace("%","").replace(",","")[1:]

	value_return = {'Molécule': mod, 'dose':dose,'ingérence' : type_m}

	return value_return





url = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
columns_name = ['Molécule','dose','ingérence']
data = pd.DataFrame(columns=columns_name)


j = 0
for i in range(1,4):

	page_medoc= requests.post(url, data = {"page":str(i), \
				"affliste": str(j), \
				"affNumero":"0", \
				"isAlphabet":"0", \
				"inClauseSubst":"0", \
				"typeRecherche":"0", \
				"choixRecherche":"medicament", \
				"paginationUsed": str(j), \
				"txtCaracteres":"ibuprofene", \
				"radLibelle":"2", \
				"radLibelleSub":"4" })
	
	soup_med = BeautifulSoup(page_medoc.text, 'html.parser') 	
	resultat = soup_med.find_all(class_="ResultRowDeno")
	
	for v in range(len(resultat)):
		
		it_dict = patterT(v,resultat)
		data = data.append(it_dict, ignore_index=True)

	j = 1


path = "/home/brehelin/Documents/Kit Data Science/starter-kit-datascience/alexandre-brehelin/Lesson 5/"
data.to_csv(path + "export_ibuprofene.csv")







