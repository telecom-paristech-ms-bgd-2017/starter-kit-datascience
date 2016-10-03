# coding: utf8
import requests
from bs4 import BeautifulSoup


def scrap_data_for_year(annee):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?" +\
        "icom=056&dep=075&type=BPS&param=5&exercice="+str(annee)
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    # on prend toutes les tables
    tables = soup.body.find_all("table", recursive=False)
    # c'est la troisième qui nous interesse (soit 2 car commence à 0)
    table = tables[2]
    lignes = table.find_all("tr", recursive=False)
    ligneA = lignes[5]
    elA = ligneA.find_all("td")[1].string
    ligneB = lignes[9]
    elB = ligneB.find_all("td")[1].string
    ligneC = lignes[17]
    elC = ligneC.find_all("td")[1].string
    ligneD = lignes[22]
    elD = ligneD.find_all("td")[1].string

    comptes = Comptes(annee, elA, elB, elC, elD)
    return comptes


class Comptes:
    def __init__(self, annee="", a="", b="", c="", d=""):
        self.annee = annee
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __str__(self):
        resultat = "------------\n"
        resultat += "Comptes pour l'année "+str(self.annee)+"\n"
        resultat += "Produits de fonctionnement: "+str(self.a)+"\n"
        resultat += "Charges de fonctionnement: "+str(self.b)+"\n"
        resultat += "Ressources d'investissement: "+str(self.c)+"\n"
        resultat += "Emplois d'investissement: "+str(self.d)+"\n"
        return resultat


def get_multiple_years(year_list):
    result = []
    for year in year_list:
        result.append(scrap_data_for_year(year))
    return result

years = list(range(2010, 2016))
