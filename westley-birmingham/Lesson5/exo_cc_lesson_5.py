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

result = requests.get('http://eurekasante.vidal.fr/medicaments/alphabetique/recherche/liste-medicament-I.html').text
soup = BeautifulSoup(result, 'html.parser')
m = soup.find_all(class_='list_item')[0].ul

for mol in soup.find_all(class_='list_item')[0].find_all(class_=''):
    try:
        medic = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(0)
        molecule = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(1)
        labo = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(2)
        labo = re.search(r'(IBUPROFENE|IBUPROFÈNE)\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]),?[a-z]?', mol.text).group(3)
    except:
        m = 0

    if molecule != '':
        print(medic)

#soup.select(".tabscontent > div > li")

#   page:1
#   affliste:0
#   affNumero:0
#   isAlphabet:1
#   inClauseSubst:0
#   nomSubstances:
#   typeRecherche:0
#   choixRecherche:medicament
#   paginationUsed:0
#   txtCaracteres:I
#   radLibelle:2
#   txtCaracteresSub:
#   radLibelleSub:4