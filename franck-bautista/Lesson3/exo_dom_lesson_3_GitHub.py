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

# Récupération des id de splus gros contributeurs
adresse_page = u'https://gist.github.com/paulmillr/2657075'
whole_page = requests.get(adresse_page)
soup_page = BeautifulSoup(whole_page.text, 'html.parser')
rows = soup_page.find_all(scope="row")
liste_contributeurs = []
for row in rows:
    contributeur = row.nextSibling.nextSibling.text
    liste_contributeurs.append(contributeur.split(" ")[0])

# liste_entrypoints =  requests.get('https://api.github.com')
# entrypoints = liste_entrypoints.json()
# 'https://api.github.com/users/{user}/repos{?type,page,per_page,sort}'
# https://api.github.com/?access_token=OAUTH-TOKEN}


# Collecte pour chaque contributeur des repositories dont il est propriétaire (type: owner)
# en passant le token en param pour contourner la limite du nombre max de connexion en anonymous (autour de 50)
# et calcul de sa note moyenne par cumul du nombre de repositories et de stars
file = open('token.txt', 'r')
token = file.readline()
file.close

param = {'access_token': token, 'type': 'owner'}
note_moyenne = {}
for user in liste_contributeurs:
    liste_repo = requests.get(
        'https://api.github.com/users/' + user + '/repos', params=param)
    liste = liste_repo.json()
    nb_repos = 0
    nb_stars = 0
    for repos in liste:
        nb_repos += 1
        nb_stars += repos['stargazers_count']
    if nb_repos != 0:
        note_moyenne[user] = nb_stars / nb_repos
    else:
        note_moyenne[user] = 0
    print(user + " : %i repositories / %i stars au total / %4.2f stars en moyenne" %
          (nb_repos, nb_stars, note_moyenne[user]))

# Sauvegarde résultats sous forme de fichier)
file = open('contrib.txt', 'w')
file.writelines(["%s %i\n" % (item, note_moyenne[item])
                 for item in sorted(note_moyenne, key=note_moyenne.get, reverse=True)])
file.close()
