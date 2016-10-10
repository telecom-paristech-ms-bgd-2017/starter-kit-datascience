# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""

import requests
import re
import bs4


# Liste des données à traiter
years = list(range(2009, 2016))
cat_fiOutput = ['A', 'B', 'C', 'D']
tableau = {}

# Fonction de récupération des comptes de la ville de Paris
def get_comptes(year):

    urlparis = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+str(year)
    comptes_paris = requests.get(urlparis)
    soup_comptes = bs4.BeautifulSoup(comptes_paris.text, 'html.parser')
    return soup_comptes



# collecte, stockage et impression des informations recherchées
for year in years:
    comptes_annuels = get_comptes(year)
    cat_fiInput = comptes_annuels.find_all(class_="libellepetit G")
    book = {}
    tableau[year]= book
    for catIn in cat_fiInput:
        for catOut in cat_fiOutput:
            if catIn.find(string=re.compile(' = '+catOut+'$')):
                Euro_hb = catIn.previous_sibling.previous_sibling.previous_sibling.previous_sibling.text
                Euro_hb = str(Euro_hb).rstrip()
                Moy_strat = catIn.previous_sibling.previous_sibling.text
                Moy_strat = str(Moy_strat).rstrip()
                print('\nAnnée ', year, catIn.text)
                print("Euros par habitant : ", Euro_hb )
                print("Moyenne de la strate (€) : ", Moy_strat )
                book[catIn.text]=(("Euros par habitant : ", Euro_hb),("Moyenne de la strate : ", Moy_strat ))

print(tableau)












