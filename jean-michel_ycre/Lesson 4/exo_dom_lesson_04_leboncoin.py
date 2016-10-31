# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""

import sys, os, csv, json, xlrd, openpyxl, requests, pytz, re
import bs4
import pandas as pd
import numpy as np
from numbers import Number


# URL EXO ARGUS

url_zoe_annee = "http://www.lacentrale.fr/cote-voitures-renault-zoe--2015-.html"
url_modele_argus = "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2013.html"

url_modele_1 = "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2014.html"
url_modele_2 = "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide+type+2-2014.html"
url_modele_3 = "http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide-2014.html"
url_modele_4 = "http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide+type+2-2014.html"
url_modele_5 = "http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide-2014.html"
url_modele_6 = "http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide+type+2-2014.html"

url_cote_affinée = "http://www.lacentrale.fr/cote_proxy.php?km=80000&month=09"

url_LBC_zoe_IDF = "https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&q=renault%20zo%E9&parrot=0"
ulr_annonce = "https://www.leboncoin.fr/voitures/1037533687.htm?ca=12_s"

url_LBC_zoe_IDF = "https://www.leboncoin.fr/voitures/offres/aquitaine/?th=1&q=renault%20zo%E9&parrot=0"

url_LBC_zoe_IDF = "https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?th=1&q=renault%20zoe&parrot=0"

# Obtention des données de la page web à traiter
# ------------------------------------------------------
def getsoup(region, constr, mod):
    url = "https://www.leboncoin.fr/voitures/offres/"+region+"/?th=1&q="+constr+"%20"+mod+"&parrot=0"
    pageweb = requests.get(url)
    soup = bs4.BeautifulSoup(pageweb.text, 'html.parser')
    return soup


def get_voiture(url):
    pageweb = requests.get(url)
    soup = bs4.BeautifulSoup(pageweb.text, 'html.parser')
    return soup


def get_centrale(marque, modele, version_LC, annee, kilomt):
    url_basic = r"http://www.lacentrale.fr/cote-auto-"+marque+r"-"+modele+r"-"+version_LC+r"-"+annee+r".html"
#    url_affine = r"http://www.lacentrale.fr/cote_proxy.php?km="+kilomt+r"&month=06"
#    print(url_basic)
    pageweb1 = requests.get(url_basic)
#    pageweb2 = requests.get(url_affine)
    soup = bs4.BeautifulSoup(pageweb1.text, 'html.parser')
    return soup


def as_percent(v, precision='0.2'):
    """Convert number to percentage string."""
    if isinstance(v, Number):
        return "{{:{}%}}".format(precision).format(v)
    else:
        raise TypeError("Numeric type required")


# Programme principal

# Paramètres de recherche
regions = ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']
marque = ['renault']
modele = ['zoe']


# Initialisation du dataframe résultats

index_pd = ['Marque', 'Modèle', 'Version', 'Année', 'Kilométrage', 'Prix vente', 'Téléphone', 'Type vendeur', 'url', 'Prix Argus', 'Ecart Argus']

liste_annonces = pd.DataFrame(np.zeros(11000).reshape(1000, 11), columns=index_pd)
liste_annonces.drop(liste_annonces.index[[0,1]])
liste_annonces.reset_index()


# Obtention des données
# --------------------------
# récupération des annonces
# intégration dans le dataframe du type de véhicule, du vendeur et de l'url

n_line = 0
for region in regions:
    testLBC = getsoup(region,marque[0], modele[0])
    css_soup = testLBC.find_all('a')

    for i in range(len(css_soup)):
        try:
           if css_soup[i]['class'] == ['list_item', 'clearfix', 'trackable']:
                liste_annonces.ix[i+n_line, 2] = css_soup[i]['title']
                liste_annonces.ix[i+n_line, 8] = css_soup[i]['href']
                liste_annonces.ix[i+n_line, 7] = eval(css_soup[i]['data-info'])["ad_offres"]
        except:
            pass

    n_line += len(css_soup)

