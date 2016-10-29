import requests
from bs4 import BeautifulSoup
import pandas as pd

#IBUPROFENE\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+), ([\w\sé]+)

#url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/', data = {'affliste':'0', 'affNumero':'0','isAlphabet':'0', 'inClauseSubst':'0', 'typeRecherche':'0','choixRecherche':'0', 'paginationUsed':'0'})
soup = BeautifulSoup(r.text, 'html.parser')
