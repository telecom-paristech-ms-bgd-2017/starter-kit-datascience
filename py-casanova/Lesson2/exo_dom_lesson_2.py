#! /usr/bin/python3.5
import requests
from bs4 import BeautifulSoup

url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'

global_account = {}

for year in range(2009, 2014):
    date = str(year)
    form_data = {'ICOM': '056', 'DEP': '075', 'TYPE': 'BPS', 'PARAM': '0', 'dep': '', 'reg': '', 'nomdep': '',
                 'moysst': '', 'exercice': '', 'param': '', 'type': '', 'siren': '', 'comm': '0', 'EXERCICE': date}
    results = requests.post(url, form_data)
    soup = BeautifulSoup(results.text, "html.parser")
    print("Getting year " + date + " for city")

    # Getting figures by type (in keuros, by inhabitant, strata mean)
    figures = soup.find_all("td", class_="montantpetit G")
    keuros = []
    by_inhab = []
    strata = []
    for i, el in enumerate(figures):
        figures[i] = int(el.text.replace(u'\xa0', '').replace(" ", ""))
        if(i % 3 == 0):
            keuros.append(figures[i])
        elif(i % 3 == 1):
            by_inhab.append(figures[i])
        elif(i % 3 == 2):
            strata.append(figures[i])

    # Getting corresponding aggregate name
    aggregates = soup.find_all("td", class_="libellepetit G")
    for i, el in enumerate(aggregates):
        aggregates[i] = el.text

    # Saving in yearly account dict & adding to global account dict of dict
    yearly_account = {}
    for i, aggregate in enumerate(aggregates):
        yearly_account[aggregate] = [keuros[i], by_inhab[i], strata[i]]

    global_account[year] = yearly_account

for year in range(2009, 2014):
    print("\n")
    print("Year " + str(year))

    print("TOTAL DES PRODUITS DE FONCTIONNEMENT = A ")
    print(global_account[year].get("TOTAL DES PRODUITS DE FONCTIONNEMENT = A"))

    print("TOTAL DES CHARGES DE FONCTIONNEMENT = B ")
    print(global_account[year].get("TOTAL DES CHARGES DE FONCTIONNEMENT = B"))

    print("TOTAL DES RESSOURCES D'INVESTISSEMENT = C ")
    print(global_account[year].get(
        "TOTAL DES RESSOURCES D'INVESTISSEMENT = C"))

    print("TOTAL DES EMPLOIS D'INVESTISSEMENT = D ")
    print(global_account[year].get("TOTAL DES EMPLOIS D'INVESTISSEMENT = D"))
