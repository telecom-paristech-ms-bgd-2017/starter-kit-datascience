# -*- coding: utf-8 -*-

import requests
import bs4
import os
import pandas as pd
import json
import numpy as np
from unidecode import unidecode
import re
import pdb

base_url = "http://base-donnees-publique.medicaments.gouv.fr/"
index_url = "index.php"
regex_medicament = " (([a-zA-Z]|\s)*)([0-9]+[ ]?[a-zA-Z]*|\/)+([ [\w\-]*]?),([\w\s]*)"

def analyser_medicament(medicament):
	tab = pd.DataFrame()
	page = 1
	continuer = True
	while(continuer):
		res = analyser_page(page, medicament)
		tab = pd.concat([tab, res])
		if len(res) == 0: continuer = False
		page = page + 1
	tab.to_csv(medicament+".csv", index = False)

def analyser_page(page, medicament):

	param = {'affNumero':0,
	'affliste':0,
	'btnMedic':'Rechercher',
	'btnMedic.x':12,
	'btnMedic.y':7,
	'choixRecherche':'medicament',
	'inClauseSubst':0,
	'isAlphabet':0,
	'nomSubstances':'',
	'page':page,
	'paginationUsed':0,
	'radLibelle':2,
	'radLibelleSub':4,
	'txtCaracteres':medicament,
	'txtCaracteresSub':'',
	'typeRecherche':0}

	r = requests.post(base_url + index_url, data = param)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')

	res = []

	b = soup.find_all("a")
	for i in range(0, len(b)):
		try:
			string_medicament_complet = str.upper(unidecode(b[i]["title"]))
			if string_medicament_complet.find(unidecode(str.upper(medicament))) > 0:

				# Récupération de la présentation (dans la page de la fiche du médicament)
				lien_fiche_medicament = unidecode(b[i]["href"])
				rfiche = requests.get(base_url + lien_fiche_medicament)
				soupfiche = bs4.BeautifulSoup(rfiche.content, 'html.parser')
				presentation = unidecode(soupfiche.find("h2", class_ = "titrePresentation").text).replace(">","").strip()

				# Récupération des autres infos sur le médicament par expression régulière
				medicament_complet = string_medicament_complet.split(":")[1].strip()
				regex_medicament_complet = str.upper(medicament) + regex_medicament
				try:
					split = re.split(regex_medicament_complet,medicament_complet)
					print medicament_complet, split
					if(len(split) != 1):
						res.append([str.upper(medicament), split[1].strip(), split[3].strip(), split[4].strip(), split[-2].strip(), presentation])
					else:
						print "Pas de match regex avec la description "+ medicament_complet
				except AttributeError:
					print "Pas trouvé regex " + medicament_complet
		except KeyError:
			continue

	return pd.DataFrame(res, columns=("MEDICAMENT","MARQUE","POSOLOGIE","AUTRE INFO","FORME", "PRESENTATION"))
