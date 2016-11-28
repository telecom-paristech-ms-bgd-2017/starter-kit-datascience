import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re


# Sortir l'inventaire des formes de Ibuprofène et Levothyroxine depuis la base publique des médicaments

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#resarch=ibuprofene'

results = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php',\
                        data={'choixRecherche':'medicament', 'txtCaracteres':'ibuprofene'})

soup = BeautifulSoup(results.text, 'html.parser')
stri = 'IBUPROFENE ALMUS 200 mg, comprimé pelliculé'
strid = re.search('IBUPROFENE\s([\w\s]+)\s(\d+)\s?(%|mg),\s?([\w\s])', stri)
print(strid)
#medoc = soup.find(class_="ResultRowDeno").text.extract('IBUPROFENE\s([\w\s]+)\s(\d+)\s?(%|mg),\s?([\w\s])')
#print(medoc)

r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php#result',\
                  data = {'choixRecherche':'medicament', 'txtCaracteres':'ibuprofene'})
r.encoding

soup = BeautifulSoup(r.text, 'html.parser')
# Récup liste des médocs contenant ibuprofène dans le titre

soup.find_all("a", class_="standart")[:3]

soup.find_all("a", "standart")[:3]

soup.find("a", class_="standart")

result = soup.find_all("a", "standart")
for tagou in result:
    print(tagou)

# Extraire le string du tag cherché
soup.find("a", class_="standart").text

# Changement d'encodage pour voir si ça arrange quelque chose (mais non)
r.encoding = 'UTF-8'
soup = BeautifulSoup(r.text, 'html.parser')
soup.find_all("a", class_="standart")[:3]

soup.find_all("a", class_="standart").text

for tagou in result:
    print(soup.find("a", class_="standart").text)

# Maintenant, on va parcourir les plusieurs pages de résultats
r = []
for i in range(3):
    res = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php#result',\
                    data = {'choixRecherche':'medicament', 'txtCaracteres':'ibuprofene', 'page':i})
    soup = BeautifulSoup(res.text, 'html.parser')
    tab = soup.find_all("a", class_="standart", string=re.compile('IBUPRO'))
    for t in range (len(tab)):
        r.append(tab[t].text)
r

# Création du bon dataframe qui répond à toutes les questions
pat = '([A-Z\s+-]+)\s?([0-9]+)\s?(mg|%)\/?(ml)?,?\s?([A-Z\s+-]+)'
df = pd.Series(r).str.upper().str.extract(pat, flags=re.IGNORECASE)
df = df.rename(columns = {0:'Nom Médicament', 1:'quantité', 2:'unité_1',3:'unité_2',4:'type'} )
df.index = df.index.map(lambda x: 'Médicament ' +str(x))
df
