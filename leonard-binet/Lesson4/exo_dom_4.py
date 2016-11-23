# ########## ETAPE 1 - SCRAPING DE LEBONCOIN.FR ############
import unittest
import requests
import re
import ipdb


class Scrap_RechercheZoe:
    """
    Scraping pour une liste de régions
    """

    def __init__(self, region_list=["ile_de_france"]):
        """
        """
        self.host = "https://www.leboncoin.fr/voitures/offres"
        self.region_list = region_list
        self.url_ext = "/?q=zoe"
        self.requests = {}  # une par page
        self.soups = {}
        self.urls = {}
        self.data = {}

    def scrap_zoe_from_regions(self, region_list):
        for region in region_list:
            self.scrap_zoe_from_region(region)

    def scrap_zoe_from_region(self, region="ile_de_france"):
        """
        Fait première recherche, obtient tout et notamment nombre de pages
        """
        from bs4 import BeautifulSoup
        page = 1
        host = self.host
        url_ext = self.url_ext
        region = "/" + region
        page_url = "&o=" + str(page)
        url = host + region + url_ext + page_url
        ipdb.set_trace()
        req = requests.get(url)
        id_scrap = "menu_" + region + "_" + str(page)

        self.requests[id_scrap] = req
        self.soups[id_scrap] = BeautifulSoup(req.text, 'html.parser')
        self.soup_to_urls()

    def soup_to_urls(self):
        for key, soup in self.soups.items():
            ul = soup.find(id="listingAds").section.section.ul
            li_s = ul.find_all("li", recursive=False)
            try:
                url_s = list(map(lambda x: "https:" + x.a["href"], li_s))
                self.urls[key] = url_s
            except AttributeError:
                print("Pour l'élément suivant, erreur: ", li_s)
                for number, li in enumerate(li_s):
                    url_s = []
                    try:
                        url_s.append("https:" + li.a["href"])
                    except:
                        print("Problème: élément " + str(number) + " / " + key)
                        continue
                self.urls[key] = url_s

    def scrap_urls(self):
        pass


test = Scrap_RechercheZoe()
test.scrap_zoe_from_region()


"""
    def request_to_li(self, request):
        soup = BeautifulSoup(request.text, 'html.parser')
        ul = soup.find(id="listingAds").section.section.ul
        li_s = ul.find_all("li", recursive=False)  # plus de pubs (div, pas li)
        # retourne une liste des li
        return li_s
        # rajouter si vide
    # on veut l'url uniquement


    def get_urls_for_pages_for_region(self, region_list, nb_pages):


        result_dict = {}
        for region in region_list:
            result_url_list = []
            for page in range(nb_pages):
                # on effectue la requête
                request = self.scrap_zoe_from_region_page(
                    region=region, page=page)
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
    return soup.find(id="adview").section.section.find_all("div", {"class": "line"})


def lines_to_data(lines):
    # prix: 1ere ligne
    prix = lines[1].find("span", {"class": "value"}).string.replace(" ", "")
    modele = lines[4].find("span", {"class": "value"}).string.replace(" ", "")
    annee_modele = lines[5].find(
        "span", {"class": "value"}).string.replace(" ", "")
    kilometrage = lines[6].find(
        "span", {"class": "value"}).string.replace(" ", "")
    return [prix, modele, annee_modele, kilometrage]

url_test = "https://www.leboncoin.fr/voitures/1018969268.htm?ca=12_s"
# idf_urls = get_urls_for_pages_for_region(["ile_de_france"], 4)
annonce = scrap_url(url_test)
data = lines_to_data(annonce)

#### TESTS UNITAIRES #####


class ZoeTest(unittest.TestCase):


    def setUp(self):
        self.urltest = "https://www.google.fr/"

    def test_scrap_zoe_from_region_page(self):

        elt = scrap_zoe_from_region_page(self.urltest)
        self.assertEquals(elt.status_code, 200)
        with self.assertRaises(IpError):
            scrap_zoe_from_region_page("seser")


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
