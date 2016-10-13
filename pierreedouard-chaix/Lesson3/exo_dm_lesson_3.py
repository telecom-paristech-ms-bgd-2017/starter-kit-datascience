# -*- coding: utf-8 -*-

import requests
import bs4
import os
import json
import numpy as np
import pandas as pd

USER = "pierreedouardchaix"
TOKEN = # Insérer un nouveau token

URL = "https://gist.github.com/paulmillr/2657075"
R = requests.get(URL)
soup = bs4.BeautifulSoup(R.content, 'html.parser')

# Récupératioun des 256 users les plus actif
user_table = soup.find("table").find_all("tr")

USER_IDS = []
for i in range(0,256):
    USER_IDS.append(user_table[i+1].find("a").text.encode("ascii")) # Pour ne pas récupérer la première ligne du tableau qui contient le header

print USER_IDS

# Nombre moyen de stars des repositories qui leur appartiennent
USER_STATS = []
count = 1
for USER in USER_IDS:
    print "Début de la récupération pour "+USER+" ("+str(count)+"e utilisateur)"
    PAGE = 1
    ENCORE = True
    REPOS_COUNT = 0
    STAR_COUNT = 0
    while(ENCORE):
        USER_REPOS = json.loads(requests.get("https://api.github.com/users/" + USER + "/repos?page=" + str(PAGE), auth=(USER, TOKEN)).text)
        if len(USER_REPOS) > 0 :
            for REPO in USER_REPOS:
                REPOS_COUNT += 1
                STAR_COUNT += REPO["stargazers_count"]
            PAGE = PAGE + 1
        else:
            ENCORE = False
    if REPOS_COUNT == 0: REPOS_COUNT = 1 # Pour ne pas diviser par 0 au final. C'est par exemple le cas de jfrazelle qui n'a pas de public repository.
    USER_STATS.append([USER, REPOS_COUNT, STAR_COUNT])
    count += 1

USER_STATS_DF = pd.DataFrame(USER_STATS)

USER_STATS_DF.columns = ["username","number of repositories", "number of stars"]
USER_STATS_DF["mean number of stars per repository"] = (USER_STATS_DF["number of stars"]/USER_STATS_DF["number of repositories"]).map(lambda x: round(x,2))

# Classement des utilisateurs par note moyenne et écriture en csv
USER_STATS_DF_SORTED = USER_STATS_DF.sort("mean number of stars per repository", ascending=False)
USER_STATS_DF_SORTED.to_csv("GITHUB_USERS_STAR_COUNT.csv", sep=";", header = True)
