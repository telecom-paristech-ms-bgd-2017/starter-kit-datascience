# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:40:01 2016

@author: Antoine
"""

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

pages = [1]
medicaments = ["ibuprofene"] #levothyroxime
search_url = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
for medoc in medicaments:
    for p in pages:
        # Pour voir la requete aller dans inspecter onglet network
        # Pour cet exercice, il faut faire une requete post
        params_post = {"page": p,
                       "affliste": 0,
                       "affNumero": 0,
                       "isAlphabet": 0,
                       "inClauseSubst": 0,
                       "nomSubstances": "",
                       "typeRecherche": 0,
                       "choixRecherche": "medicament",
                       "paginationUsed": 0,
                       "txtCaracteres": medoc,
                       "btnMedic.x": 15,
                       "btnMedic.y": 9,
                       "btnMedic": "Rechercher",
                       "radLibelle": 2,
                       "txtCaracteresSub": "",
                       "radLibelleSub": 4}
        req = requests.post(search_url, data=params_post)
        soup = BeautifulSoup(req.text, 'html.parser')
        raw_res = list(soup.find_all(class_="standart"))
        pattern = medoc.upper() + '\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+), ([\w\sé])'
        regex = re.compile(pattern)
        all_medocs = list(map(lambda l: regex.findall(l.string), raw_res[:-3]))
    
    # pb de regex ???
    medicament_df = pd.Series(all_medocs).str.extract('\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+), ([\w\sé])', expand=True)

print(medicament_df) # 
