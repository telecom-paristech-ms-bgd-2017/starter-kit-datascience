#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import urllib

targets = ['ibuprofene','levothyroxine']

target_med = 'ibuprofene'

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

form_data = {
'page':'1',
'affliste':'0',
'affNumero':'0',
'isAlphabet':'0',
'inClauseSubst':'0',
'nomSubstances':'',
'typeRecherche':'0',
'choixRecherche':'medicament',
'paginationUsed':'0',
'txtCaracteres':target_med,
'btnMedic.x':'13',
'btnMedic.y':'14',
'btnMedic':'Rechercher',
'radLibelle':'1',
'txtCaracteresSub':'',
'radLibelleSub':'4',
}

res = requests.post(url, data=form_data)
soup = BeautifulSoup(res.text, 'html.parser')

meds = [x.text for x in soup.find_all(class_="standart")]
meds = pd.Series(meds)
meds = meds.str.strip()

regex_name = re.compile(r''+target_med.upper()+' \D+')
regex_dosage = re.compile(r'\d+( |)(mg|g|%|µg|microgrammes)')
regex_galenic = re.compile(r'[,] [\D+]*')

name = list(map(lambda x:regex_name.search(x), meds))
dosage = list(map(lambda x:regex_dosage.search(x), meds))
galenic = list(map(lambda x:regex_galenic.search(x), meds))

def matchToString(matchlist):
	for i,match in enumerate(matchlist):
		if(match != None):
			matchlist[i] = matchlist[i].group(0)
	return matchlist

name = matchToString(name)
dosage = matchToString(dosage)
galenic = matchToString(galenic)
