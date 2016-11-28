# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:40:56 2016

@author: arthurouaknine
"""

# base de données des médicaments
# Ibuprofene / Levothyroxine

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

nombrePages = 3
dataMedoc = []

for p in range(1, nombrePages+1):
    r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php',
                      data={'nomSubstances': "",
                            'choixRecherche': "medicament",
                            'txtCaracteres': "ibuprofene",
                            'txtCaracteresSub': "",
                            'page': "1"})

    soup = BeautifulSoup(r.text, 'html.parser')
    tableau = soup.find_all(class_='result')
    for line in tableau:
        for data in line.find_all(class_='standart'):
            dataMedoc.append(data.text.replace('</a>', '').strip().split(","))
print(dataMedoc)

dataInForm = []
for element in dataMedoc:
    oneLine = []
    oneLine.append(element[0].split(" ")[0] + " " + element[0].split(" ")[1])
    if re.search(r'(\d{1,4})(\s+mg?|%)', element[0]):
        oneLine.append(re.search(r'(\d{1,4})(\s+mg|%)', element[0]).group(1)
                                                                   .strip())
        oneLine.append(re.search(r'(\d{1,4})(\s+mg|%)', element[0]).group(2)
                                                                   .strip())
    else:
        oneLine.append('')
        oneLine.append('')
    oneLine.append(element[1].strip())
    dataInForm.append(oneLine)

df = pd.DataFrame(dataInForm)
df.columns = [['Name', 'Quantity', 'Mesure', 'Type']]

df.to_csv("/Users/arthurouaknine/Dropbox/Fac/MS/P1/Kit Data Sciences/Semaine 5/medicaments.csv")
print(df)
