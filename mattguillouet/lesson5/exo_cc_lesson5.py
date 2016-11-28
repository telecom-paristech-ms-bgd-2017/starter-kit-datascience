

import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import json
import re
import json
import ipdb


choixRecherche = 'medicament'
medicName = 'levothyroxine'
subName = ''
actionBtn = 'Rechercher'

postParams = {'page': 1,
	'affliste':0,
	'affNumero':0,
	'isAlphabet':0,
	'inClauseSubst':0,
	'nomSubstances':'',
	'typeRecherche':0,
	'choixRecherche':choixRecherche,
	'paginationUsed':0,
	'txtCaracteres':medicName,
	'btnMedic.x':14,
	'btnMedic.y':6,
	'btnMedic':actionBtn,
	'radLibelle':2,
	'txtCaracteresSub':subName,
	'radLibelleSub':4}

baseUrl = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

lines = []

nbPageMax = 10
reMed = re.compile(medicName.upper() + ' ([A-Z ]+) (\d+) ?([\w%]+),([ \w]+)')


for page in range(1,nbPageMax):

	postParams['page'] = page,
	r = requests.post(baseUrl, data=postParams)
	soup = BeautifulSoup(r.content, 'html.parser')
	mainTable = soup.find_all('table', {'class', 'result'})[0]	
	allMed = reMed.findall(mainTable.text)
	lines.extend(allMed)


pdMeds = pd.DataFrame(lines, columns=['brand', 'dose', 'unit', 'type'])

pdMeds.to_csv(medicName + '.csv')



