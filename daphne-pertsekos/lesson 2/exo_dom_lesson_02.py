# coding: utf8
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests

def data_by_city_by_year(departement,exercice, icom):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom="+icom+"&dep="+departement+\
          "&type=BPS&param=5&exercice="+exercice
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def filter_interesting_row_by_label(cells_with_bold_label):
    interesting_row = {}
    for cell in cells_with_bold_label:
        if cell.text in labels:
            interesting_row[cell.text[-1]] = cell.parent
    return interesting_row


def extract_value_from_row(tr_tag):
    dico = {}
    dico['by_habitant'] = tr_tag.find_all("td")[1].text
    dico['by_strate'] = tr_tag.find_all("td")[2].text
    dico['label'] = tr_tag.find_all("td")[3].text
    return dico


def print_bilan(commune, city_data):
    print ("************************     {}    **********************".format(commune))
    for key, value in city_data.items():
        print(value["label"])
        print("{}/ {}".format(value["by_habitant"], value["by_strate"]))


def analysis_by_city_by_year(departement,exercice,icom):
    city_data = data_by_city_by_year(departement,exercice,icom)
    interesting_cells = city_data.find_all("td", {"class":'libellepetit G'})
    interesting_row = filter_interesting_row_by_label(interesting_cells)
    final_data = {}
    for key,value in  interesting_row.items():
        final_data[key] = extract_value_from_row(value)

    return final_data


labels = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
          "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

# Analyse de Paris
city_data = analysis_by_city_by_year("075","2013","056")
print_bilan("PARIS", city_data)

# Analyse des villes du calvados
city_data = analysis_by_city_by_year("014","2013","118")
print_bilan("CAEN", city_data)
