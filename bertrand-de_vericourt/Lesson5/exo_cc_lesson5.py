# à chaque médicament => MOLÉCULE, DOSAGE, FORME GALÉNIQUE, MARQUE
# médicaments contenant de la levothyroxine OU médicament: de l'ibuprofène, par exemple.
# http://base-donnees-publique.medicaments.gouv.fr/
# mettre ces données dans un dataframe

################################ SCRAP MEDICAMENTS ################################

import requests
from bs4 import BeautifulSoup
import re

keyword = 'ibuprofene'
urlPost = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
data = {
'page':1,
'affliste':0,
'affNumero':0,
'isAlphabet':0,
'inClauseSubst':0,
'typeRecherche':0,
'choixRecherche':'medicament',
'paginationUsed':0,
'txtCaracteres':keyword,
'btnMedic.x':0,
'btnMedic.y':0,
'radLibelle':2,
'radLibelleSub':4
}

response = requests.post(urlPost, data=data)
soup = BeautifulSoup(response.text, 'html.parser')
medic = soup.find_all('a', class_='standart')

for m in medic:
	string = str(m)
	regexp = r"(IBUPROFENE[A-Z ]*[0-9]+\s(%|mg), [a-zé ])+"
	if re.findall(regexp, string) != []:
		print(re.findall(regexp, string))