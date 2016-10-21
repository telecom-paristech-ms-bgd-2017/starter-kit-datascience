import urllib.request as req
from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import pandas as pd


def get_liste_ville(nbr_villes=10):
    url = "http://www.toutes-les-villes.com/villes-population.html"
    html = req.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    listes_balisea = soup.select("a.HomeTxtVert")

    liste_balises_a = []
    liste_villes = []

    for balisea in listes_balisea:
        liste_balises_a.append(str(balisea.text))

    for i in range(0, 2 * nbr_villes, 2):
        liste_villes.append(liste_balises_a[i])

    return liste_villes


def get_distances_villes(liste_villes):
    origins_destinations_for_google = ""

    for ville in liste_villes:
        origins_destinations_for_google += ville + "+France|"
    origins_destinations_for_google = origins_destinations_for_google[:-1]

    distance_google = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + origins_destinations_for_google + '&destinations=' + origins_destinations_for_google + '&key=AIzaSyDRTqWJiE3zELiD8jEY3J9HMBTF5SCZXQc')
    json_distances = json.loads(distance_google.text)

    matrice_resultat = pd.DataFrame(index=liste_villes, columns=liste_villes)

    clean_distances = []
    for index_ligne, ville_ligne in enumerate(liste_villes):
        for index_colonne, ville_colone in enumerate(liste_villes):
            matrice_resultat.set_value(ville_ligne, ville_colone,
                                       json_distances['rows'][index_ligne]['elements'][index_colonne]['distance']['value'])

    matrice_resultat.to_csv('Distances_villes.csv')

if __name__ == '__main__':
    liste_villes = get_liste_ville()
    get_distances_villes(liste_villes)