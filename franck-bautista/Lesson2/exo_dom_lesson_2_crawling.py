# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 16:41:10 2016

@author: Franck
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd

"""	
	num_commune et num_dep sous forme de str de 3 caractères, renvoye un tableau de 8 colonnes
"""


def lire_data(num_dep, num_commune, annee):

    adresse_page = u'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' + num_commune + '&dep=' + num_dep + '&type=BPS&param=5&exercice=' + \
        str(annee)
    whole_page = requests.get(adresse_page)
    soup_page = BeautifulSoup(whole_page.text, 'html.parser')

    list_lignes = soup_page.find_all(class_='montantpetit G')
    list_lignes = soup_page.find_all(class_='libellepetit G')

    lecture = np.zeros(8)
    for ligne in list_lignes:
        shortlib = ligne.text[-3:]
        # selection des lignes avec données à collecter
        if shortlib in ('= A', '= B', '= C', '= D'):
            if shortlib == '= A':  # Détermination du type de ligne collectée
                i = 0
            elif shortlib == '= B':
                i = 1
            elif shortlib == '= C':
                i = 2
            else:
                i = 3
                # Collecte des infos des 2 colonnes précédant le tag sur lequel
                # on s'est appuyé
            temptxt1 = re.sub(
                r'([^0-9])', '', str(ligne.previousSibling.previousSibling.previousSibling.previousSibling))
            temptxt2 = re.sub(
                r'([^0-9])', '', str(ligne.previousSibling.previousSibling))
            # Stockage des données dans un array 1x8
            lecture[i] = int(temptxt1)
            lecture[i + 4] = int(temptxt2)
    return lecture

"""
Lecture du fichier des communes qui indiquent les communes à cibler
"""


def liste_communes(filename):
    df = pd.read_csv('exo_dom_lesson_2_crawling_Liste_Communes.csv', sep=None)
    return df


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Debut du programme principal, génération d'un DF
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Définition du périmètre de la collecte (fichier des communes + annnées)
filename = 'Liste_Communes.csv'  # Champ GETDATA à 1... initialisé sur PARIS et 92
annee_deb = 2011
annee_fin = 2015

# Initialsiation
# Structure du DataFrame qui stockera les résultats
list_champs = ['Ville', 'Annee', 'A1', 'B1',
               'C1', 'D1', 'A2', 'B2', 'C2', 'D2']
# Creation du df de restitution
df_tot = pd.DataFrame(columns=list_champs, dtype=int)
# Récupération de la liste des communes
toutes_communes = liste_communes(filename)
communes = toutes_communes[toutes_communes.GETDATA == 1]
nbvilles=communes.REG.count() 
print("%s  villes" %nbvilles + " à crawler sur %s annees" %(annee_fin - annee_deb + 1))

# Boucle sur les villes à cibler
for index, commune in communes.iterrows():
    # reformatage des codes commune et département
    nom_ville = str(commune.NCC)
    num_commune = commune.COM
    if num_commune < 10:
        code_ville = "00%s" % num_commune
    elif num_commune < 100:
        code_ville = "0%s" % num_commune
    else:
        code_ville = "%s" % num_commune

    num_dep = commune.DEP
    if len(num_dep) < 2:
        code_dep = "00" + num_dep
    elif len(num_dep) < 3:
        code_dep = "0" + num_dep
    else:
        code_dep = "" + num_dep

    # Boucle sur les années
    for annee in range(annee_deb, annee_fin + 1):
        lecture1 = lire_data(code_dep, code_ville, annee)
        list_data = [nom_ville, int(annee)]
        list_data.extend(lecture1)
        df = pd.DataFrame(columns=list_champs, data=[list_data])
        print(nom_ville, annee, lecture1[0])
        df_tot = df_tot.append(df)

# Sauvegarde du résultat dans le fichier
df_tot.to_csv("exo_dom_lesson_2_crawling_Depenses_Villes.csv")
