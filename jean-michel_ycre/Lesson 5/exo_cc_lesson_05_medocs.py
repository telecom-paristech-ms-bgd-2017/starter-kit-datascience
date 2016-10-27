# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""

import sys, os, csv, json, xlrd, openpyxl, requests, pytz
import re
import bs4
import pandas as pd

# Obtention des données via l'API de google maps
# ------------------------------------------------------
def get_medoc(molecule):
    """
    API sur googlemaps :
    """
    url_api = "https://medicaments.api.gouv.fr/api/medicaments?nom="+molecule
    print(url_api)
    reponse = requests.get(url_api).json()
    medoc_molecule = []
    for dico in reponse:
        if dico.get('composition'):
            mon_medoc = {}
            try:
                mon_medoc['formePharmaceutique'] = dico['formePharmaceutique']
                print("0")
            except Exception:
                print("KO0")
                pass
            try:
                mon_medoc['nom'] = dico['nom']
                print("1")
            except Exception:
                print("KO1")
                pass
            try:
                mon_medoc['titulaire'] = dico['titulaire'][0]
                print("3")
            except Exception:
                print("KO3")
                pass
            try:
                mon_medoc['etatCommercialisation'] = dico['composition'][0]['etatCommercialisation']
                print("4")
            except Exception:
                print("KO4")
                pass
            try:
                mon_medoc['libelle'] = dico['presentation'][0]['libelle']
                print("5")
            except Exception:
                print("KO5")
                pass
            print(mon_medoc)
            medoc_molecule.append(mon_medoc)

    medocs = pd.DataFrame(medoc_molecule,
                          columns=['nom', 'etatCommercialisation',
                                   'formePharmaceutique',
                                   'libelle', 'titulaire'])

    medocs.columns = ['Nom', 'Dosage', 'Forme pharmaceutique',
                      'Libellé', 'Marque']

    return medocs



# Programme principal

liste_molecules = ["ibuprofene", "LEVOTHYROXINE", "Diosmectite"]

# on ne conserve qu'une racine du nom de la molécule pour obtenir le maximum de résultats

liste_recherche = ["ibu", "LEVOTHYR", "smect"]

for k in range(len(liste_recherche)):
    reponse = get_medoc(liste_recherche[k])
    print(reponse)
    reponse.to_csv(liste_molecules[k]+".csv", sep=",", header=True)
