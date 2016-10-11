import json
import requests
from bs4 import BeautifulSoup


def get_top_user(nombre_user=256):
    """ Permet d'obtenir les meilleurs contributeurs
     de github. Par défaut la fonction recherche les
     256 premiers """

    url = "https://gist.github.com/paulmillr/2657075"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    listes_balisea = soup.select("tbody > tr > td:nth-of-type(1) > a")
    liste_user = []

    i = 1
    for balisea in listes_balisea:
        if i > nombre_user:
            break
        liste_user.append(str(balisea.text))
        i += 1

    return liste_user


def get_projet(username):
    """ Permet d'obtenir tous les projets github
    d'un utilisateur particulier """

    credentials = {'Authorization': 'token 7283beba89b0cb0f9add0c11041975f5248d7d0a'}
    liste_projets = requests.get('https://api.github.com/users/' + username + '/repos', headers=credentials)
    return json.loads(liste_projets.text)


def calcul_moyenne_stars(liste_projets_json):
    """ Permet de calculer les moyenne des
    stars pour une liste de projets au format json"""

    if not liste_projets_json:
        return 0

    nombre_stars = 0.0
    for projet in liste_projets_json:
        # if projet['stargazers_count']:
        nombre_stars += projet['stargazers_count']

    moyenne_stars = nombre_stars / len(liste_projets_json)

    return moyenne_stars


def get_moyenne_star_par_user(nombre_user=256):
    """ Retourne pour les n meilleurs contributeurs,
    256 par défaut, la moyenne des stars pour leurs projets"""

    moyenne_stars_par_users = {}

    liste_top_user = get_top_user(nombre_user)

    for user in liste_top_user:
        liste_projets = get_projet(user)
        moyenne_stars = calcul_moyenne_stars(liste_projets)
        moyenne_stars_par_users[user] = moyenne_stars
    return moyenne_stars_par_users


if __name__ == '__main__':
    print(sorted(get_moyenne_star_par_user(10).items(), key=lambda x: x[1], reverse=True))
