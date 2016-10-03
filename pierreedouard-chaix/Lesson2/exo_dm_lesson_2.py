# -*- coding: utf-8 -*-
# PARIS 2013 : ("056", "075", "BPS", "5", 2013)

import requests
import bs4
import csv
import os

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
    RESULTATS = []
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
        RESULTATS.append(TABLEAU_SIMPLIFIE)
    return RESULTATS

def construireIndexAvecZeros(n):
    if n < 10:
        return "00"+str(n)
    elif n < 100:
        return "0"+str(n)
    elif n <1000:
        return str(n)

def recupValeursCommuneDepartement(departement, type, param, exercicedebut, exercicefin):
    RESULTATS = []
    for i in range(0,1000):
        print(i)
        try:
            RESULTATS.append(recupValeurs(construireIndexAvecZeros(i), departement, type, param, exercicedebut, exercicefin))
        except IndexError:
            continue

    try:
        os.remove("RESULTATS_"+str(departement)+"_"+str(exercicedebut)+"_"+str(exercicefin)+".csv")
    except OSError:
        print "Le fichier n'existe pas encore"
    c = csv.writer(open("RESULTATS_"+str(departement)+"_"+str(exercicedebut)+"_"+str(exercicefin)+".csv", "wb"))
    c.writerow(["Département", "Ville", "Année", "A Euros par habitant", "A Moyenne de la strate", "B Euros par habitant", "B Moyenne de la strate", "C Euros par habitant", "C Moyenne de la strate", "D Euros par habitant", "D Moyenne de la strate"])
    for resultat in RESULTATS:
        print(resultat)
        c.writerow([resultat[0]["Departement"], resultat[0]["Ville"], resultat[0]["Annee"], resultat[0]["Valeurs"]["A"][0], resultat[0]["Valeurs"]["A"][1],resultat[0]["Valeurs"]["B"][0], resultat[0]["Valeurs"]["B"][1], resultat[0]["Valeurs"]["C"][0], resultat[0]["Valeurs"]["C"][1], resultat[0]["Valeurs"]["D"][0], resultat[0]["Valeurs"]["D"][1]])

# Récupérer les valeurs pour toutes les villes du Calvados
recupValeursCommuneDepartement(construireIndexAvecZeros(95), "BPS", "5", 2014, 2014)