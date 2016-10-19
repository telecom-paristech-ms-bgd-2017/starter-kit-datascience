from __future__ import division
from collections import defaultdict
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, json, sys
from operator import itemgetter
import threading, time


######################
# VARIABLES GLOBALES #
######################

token = 'tok2a8f990dc036f8f7bfd23fbb5dde3746e22ee2d2'
etoiles = defaultdict(lambda: 0)

################################
#           Fonctions          #
################################
def add_stars(contributeur_etoiles):
    global etoiles
    etoiles[contributeur_etoiles[0]] = contributeur_etoiles[1]


def contributor_stars(contributeur):
    repos = json.loads(api_get_repos(contributeur))
    total_stars = sum([repo['stargazers_count'] for repo in repos])

    try:
        return (contributeur, total_stars / len(repos))
    except ZeroDivisionError:
        print("User {u} doesn't own any repo, moving on.".format(u=contributeur))
        return(contributeur, 0)


def api_get_repos(contributeur):
        url = 'https://api.github.com/users/' + contributeur + '/repos'
        resp = .get(url, params=token)
        if resp.status_code != 200:
            print('json.loads')
            print(json.loads(resp.text)['message'])
            resp.raise_for_status()
        return resp.text
requests




#Le user principal
master_user = "paulmillr/2657075"

#Recuperer la liste de scontributeurs
url = 'https://gist.github.com/' + master_user;
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
rows = soup.select('#readme table tr')[1:]


#Liste des contributeurs
contributeurs = [r.select('td:nth-of-type(1) > a')[0].text for r in rows]
print(contributeurs)
print(len(contributeurs))


#On boucle sur les contributeurs
for contributeur in contributeurs:
    args = {'args': (contributeur,), 'callback': add_stars}
    contributor_stars(contributeur)

sorted_stars = sorted(etoiles.items(), key=itemgetter(1), reverse=True)

print('sorted_stars')
print(sorted_stars)

