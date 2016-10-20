
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

import requests
from bs4 import BeautifulSoup
import re
import json  # json.loads

# --------------------------------------ENONCE ---------------------------
# L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion
# en Ile de France, PACA et Aquitaine.
# Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes :
# version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
# Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous
# récupérez sur ce site
# http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

# Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
# Vous ajouterez une colonne si la voiture est plus chere ou moins chere
# que sa cote moyenne.﻿

# ----------------------------------- APPROCHE --------------------------
# 1) Récupération des numéros d'annonce ou adresses de pages web à aller chercher
# https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&q=zoe&parrot=0
# https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?th=1&q=zoe&parrot=0
# https://www.leboncoin.fr/voitures/offres/aquitaine/?th=1&q=zoe&parrot=0

# 2) Récupération des infos plus détaillées par annonce, sur des pages de type
# https://www.leboncoin.fr/voitures/1035061272.htm?ca=12_s

# 3) Récupération des infos sur la Centrale en deux temps... une première
# requête donnant les différents modèles diponibles, sélection de la
# première ligne présentée pour ouvrir page et collecter cote


# Récupération des annonces - 3 requêtes correspondant aux 3 régions demandées
liste_regions = {'IDF': 'ile_de_france',
                 'PACA': 'provence_alpes_cote_d_azur', 'AQU': 'aquitaine'}
modele = 'zoe'
marque = 'Renault'# majuscule puis minuscule
versions = ['Zen','Intens','Life']

# modele = 'Q5'
# marque = 'Audi'# majuscule puis minuscule
# versions = ['Sline','quattro','Luxe']




liste_annonces = []
liste_region_annonces = []
liste_type_vendeur = []

param1 = {'th':1,'parrot':0,'brd':marque,'q':modele.lower()}
for region in liste_regions:
    # adresse_page = u'https://www.leboncoin.fr/voitures/offres/' + \
    #     liste_regions[region] + '/?th=1&parrot=0&fu=4&brd=' + marque + '&q=' + modele.lower()
    # whole_page = requests.get(adresse_page)
    adresse_page = u'https://www.leboncoin.fr/voitures/offres/' + liste_regions[region]
    whole_page = requests.get(adresse_page, params=param1)
    soup_page = BeautifulSoup(whole_page.text, 'html.parser')
    rows = soup_page.find_all(class_="list_item clearfix trackable")

    for row in rows:
        info_glob = row.unwrap()
        liste_annonces.append(info_glob['href'])
        liste_region_annonces.append(region)
        # Récup type vendeur
        data_info = info_glob['data-info']
        pos_info = data_info.rfind('ad_offres')
        type_vendeur = ""
        if (pos_info > 0):
            type_vendeur = data_info[pos_info +
                                     14:pos_info + 18].replace('"', '')
        liste_type_vendeur.append(type_vendeur)

df = pd.DataFrame({'Region': liste_region_annonces, 'Site': liste_annonces, 'Type_Vendeur': liste_type_vendeur,
                   'prix': 0, 'annee': 0, 'kms': 0, 'marque': "", 'version': "", 'tel': "", 'Argus': 0})

num_tel = re.compile(
    "(\+33|0)(\s||0|\-)[0-9](\.|\s||)([0-9]{2}(\.|\s||\-)){3}[0-9]{2}")
for row in range(0, df.count()[0]):
    adresse_page = "https:" + df['Site'].ix[row]
    whole_page = requests.get(adresse_page)
    soup_page = BeautifulSoup(whole_page.text, 'html.parser')
    temp = soup_page.find(class_="item_price clearfix").find(class_="value")
    if temp != None:
        df['prix'].ix[row] = int(re.sub("[^0-9]", "", temp.text))
    temp = soup_page.find(class_="value", itemprop="brand")
    if temp != None:
        df['marque'].ix[row] = temp.text
    temp = soup_page.find(class_="value", itemprop="releaseDate")
    if temp != None:
        df['annee'].ix[row] = int(re.sub("[^0-9]", "", temp.text))
    temp = soup_page.find(
        class_="value", itemprop="releaseDate").parent.parent.nextSibling.nextSibling.find(class_="value")
    if temp != None:
        df['kms'].ix[row] = int(re.sub("[^0-9]", "", temp.text))
    
    temp = soup_page.find(class_="adview_header clearfix").find(
        class_="no-border")
    temp_version = re.sub("[^A-Za-z]", "", temp.text).upper()
    version = ""
    for version_testee in versions:
        if re.search(version_testee.upper(), temp_version):
            version = version_testee        
    df['version'].ix[row] = version

    # Chercher numéro de téléphone dans annonce...
    description = soup_page.find(class_="value", itemprop="description").text
    tel_description = re.search(num_tel, description)
    if tel_description != None:
        num_tel_brut = tel_description.string[
            tel_description.span()[0]:tel_description.span()[1]]
        num_tel_propre = re.sub('([^0-9+])', '', num_tel_brut)
        df['tel'].ix[row] = num_tel_propre

# df.to_excel("Annonces " + modele + ".xls")
# df = pd.read_excel("Annonces " + modele + ".xls")

# Collecte infos La Centrale
# http://www.lacentrale.fr/cote-voitures-renault-zoe--2015-.html
# http://www.lacentrale.fr/cote-auto-renault-zoe-intens-2015.html
df1 = df.dropna(subset=['version']).reset_index()
for row in range(0, df1.count()[0]):
    if df1.version.ix[row] != "":
        adresse_page = 'http://www.lacentrale.fr/cote-voitures-' + \
            df1.marque.ix[row].lower() + '-' + modele + '-' + df1.version.ix[row].lower() + \
            '-' + str(df1.annee.ix[row]) + '-.html'
        whole_page = requests.get(adresse_page)
        soup_page = BeautifulSoup(whole_page.text, 'html.parser')
        premiere_ligne = soup_page.find(class_="listingResultLine f14 auto")
        if premiere_ligne != None:
            adresse_page = 'http://www.lacentrale.fr/' + premiere_ligne.findChild()['href']
            whole_page = requests.get(adresse_page)
            soup_page = BeautifulSoup(whole_page.text, 'html.parser')
            temp = soup_page.find(class_="f24 bGrey9L txtRed pL15 mL15")
            if temp != None:
                cote = int(re.sub('[^0-9]', "", temp.text))
                df1.Argus.ix[row] = cote

df1.to_excel("Annonces " + modele + ".xls")
