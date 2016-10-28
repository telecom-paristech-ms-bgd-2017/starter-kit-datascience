# Ibuprofene, Levothyroxine
from bs4 import BeautifulSoup
import requests
import json

URL_SEARCH = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
regex_pattern = '(IBUPROFENE)\s([\w\s]+)\s(\d+)(\smg|\s%), ([a-zA-Zé ]{1,20})'

data = {"choixRecherche": "medicament", "txtCaracteres": "ibuprofene"}


re = requests.post(URL_SEARCH, data=data)
bs = BeautifulSoup(re.text, 'html.parser')

table = bs.find('table', {'class' : 'result'})
table_body = table.find('tbody')
# rows = table_body.find_all('tr')
print(table)
