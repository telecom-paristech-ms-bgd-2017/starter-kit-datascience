import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

#URL = 'http://base-donnees-publique.medicaments.gouv.fr/'
URL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
regex = re.compile('^IBUPROFENE[A-Z][A-Z]|\[0-9][m,g]\,[a-z] [a-z]')
p = re.compile("(IBUPROFENE)\s+([A-Z]+)")
p1 = re.compile("[^\s]+[0-9]{2,3}\s(mg)")
p2 = re.compile(",\s(.)+")
data = pd.DataFrame(columns = ["Nom pharmaceutique", "Dosage", "Forme"])
parametre = {'page':'1',
'affliste':'0',
'affNumero':'0',
'isAlphabet':'0',
'inClauseSubst':'0',
'nomSubstances':'',
'typeRecherche':'0',
'choixRecherche':'medicament',
'paginationUsed':'0',
'txtCaracteres':'ibup',
'btnMedic.x':'0',
'btnMedic.y':'0',
'btnMedic':'Rechercher',
'radLibelle':'2',
'txtCaracteresSub':'',
'radLibelleSub':'4'} 
r = requests.post(URL,data = parametre)
r2 = BeautifulSoup(r.text, 'html.parser')
medocs = r2.find_all(class_="standart")
for elt in medocs:
    if p.search(elt.text.strip()):
        try:
            molecule = p.search(elt.text.strip()).group().split(" ")[1]
            dosage = p1.search(elt.text.strip()).group().replace("mg","")
            forme = p2.search(elt.text.strip()).group().replace(",","")
        except Exception as e: 
            molecule = ""
            dosage = ""
            forme = ""
    data = data.append({"Nom pharmaceutique":molecule, "Dosage":dosage, "Forme":forme}, ignore_index = True)

data.to_csv('Donnees_Ibuprofene'+'.csv')
