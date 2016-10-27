#coding: utf8

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
result = pd.DataFrame(columns=['Medicament', 'Dose', 'Unite', 'Type'])

for page in range(4):
    payload = requests.post(url, {
        "page": page,
        "affliste": 0,
        "affNumero": 0,
        "isAlphabet": 0,
        "inClauseSubst": 0,
        "nomSubstances": '',
        "typeRecherche": 0,
        "choixRecherche": 'medicament',
        "txtCaracteres": 'ibuprofene',
        "btnMedic.x": '20',
        "btnMedic.y": '20',
        "btnMedic": 'Rechercher',
        "radLibelle": 2,
        "txtCaracteresSub": '',
        "radLibelleSub": 4})

    soup = BeautifulSoup(payload.text, 'html.parser')
    links = soup.findAll('a', {'class': 'standart'})
    for a in links:
        text = a.get_text()
        regex = re.findall(r'(.*)\s(\d{2,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)', text)
        try :

            result = result.append({
                'Medicament': (regex[0][0].encode('utf-8') + ' ' + regex[0][3].encode('utf-8')).strip(),
                'Dose': int(regex[0][1]),
                'Unite': regex[0][2].encode('utf-8'),
                'Type': regex[0][4].encode('utf-8').strip()
            }, ignore_index=True)

        except IndexError :
            None

result.to_csv('medocs.csv', index=False)