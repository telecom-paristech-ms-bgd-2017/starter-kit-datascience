# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 13:40:56 2016

@author: arthurouaknine
"""

# base de données des médicaments
# Ibuprofene / Levothyroxine

import requests
from bs4 import BeautifulSoup

r = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php', data={'nomSubstances':"", 'choixRecherche' :"medicament", 'txtCaracteres' :"ibuprofene", 'txtCaracteresSub':""})
soup = BeautifulSoup(r.text, 'html.parser')
tableau = soup.find_all(class_='result')[0].a
line = tableau.text.replace('\xa0','').strip()

# IBUPROFENE\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+), ([\w\sé])
# A compléter pour avoir toute la ligne d'un coup