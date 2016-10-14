# -*- coding: utf-8 -*-

import requests
import bs4
import os
import pandas as pd
import json
import numpy as np

# Ce fichier contient les 264 plus grandes villes de France (copié collé depuis un site internet)
file = "villes.csv"
villes = pd.read_csv(file, sep = ";")[["Classement", "Ville"]]

# Clé API Google Maps
key = open('key.txt').read()

# Combien de villes considérer ?
top = 30

# Initialisation des vecteurs qui contiendront les réponses
reskm = []
resduration = []

for i in range(0,top):
    for j in range(0, top):
        if(i != j): # La diagonale des matrices résultat contiendra des 0

            # Récupération des deux villes à considérer

            villegauche = villes["Ville"][i] # + "+France"
            villedroite = villes["Ville"][j] # + "+France"

            print villegauche, villedroite

            # Construction de l'URL et parsing json
            URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+villegauche+"&destinations="+villedroite+"&key="+key
            villes_json = json.loads(requests.get(URL).text)

            # Récupération de la distance en float
            km = float(villes_json["rows"][0]["elements"][0]["distance"]["text"].replace(" km","").replace(",","."))

            # Récupération du temps de trajet en float - si la durée est inférieure à 1h, il n'y a que les minutes
            duration = villes_json["rows"][0]["elements"][0]["duration"]["text"].replace(",",".").split(" ")
            print duration
            if(len(duration) == 2):
                duration_h = 0
                duration_m = float(duration[0])
            if(len(duration) == 4):
                duration_h = float(duration[0])
                duration_m = float(duration[2])

            reskm.append(km)
            resduration.append(duration_h*60+duration_m)
        else: # Cas ou i = j
            reskm.append(0)
            resduration.append(0)

# Insertion des données dans des matrices
reskm_mat = pd.DataFrame(np.reshape(np.matrix(reskm), (top, top)))
resduration_mat = pd.DataFrame(np.reshape(np.matrix(resduration), (top, top)))

# Nommage des colonnes
reskm_mat.columns = villes["Ville"][0:top]
resduration_mat.columns = villes["Ville"][0:top]

# Nommage des lignes
reskm_mat.index = villes["Ville"][0:top]
resduration_mat.columns = villes["Ville"][0:top]

# Ecriture en csv
reskm_mat.to_csv("Distance matrix.csv", sep=";", header = True)
resduration_mat.to_csv("Duration matrix.csv", sep=";", header = True)

