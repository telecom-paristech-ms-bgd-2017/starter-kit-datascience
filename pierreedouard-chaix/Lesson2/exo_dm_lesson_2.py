# -*- coding: utf-8 -*-
# PARIS 2013 : ("056", "075", "BPS", "5", 2013)

import requests
import bs4

URL_BASE = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?"
LABEL_COMMUNE = "icom"
LABEL_DEPARTEMENT = "dep"
LABEL_TYPE = "type"
LABEL_PARAM = "param"
LABEL_EXERCICE = "exercice"

def escapeandint(s):
    try:
        ss = int(s.replace(u'','').replace(' ',''))
        return ss
    except ValueError:
        print "Erreur de conversion !"

def escape(s):
    try:
        ss = s.encode('ascii', 'ignore')
        return ss
    except ValueError:
        print "Erreur de conversion !"

def construireURL(commune, departement, type, param, exercice):
    return URL_BASE + LABEL_COMMUNE + "=" + commune + "&" + LABEL_DEPARTEMENT + "=" + departement + "&" + LABEL_TYPE + "=" + type + "&" + LABEL_PARAM + "=" + param + "&" + LABEL_EXERCICE + "=" + str(exercice)

def recupValeurs(commune, departement, type, param, exercicedebut, exercicefin):
    for annee in range(exercicedebut, exercicefin + 1):
        URL = construireURL(commune, departement, type, param, annee)

        TABLEAU_COMPLET = [[]]
        TABLEAU_SIMPLIFIE = {}

        R = requests.get(URL)
        soup = bs4.BeautifulSoup(R.content, 'html.parser')

        for LIGNE in soup.find_all("table")[2].find_all("tr"):
            TABLEAU_LIGNE = LIGNE.find_all("td")
            LIGNE_POUR_TABLEAU = []
            for CELL in TABLEAU_LIGNE:
                LIGNE_POUR_TABLEAU.append(CELL.text)
            TABLEAU_COMPLET.append(LIGNE_POUR_TABLEAU)

        VALEURS = {}
        for LIGNE in TABLEAU_COMPLET:
            try:
                if LIGNE[1] == "ANALYSE DES EQUILIBRES FINANCIERS FONDAMENTAUX":
                    TABLEAU_SIMPLIFIE["Annee"] = escapeandint(LIGNE[2])
                if LIGNE[0][0:13] == "DEPARTEMENT :":
                    TABLEAU_SIMPLIFIE["Ville"] = LIGNE[1]
                    TABLEAU_SIMPLIFIE["Departement"] = LIGNE[0][14:]
                if LIGNE[3] == "TOTAL DES PRODUITS DE FONCTIONNEMENT = A":
                    VALEURS["A"] = [escapeandint(LIGNE[1]), escapeandint(LIGNE[2])]
                if LIGNE[3] == "TOTAL DES CHARGES DE FONCTIONNEMENT = B":
                    VALEURS["B"] = [escapeandint(LIGNE[1]), escapeandint(LIGNE[2])]
                if LIGNE[3] == "TOTAL DES RESSOURCES D'INVESTISSEMENT = C":
                    VALEURS["C"] = [escapeandint(LIGNE[1]), escapeandint(LIGNE[2])]
                if LIGNE[3] == "TOTAL DES EMPLOIS D'INVESTISSEMENT = D":
                    VALEURS["D"] = [escapeandint(LIGNE[1]), escapeandint(LIGNE[2])]
                TABLEAU_SIMPLIFIE["Valeurs"] = VALEURS
            except IndexError:
                continue
        TABLEAU_SIMPLIFIE["Valeurs"] = VALEURS
        print TABLEAU_SIMPLIFIE

def construireIndexAvecZeros(n):
    if n < 10:
        return "00"+str(n)
    elif n < 100:
        return "0"+str(n)
    elif n <1000:
        return str(n)

def recupValeursCommuneDepartement(departement, type, param, exercicedebut, exercicefin):
    for i in range(0,1000):
        try:
            recupValeurs(construireIndexAvecZeros(i), departement, type, param, exercicedebut, exercicefin)
        except IndexError:
            continue


# Récupérer les valeurs pour toutes les villes du Calvados
recupValeursCommuneDepartement(construireIndexAvecZeros(14), "BPS", "5", 2010, 2014)