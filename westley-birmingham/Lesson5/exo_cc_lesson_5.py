import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import pandas as pd
import re

#   Exercice Lesson5
#---------------------------------------------------------------------------------------------------------------
#   Récupération de la liste des molécules IBUPROFENE etc...
#   requete post + utilisation regex
#   Propal url :    http://base-donnees-publique.medicaments.gouv.fr/index.php#result
#   alternative url : http://eurekasante.vidal.fr/medicaments/alphabetique/recherche/liste-medicament-I.html

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'

''''
result = requests.get('http://eurekasante.vidal.fr/medicaments/alphabetique/recherche/liste-medicament-I.html').text
soup = BeautifulSoup(result, 'html.parser')
m = soup.find_all(class_='list_item')[0].ul
'''

molecule = ["ibuprofene"]
page = 1

params_post = {"page":page,
   		"affliste":0,
   		"affNumero":0,
   		"isAlphabet":0,
   		"inClauseSubst":0,
   		"nomSubstances":"",
   		"typeRecherche":0,
   		"choixRecherche":"medicament",
   		"paginationUsed":0,
   		"txtCaracteres":molecule,
   		"btnMedic.x":0,
   		"btnMedic.y":0,
   		"btnMedic":"Rechercher",
   		"radLibelle":2,
   		"radLibelleSub":4}



response = requests.post(url, data=params_post)
soup = BeautifulSoup(response.text, 'html.parser')
medoc_selected = soup.find_all(class_='standart')

dico_medoc = {}


for mol in medoc_selected:
    mol_detail = []
    try:
        medic = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(0)
        molecule = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(1)
        labo = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(2)
        dosage = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(3)
    except:
        m = 0

    if molecule != '':
        mol_detail.append(molecule)
        mol_detail.append(labo)
        mol_detail.append(dosage)
        dico_medoc[medic] = mol_detail
        print(medic)
        print(molecule)
        print(labo)
        print(dosage)

print(dico_medoc)
