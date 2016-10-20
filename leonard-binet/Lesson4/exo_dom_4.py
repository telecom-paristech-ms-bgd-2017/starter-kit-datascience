# ########## ETAPE 1 - SCRAPING DE LEBONCOIN.FR ############
import unittest
import requests
from bs4 import BeautifulSoup
import re


def scrap_zoe_from_region_page(region="ile_de_france", page=1):
    host = "https://www.leboncoin.fr"
    category = "/voitures"
    region = "/" + region
    research = "/?q=zoe"
    page = "&o=" + str(page)
    url = host + category + region + research + page
    req = requests.get(url)
    if req.status_code == 200:
        return req
    else:
        raise ValueError("Impossible de se connecter")


def request_to_li(request):
    soup = BeautifulSoup(request.text, 'html.parser')
    ul = soup.find(id="listingAds").section.section.ul
    li_s = ul.find_all("li", recursive=False)  # plus de pubs (div, pas li)
    # retourne une liste des li
    return li_s
    # rajouter si vide

# on veut l'url uniquement


def li_to_urls(block_list):
    try:
        url_s = list(map(lambda x: x.a["href"], block_list))
        return url_s
    except AttributeError:
        print("Pour l'élément suivant, erreur: ", block_list)
        return []
        # problème si un élément du tableau merde, tout merde


def get_urls_for_pages_for_region(region_list, nb_pages):
    result_dict = {}
    for region in region_list:
        result_url_list = []
        for page in range(nb_pages):
            # on effectue la requête
            request = scrap_zoe_from_region_page(region=region, page=page)
            # on prend les blocs 'li'
            li_list = request_to_li(request)
            # on extrait la liste des urls
            urls = li_to_urls(li_list)
            # on nettoie les urls
            urls_clean = map(lambda x: "https:" + x, urls)
            # on ajoute cela au résultat
            result_url_list += urls_clean
        result_dict[region] = result_url_list
    return result_dict


def scrap_url(url):
    # prend pour argument une liste d'url et renvoie les informations utiles
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, "html.parser")
    return soup


url_test = "https://www.leboncoin.fr/voitures/1018931643.htm?ca=12_s"
# idf_urls = get_urls_for_pages_for_region(["ile_de_france"], 4)
annonce = scrap_url(url_test)


#### TESTS UNITAIRES #####


class ZoeTest(unittest.TestCase):

    """Test case utilisé pour tester les fonctions du module "Zoé"."""

    def setUp(self):
        """Initialisation des tests."""
        self.urltest = "https://www.google.fr/"

    def test_scrap_zoe_from_region_page(self):
        """Test le fonctionnement de la fonction 'scrap_zoe_from_region_page'."""
        elt = scrap_zoe_from_region_page(self.urltest)
        self.assertEquals(elt.status_code, 200)
        with self.assertRaises(IpError):
            scrap_zoe_from_region_page("seser")

"""
Par ailleurs voici l'exercice que je vous propose pour  la semaine prochaine.
L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿


1 - Obtenir données sur le prix de vente des voitures Zoé sur le bon coin.
Données nécessaires:
 - version (3 différentes)
 - année
 - kilométrage
 - prix
 - téléphone
 - pro/particulier
A - Obtenir les urls des vraies annonces
B - Charger chaque annonce et récolter les informations utiles

2 - Obtenir le prix de l'argus selon les différents modèles.

"""
