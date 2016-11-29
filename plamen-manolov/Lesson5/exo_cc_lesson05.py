import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
result = pd.DataFrame(columns=['Medicament', 'Dosage', 'Unite', 'Prescription'])

for page in range(1, 3):
    print ('page ' + str(page))
    r = requests.post(url, {
        "page": page,
        "affliste": 0,
        "affNumero": 0,
        "isAlphabet": 0,
        "inClauseSubst": 0,
        "nomSubstances": '',
        "typeRecherche": 0,
        "choixRecherche": 'medicament',
        "txtCaracteres": 'doliprane',
        "btnMedic.x": '12',
        "btnMedic.y": '5',
        "btnMedic": 'Rechercher',
        "radLibelle": 2,
        "txtCaracteresSub": '',
        "radLibelleSub": 4
    })
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.findAll('a', {'class': 'standart'})
    for a in links:
        text = a.get_text()
        tokens = re.findall(r'(.*)\s(\d{2,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)', text)
        print (tokens)
        if len(tokens) > 0 and len(tokens[0]) >= 3:
            print (tokens)
            result = result.append({
                'Medicament': (tokens[0][0] + ' ' + tokens[0][3]).strip(),
                'Dosage': int(tokens[0][1]),
                'Unite': tokens[0][2],
                'Prescription': tokens[0][4].strip()
            }, ignore_index=True)

print (result)
