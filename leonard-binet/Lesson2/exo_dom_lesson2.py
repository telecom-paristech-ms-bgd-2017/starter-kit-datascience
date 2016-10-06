# coding: utf8
import requests
import re
from bs4 import BeautifulSoup


def get_data_for_filters(annee, id_commune="056", methode="post", departement="075"):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php"
    filters = {
        "DEP": departement,
        "EXERCICE": annee,
        "ICOM": id_commune,
        "PARAM": "0",
        "TYPE": "BPS",
        "comm": "0",
    }
    if methode == "get":
        request = requests.get(url, params=filters)
    elif methode == "post":
        request = requests.post(url, data=filters)
    else:
        pass
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    comptes = soup_to_data(soup)
    return comptes


def soup_to_data(soup):
    # on prend toutes les tables
    tables = soup.body.find_all("table", recursive=False)
    # c'est la troisième qui nous interesse (soit 2 car commence à 0)
    try:
        table = tables[2]
        lignes = table.find_all("tr", recursive=False)
        ligneAnnee = lignes[0]
        elAnnee = ligneAnnee.find_all("td")[2].string
        ligneVille = lignes[1]
        elVille = ligneVille.find_all("td")[1].string
        ligneA = lignes[5]
        elA = ligneA.find_all("td")[1].string
        ligneB = lignes[9]
        elB = ligneB.find_all("td")[1].string
        ligneC = lignes[17]
        elC = ligneC.find_all("td")[1].string
        ligneD = lignes[22]
        elD = ligneD.find_all("td")[1].string
    except IndexError:
        return Comptes()
    comptes = Comptes(elVille, elAnnee, elA, elB, elC, elD)
    return comptes


class Comptes:
    def __init__(self, ville="",annee="", a="", b="", c="", d=""):
        self.annee = annee
        self.ville = ville
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __str__(self):
        resultat = "------------\n"
        resultat += "Comptes pour l'année "+str(self.annee)+" de la ville " + \
            str(self.ville)+"\n"
        resultat += "Produits de fonctionnement: "+str(self.a)+"\n"
        resultat += "Charges de fonctionnement: "+str(self.b)+"\n"
        resultat += "Ressources d'investissement: "+str(self.c)+"\n"
        resultat += "Emplois d'investissement: "+str(self.d)+"\n"
        return resultat


def get_years_departement(year_list, departement):
    result = []
    dict_villes = liste_ville_dans_departement(departement)
    for id_commune in dict_villes.values():
        print("--requete pour ville id: "+str(id_commune)+" --")
        for year in year_list:
            print("--annee: "+str(year)+" --")
            result.append(get_data_for_filters(annee=year, id_commune=id_commune, departement=departement))
    return result

years = list(range(2010, 2016))


def liste_ville_dans_departement(num_departement="014"):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/RDep.php"
    resultats = {}
    for lettre in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        filters = {
            "DEP": num_departement,
            "TYPE": "BPS",
            "LETTRE": lettre,
            }
        print("---LANCEMENT REQUETES POUR VILLES COMMENCANT PAR UN '"+lettre+"'")
        request = requests.post(url, data=filters)
        soup = BeautifulSoup(request.text, "html.parser")
        try:
            villes = soup.body.find_all("table", recursive=False)[1]
        except IndexError:
            print("Pas de ville pour cette lettre")
            pass
        for ville in villes.find_all("tr", recursive=False):
            nom = ville.td.a.font.contents[0]

            id_ville = ville.td.a["href"]
            pat = re.compile('\{\'ICOM\':(\d{3})\'')
            id_ville = id_ville.replace("javascript:openWithPostData('RComm_gfp.php',{", "").replace("}","").split(",")[0]
            id_ville = id_ville.split(":")[1].replace("'","")
            id_ville = pat.match(id_ville).group(1)
            resultats[nom] = id_ville
    return resultats
