
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

import requests
from bs4 import BeautifulSoup
import re
import json  # json.loads

# --------------------------------------ENONCE ---------------------------
# Organisame para-public ou pour un labo
# Récuperer pour l'ibuprophene - l'ensemble des formes médicamenteuses (marque, boite, forme galénique)
# levothyroxime, ibuprophene
# Base de données publiques des médicaments

adresse_page = u'http://base-donnees-publique.medicaments.gouv.fr/index.php'
medicament = "levothyrox"

liste_formes = []
liste_names = []
liste_labos = []
liste_grammages = []

fin = False
for page in range(1, 10):
    parametres = {'page': page, 'txtCaracteres': medicament,
                  'btnMedic': 'Rechercher', 'choixRecherche': 'medicament'}
    whole_page = requests.post(adresse_page, parametres)
    soup_page = BeautifulSoup(whole_page.text, 'html.parser')
    # Accroche correspondat aux lignes du tableau résultat de la recherche
    rows = soup_page('a', class_="standart")
    if rows != None:  # Il y a des lignes sur cette page
        # Récupération du nom de la molécule dans la liste, permet de gérer les cas des noms 
        # de médicament avec espaces (mais pas le cas où le critère de recherche est plus court que 
        # le nom du médicament        
        molecule = medicament+rows[0].text.strip()[len(medicament):].split(" ")[0]
        for row in rows:
            title = row.text.replace('\t', '')
            if title.lower().rfind(medicament.lower()) >= 0:  # On est bien sur une ligne correspondant à la molécule
                # Elimination du nom de la molécule dans la liste
                title = title[len(molecule) + 1:]
                # Récupération du dernier champ séparé par virgule correspond
                # au format
                forme_medoc = ""
                temp = title.split(",")
                if len(temp) >= 1:
                    forme_medoc = temp[len(temp) - 1]
                    title = temp[0]
                # Récupération du nom du laboratoire sensé précéder un grammage,
                # et en passant , récup du grammage
                labo = ""
                grammage = ""
                debut_grammage = re.search('[0-9]', title)
                if debut_grammage != None:
                    position_grammage = debut_grammage.span(0)[0]
                    labo = title[:position_grammage]
                    grammage = title[position_grammage:]
                # Stockage
                liste_labos.append(labo.strip())
                liste_grammages.append(grammage.strip())
                liste_formes.append(forme_medoc.strip())
                liste_names.append(molecule)
    else:
        fin = True
    if fin:
        break
Results = pd.DataFrame({'Molecule': liste_names, 'Labo': liste_labos,
                        'Dosage': liste_grammages, 'Format': liste_formes})
Results.to_excel("Catalogue_" + medicament + ".xls")
