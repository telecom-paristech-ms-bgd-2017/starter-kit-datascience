# @author : BENSEDDIK Mohammed
# @version : 0.2
# @desc : Crawler for financial results of accounts of Paris from 2010 to 2015

import requests
from bs4 import BeautifulSoup

url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
display_str_choice = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A","TOTAL DES CHARGES DE FONCTIONNEMENT = B",
                        "TOTAL DES RESSOURCES D'INVESTISSEMENT = C","TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

def display_value(ligne, display_str):
    per_habitant = ligne.select('td:nth-of-type(2)')[0].text.replace(u'\xa0','')
    mean_strat = ligne.select('td:nth-of-type(3)')[0].text.replace(u'\xa0','')

    print("*******************   " + display_str)
    print("Moyenne par habitant : " + str(per_habitant))
    print("Moyenne de la strat : " + str(mean_strat))


print("Debut ==================================================")

for year in range(2010, 2016):
    req = requests.get(url + str(year))

    soup = BeautifulSoup(req.text,'html.parser')

    lignes = soup.find_all(class_ = 'bleu')

    print("Resultats des comptes de la ville de Paris de l'annee : " + str(year))

    for ligne in lignes:
        title_gen = (ligne.find_all(class_ = 'libellepetit G'))
        if title_gen:
            title = title_gen[0].text
            for display_str_value in display_str_choice:
                if title == display_str_value:
                    display_value(ligne,display_str_value)

    print("\n\n\n")

print("Fin ==================================================")
