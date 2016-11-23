# Ibuprofene, Levothyroxine
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

import json

URL_SEARCH = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
regex_pattern = '(IBUPROFENE)\s([\w\s]+)\s(\d+)(\smg|\s%), ([a-zA-Zé ]{1,20})'

data = {"choixRecherche": "medicament", "txtCaracteres": "ibuprofene"}


req = requests.post(URL_SEARCH, data=data)
bs = BeautifulSoup(req.text, 'html.parser')

table = bs.find('table', {'class' : 'result'})
table_body = table.find('tbody')
rgx = re.compile(regex_pattern, re.IGNORECASE)
rgx_all = rgx.findall(table.text)

columns = ['MOLECULE', 'NAME', 'DOSAGE_VALUE', 'DOSAGE_UNIT',
           'FORMAT']

df = pd.DataFrame(data=rgx_all, columns=columns)

print(df)
