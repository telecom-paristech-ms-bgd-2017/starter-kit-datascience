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
    url = "https://gist.github.com/paulmillr/2657075"
    pageweb = requests.get(url)
    soup = bs4.BeautifulSoup(pageweb.text, 'html.parser')
    return soup


# API sur Github :obtention des 30 premiers repos
# ------------------------------------------------------

def get_user_stats(user):
    """
    API sur Github :
    1) Obtention des 30 premiers repos pour le user GitHub
    2) Obtention pour chaque repo du nombre de stargazers
    3) Calcul du nombre de repos
    4) Calcul de la somme et de la moyenne de stargazers du user
    5) Renvoie :
        - la liste des repos et les nombres respectifs de stargazers,
        - le nb total de repos,
        - la somme des star_gazers
        - la moyenne des star_gazers de l'utilisateur
    """
    user_git = 'JeanMiMi'
    password_git = '*******'  # ou bien TOKEN
    user_stats = []
    r = requests.get('https://api.github.com/'+user, auth=('user', 'pass'))
    resp = requests.get('https://api.github.com/users/'+user+'/repos', auth=(user_git, password_git))
    if resp.status_code != 200:
        user_stats=[resp.status_code, 0]
        # This means something went wrong.
        return user_stats, 0, 0, 0
    if resp == None:
        user_stats=["pas de repos", 0]
        moyenne = 0
        return user_stats, 0, 0, 0
    total = 0
    for repo in range(len(resp.json())):
        user_stats.append([resp.json()[repo]['name'],resp.json()[repo]['stargazers_count']])
        total += resp.json()[repo]['stargazers_count']
    nb_repos = len(user_stats)
    if nb_repos == 0:
        nb_repos = 1
    moyenne = round(total / nb_repos, 1)
    return user_stats, nb_repos, total, moyenne


# Programme principal

# Obtention des données
soup = getsoup()

# Extraction de la liste des contributeurs
liste_contributeurs = []
table_users = soup.table.tbody.find_all('a')
for contributeur in table_users:
    liste_contributeurs.append(contributeur.text)

# Nettoyage de la liste des contributeurs
while liste_contributeurs.__contains__(''):
    liste_contributeurs.remove('')

# Impression de la liste des contributeurs
print(liste_contributeurs, end='\n\n')


# Analyse de chaque contributeur
classement_users = pd.DataFrame()

for contributeur in range(len(liste_contributeurs)):
    contributions, nombre, total_stargazers, moyenne_stars  = get_user_stats(liste_contributeurs[contributeur])
    classement_users = classement_users.append({'ID_user': liste_contributeurs[contributeur],'Nombre des repos': nombre, 'Moyenne Stargazers': moyenne_stars, 'Total Stargazers': total_stargazers}, ignore_index=True)


# Tri des contributeurs par nombre de stargazers moyen
classement_users.sort_values('Moyenne Stargazers', inplace=True, ascending=False)

# Impression du classement
print(classement_users)

# Sauvegarde du classement
classement_users.to_csv("bestof_github_users.csv", sep=",", header = True)


