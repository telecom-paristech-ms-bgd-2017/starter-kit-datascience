# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:51:41 2016

@author: nuttinck
"""

import requests
from bs4 import BeautifulSoup


def cleanMontant(eurHab_draft, moyStrate_draft):
    eurHab = eurHab_draft.text.replace('</td>', '').replace(u'\xa0', '') \
             .replace(' ', '')
    moyStrate = moyStrate_draft.text.replace('</td>', '') \
        .replace(u'\xa0', '').replace(' ', '')
    return int(eurHab), int(moyStrate)


def getValueClean(soup, classname):  # Document Object Model
    coordonnees = {"TOTAL DES PRODUITS DE FONCTIONNEMENT (A)": (1, 2),
                   "TOTAL DES CHARGES DE FONCTIONNEMENT (B)": (4, 5),
                   "TOTAL DES EMPLOIS D'INVESTISSEMENT (C)": (10, 11),
                   "TOTAL DES EMPLOIS D'INVESTISSEMENT (D)": (13, 14)}
    res_str = soup.find_all(class_=classname)  # Pr recuperer tte la class
    montant = {}
    if res_str:
        for m in coordonnees.keys():
            montant[m] = cleanMontant(res_str[coordonnees[m][0]],
                                      res_str[coordonnees[m][1]])

    return montant


def getComptesSoup(annee, departement, commune):
    com_str = "00" + str(commune)
    dep_str = "00" + str(departement)
    URL = "http://alize2.finances.gouv.fr/communes/eneuro/" \
        + "detail.php?icom=" + com_str[-3:] + "&dep=" + dep_str[-3:] \
        + "&type=BPS&param=5&exercice=" + str(annee)
    r = requests.get(URL)

    return BeautifulSoup(r.text, 'html.parser')


def displayComptesCommune(annee, departement, commune):
    displayed_cpt = "================================= \nComptes de l'annee " \
        + str(annee) + " de la ville N°" + str(commune) + " (" \
        + str(departement) + ") : \n\n"
    soupComptes = getComptesSoup(annee, departement, commune)
    cpt_dict = getValueClean(soupComptes, "montantpetit G")
    if not cpt_dict:
        displayed_cpt += "/!\ Aucune donnee ! \n"
    for cpt, res in cpt_dict.items():
        displayed_cpt += cpt + " = " + str(res) + "\n"
    displayed_cpt += "================================= \n"

    return displayed_cpt

# Affiche les compte de la commune de Paris
for an in range(2009, 2014):
    print(displayComptesCommune(an, 75, 56))

# Affiche les compte de la commune de Caen
for an in range(2009, 2014):
    print(displayComptesCommune(an, 14, 118))

# Affiche les compte de 2013 des 120 premières communes du Calvados
for com in range(120):
    print(displayComptesCommune(2013, 14, com))

    # Ligne associée à la conne montant par habitant de la ligne A :
    # <td class="libellepetit G">TOTAL DES PRODUITS DE FONCTIONNEMENT = A</td>
    # <td class="montantpetit G">2 308&nbsp;</td>

    # Ligne associée à la conne montant par habitant de la ligne B :
    # <td class="libellepetit G">TOTAL DES CHARGES DE FONCTIONNEMENT = B</td>
    # <td class="montantpetit G">2 235&nbsp;</td>

    # Ligne associée à la conne montant par habitant de la ligne C :
    # <td class="libellepetit G">TOTAL DES CHARGES DE FONCTIONNEMENT = B</td>
    # <td class="montantpetit G">1 157&nbsp;</td>

    # Ligne associée à la conne montant par habitant de la ligne D :
    # <td class="libellepetit G">TOTAL DES EMPLOIS D'INVESTISSEMENT = D</td>
    # <td class="montantpetit G">1 048&nbsp;</td>

    #  Ligne associée à la conne moyenne de la strate de la ligne A :
    # <td class="montantpetit G">2 308&nbsp;</td>

    #  Ligne associée à la conne moyenne de la strate de la ligne A :
    # <td class="montantpetit G">2 235&nbsp;</td>