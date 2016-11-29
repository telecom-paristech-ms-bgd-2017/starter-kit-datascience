import requests
from bs4 import BeautifulSoup
import re


result = requests.post('http://eurekasante.vidal.fr/medicaments/alphabetique/recherche/liste-medicament-I.html').text
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