#---------------------------------------------------------------------------------------
# suppression des lignes inutilisées du dataframe et renumérotation

liste_annonces = liste_annonces.drop_duplicates()
liste_annonces = liste_annonces.ix[1:,:]
liste_annonces.index = np.arange(0, len(liste_annonces.index))

# ------------------------------------------------
# pour chaque annonce, récupération de l'annonce détaillée :
# pour avoir : l'année de mise en service, le prix, le kilométrage

for i in range(len(liste_annonces)):

    x = get_voiture('http:' + liste_annonces.ix[i, 8])

    #y = x.find("p", itemprop="description").next
    liste_annonces.ix[i, 3] = x.find("span", itemprop="releaseDate").next.replace("\n", "").rstrip().lstrip()

    petite_soup = x.find_all("span", attrs={'class':'value'})

    liste_annonces.ix[i,5] = int(petite_soup[0].next.replace(r"\n", "")
    .replace("€", "").rstrip().lstrip().replace(' ', ''))


    for j in range(len(petite_soup)):
        if petite_soup[j].get_text().endswith('KM'):
            liste_annonces.ix[i, 4] = int(petite_soup[j].get_text()
            .replace('KM', '').rstrip().lstrip().replace(' ', ''))

#-----------------------------------------------------------------------------

# Nettoyage des données (colonnes marque, modèle, version)

liste_annonces['Marque'] = 'Renault'
liste_annonces['Modèle'] = 'Zoé'
liste_annonces['Version'] = liste_annonces['Version'].str.lstrip('Renault')
liste_annonces['Version'] = liste_annonces['Version'].str.replace('é', 'e')
liste_annonces['Version'] = liste_annonces['Version'].str.lower()
liste_annonces['Version'] = liste_annonces['Version'].str.lstrip('zoe')

myset = {'z.e.', 'zen', 'charge', 'rapide', 'intens', 'type 2', 'life'}

for i in range(len(liste_annonces)):
   list_i = liste_annonces.ix[i, 2].split(' ')
   nom_voiture = [x for x in list_i if x in myset]
   model = ' '.join(nom_voiture)
   if model == '':
       model = 'Modèle inconnu'
   liste_annonces.ix[i, 2] = model

#-----------------------------------------------------------------------------

# Récupération si possible de la cote Argus
# Sinon, prix Argus = prix de vente


for i in range(len(liste_annonces)):
    if liste_annonces.ix[i, 2] != 'Modèle inconnu':
       version_LC = liste_annonces.ix[i, 2].replace(' ',  '+')
       annee = str(liste_annonces.ix[i, 3])
       kilomt = str(liste_annonces.ix[i, 4])
       if version_LC != '':
           z = get_centrale(marque[0], modele[0], version_LC, annee, kilomt)
           try:
               d = int(z.find("strong", attrs={'class':'f24 bGrey9L txtRed pL15 mL15'}
                              ).text.replace("\n", "").replace(' ', '').replace("€", ""))
           except:
               d = liste_annonces.ix[i, 5]
       else:
          liste_annonces.ix[i, 9] = liste_annonces.ix[i, 5]
       if  d != 0:
           liste_annonces.ix[i, 9] = int(d)
       else:
           liste_annonces.ix[i, 9] = liste_annonces.ix[i, 5]
    else:
        liste_annonces.ix[i, 9] = liste_annonces.ix[i, 5]


#---------------------------------------------------------------------------------------

# Calcul écart de prix Argus vs. prix de vente
# Tri sur l'écart, formatage et affichage


liste_annonces['Ecart Argus'] = (liste_annonces['Prix vente'] - liste_annonces['Prix Argus'])/liste_annonces['Prix Argus']

liste_annonces = liste_annonces.sort_values('Ecart Argus')
liste_annonces['Ecart Argus'] = liste_annonces['Ecart Argus'].apply(as_percent)

print(liste_annonces)
