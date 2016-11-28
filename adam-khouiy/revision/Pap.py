import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from multiprocessing import Pool
from functools import partial
import time
import numpy as np

numProcesses = 4 # my number of cores
run_type = 'Parallel'

requestURL = 'http://www.pap.fr/argent/calculettes/frais-de-notaire#calculette-results'


def BuilParam(rdv_signature,montant,app,code_postal,ville):
    paramPap = {
        'rdv_signature':rdv_signature,
        'date_signature':'',
        'montant':montant,
        'typebien':app,
        'adresse':'',
        'mappy_adresse_complete':'',
        'mappy_adresse':'',
        'mappy_code_postal':'',
        'mappy_ville':'',
        'mappy_lat':'',
        'mappy_lng':'',
        'code_postal': code_postal,
        'ville':ville,
        'nb_pieces':'',
        'surface':'',
        'surface_terrain':'',
        'viabilise':'',
        'vendeur_terrain':'',
        'nb_lots':'',
        'frais_de_notaire_submit':1

    }
    return paramPap


def processPage(rdv_signature, montant, app, code_postal, ville):
    paramPap = BuilParam(rdv_signature,montant,app,code_postal,ville)
    requestResponse = requests.post(requestURL, paramPap).text
    soup = BeautifulSoup(requestResponse, 'html.parser')
    prix = soup.findAll(class_='tr-green-highlight')

    for iter in prix:
        prix1 = iter.findAll('td')
        prix1_F =prix1[1].text.replace('€','').replace('.','')
        return prix1_F




if __name__ == '__main__':

     dictionnaire = {'ville' : ['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Strasbourg','Montpellier','Bordeaux','Lille','Rennes','Reims','Le Havre','Saint-Étienne','Toulon','Grenoble','Dijon','Angers','Villeurbanne','Nîmes'] ,'Arrondissement' : ['75013','13001','69001','31100','06100','44100','67100','34070','34080','33100','59160','35200','51100','76610','42100','83100','21000','49100','69100','30900']}
     df = pd.DataFrame(dictionnaire)

     #processPage('non', '1000000', 'appartement', "75013", "Paris")
     processPage('non', '500000', 'appartement', '13001', 'Marseille')
     for ville, arrondissement in zip(df['ville'], df['Arrondissement']):
        #print(ville + arrondissement)
        notaire = processPage('non', '500000', 'appartement', arrondissement, ville)
        print(notaire)


     #print(df)

     #print (len (['75013','13000','69001','31100','06100','44100','67100','34070','34080','33100','59160','35200','51100','76610','42100','83100','21000','49100','69100','30900','']))
     #list_prix = []
     #for ville, arrondissement in zip(df['ville'], df['Arrondissement']):
     #     prix_return = processPage('non', '1000000', 'appartement', arrondissement, ville)
      #    list_prix.append(prix_return)


     #print (list_prix)


