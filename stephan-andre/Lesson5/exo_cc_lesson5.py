# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:25:49 2016

@author: Stephan
"""

import requests
from bs4 import BeautifulSoup
import re

def get_medicam(medicam):
    results = requests.post("http://base-donnees-publique.medicaments.gouv.fr/index.php", data = {'choixRecherche': 'medicament', 'txtCaracteres': medicam, 'action': 'show'})
    soup = BeautifulSoup(results.text, "lxml")
    names_medicam = soup.findAll('td', {'class':'ResultRowDeno'})
    liste_medicam = []
    for name in names_medicam:
        liste_medicam.append(name.text)
    return liste_medicam
 
ibupro = get_medicam('IBUPROFENE')   
#print(get_medicam('IBUPROFENE'))   
    
ibuprofene = []

for ibup in ibupro:
    temp = (re.findall(r'(.*)\s(\d{1,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)\s(\S*)', ibup))
    ibuprofene.append(temp)
    
for i in range(len(ibuprofene)):
    if ibuprofene[i] != []:
        print(ibuprofene[i][0][0] + ibuprofene[i][0][1] +' '+ ibuprofene[i][0][2] +' '+ ibuprofene[i][0][3])