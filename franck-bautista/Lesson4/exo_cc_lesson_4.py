
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from numpy.linalg import svd
from scipy.stats import beta

import requests
from bs4 import BeautifulSoup
import re
import json  # json.loads
# Calcul de couts - Distance en kms et temps ville à ville sur les 3à plus
# grandes villes de France



# Récupération des villes les plus peuplées
adresse_page = u'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es'
whole_page = requests.get(adresse_page)
soup_page = BeautifulSoup(whole_page.text, 'html.parser')

rows = soup_page.find_all('b')
liste_villes = []
nb_max = 30
compteur = 0
for row in rows:
    ville = row.text.split(r"\s+")[0]
    # seules les villes commenencent par une majuscule
    if ville[0].isalpha() & ville[0][0].isupper():
        compteur += 1
        liste_villes.append(ville)
    if compteur >= nb_max:
        break
tableau_villes = pd.DataFrame({'EnCours': ['test'] * 30}, index=liste_villes)

Cle2 = 'AIzaSyAsLOAM_BabOHO6xP8BOKkBqSJX6Ft7Obg'
Cle2 = 'AIzaSyDUIjonWQd83W4AHqpsvFp9aJIOELooYLI'
# https://maps.googleapis.com/maps/api/distancematrix/output?parameters
matrice_distances = []
for ville_depart in liste_villes:
    dests = ""
    list_distances = []
    for ville_arrivee in liste_villes:
        dests = dests + ville_arrivee + "|"
    param = {'origins': ville_depart, 'destinations': dests, 'key': Cle2}
    dist = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json', params=param)
    dist_dec = dist.json()
    compteur_ville = 0
    for ville_arrivee in liste_villes:
        dist_txt = dist_dec['rows'][0]['elements'][
            compteur_ville]['distance']['text']
        tableau_villes.iat[compteur_ville, 0] = dist_txt
        compteur_ville += 1
    print(tableau_villes.EnCours)
    tableau_villes[ville_depart] = tableau_villes.EnCours
del tableau_villes['EnCours']    
tableau_villes.to_excel('Distance_villes.xls')
