import requests
from bs4 import BeautifulSoup
import re

url = 'http://base-donnees-publique.medicaments.gouv.fr/'
# data = {'page':1, 'affliste':0, 'affNumero':0, 'isAlphabet':0, 'inClauseSubst':0, 'typeRecherche':1, 'choixRecherche':'substance', 'paginationUsed':0, 'radLibelle':2, 'txtCaracteresSub':'levothyroxine', 'btnSubst':'Rechercher', 'radLibelleSub':4} 

data = {'choixRecherche': 'medicament', 'page': 1, 'radLibelle': 2, 'radLibelleSub': 4, 'txtCaracteres': 'levothyroxine',
                        'typeRecherche': 0}

r = requests.post(url, data)
soup = BeautifulSoup(r.text, 'html.parser')
# soup = BeautifulSoup(open(url))
# soup = BeautifulSoup(r.text, 'lxml')
