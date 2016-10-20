# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""
import sys, os, csv, json, xlrd, openpyxl, requests, pytz
import bs4
import pandas as pd
import numpy as np

# Obtention des données de la page web à traiter
# ------------------------------------------------------
def getsoup():
    url_wikipedia = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"
    pageweb = requests.get(url_wikipedia)
    soup = bs4.BeautifulSoup(pageweb.text, 'html.parser')
    return soup

# ---------------------------------------------------
# URL exemple API de google maps api distance matrix

#https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key=YOUR_API_KEY
# ---------------------------------------------------


# Obtention des données via l'API de google maps
# ------------------------------------------------------
def get_distance(ville1, ville2):
    """
    API sur googlemaps :
    """
#    user_git = 'JeanMiMi'
    key_api = open(r'C:/Users/Justyna/Documents/1-CT-doc/bigdata/googlemaps_key.txt').read()
    url_api_google = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+ville1+"&destinations="+ville2+'&key='+key_api
    reponse = requests.get(url_api_google).json()
    distance = reponse['rows'][0]['elements'][0]['distance']['value']

    return distance


# Programme principal

# Obtention des données
soup = getsoup()

# Extraction et nettoyage de la liste des villes
liste = []
liste_villes = soup.table.find_all('tr')
i = 0
for ville in liste_villes:
    ma_ville = ville.find('a').text
    liste.append(ma_ville)
    i += 1
    if i == 31:
        break
liste = liste[1:]
print(liste)

# Création de la matrice ville-ville
tableau = pd.DataFrame(index=liste, columns=liste)

# remplissage de la matrice par la fonction get-distance basée sur l'API de google
for ville1 in liste:
    for ville2 in liste:
        tableau.set_value(ville1, ville2, get_distance(ville1, ville2))

# Impression de la matrice
print(tableau)

# Sauvegarde du classement
tableau.to_csv("distances_France.csv", sep=",", header=True)

# un peu d'analyse sur les données
tableau_eloignement = tableau.sum(axis=0)
tableau_eloignement.sort_values(inplace=True)
print(tableau_eloignement)
print("Lyon est la ville la plus proche des autres grandes villes.")
print("Brest est la ville la plus éloignée des autres grandes villes.")



