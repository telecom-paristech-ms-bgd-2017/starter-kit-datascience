
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import requests.auth
#



header = {"Authorization": "token " + "8bfdfd74ef56cd4ea8dc39e7b607709c2fda5625"}
GITHUB_API = 'https://api.github.com'

resultat = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(resultat.text, 'html.parser')
tableaux =soup.find_all("tr")

names = []
etoiles =[]
for element in tableaux[1:]:

    personne = element.find ("a").text

    names.append(personne)

list_info ={}
for name in names:

    url = GITHUB_API + "/users/" + name + "/repos"

   # url2= "https://github.com/" +name+"?tab = repositories"
    #print(url2)
    r = requests.get(url=url, headers=header)
    repos_data = json.loads(r.text)

    for data in repos_data:
        etoiles.append(data['watchers_count'])
    moyenne = (np.mean(etoiles))
    list_info[name] = moyenne
   


