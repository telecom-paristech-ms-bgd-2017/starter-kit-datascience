
import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import numpy as np
import requests.auth
import operator
#


# recupération de  la clé
header = {"Authorization": "token " + "8bfdfd74ef56cd4ea8dc39e7b607709c2fda5625"}

# git hub api
GITHUB_API = 'https://api.github.com'

# reccuperation du resultat de la requête get
resultat = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(resultat.text, 'html.parser')
tableaux =soup.find_all("tr")

names = []
etoiles =[]

for element in tableaux[1:]:

    personne = element.find ("a").text

    names.append(personne)

list_info ={}

# reccupération des noms des utilisateurs et leurs classements
for name in names:

    url = GITHUB_API + "/users/" + name + "/repos"

    r = requests.get(url=url, headers=header)
    repos_data = json.loads(r.text)

    for data in repos_data:
        etoiles.append(data['watchers_count'])

    moyenne = (np.mean(etoiles))
    list_info[name] = moyenne

    list_info_classement = OrderedDict(sorted(list_info.items(), key=operator.itemgetter(1), reverse=True))
# classer les utilisateurs
    print("classement des utilisateur :")

    for keys, values in list_info_classement.items():
        print(str(keys) + "  à  " + str(values))


