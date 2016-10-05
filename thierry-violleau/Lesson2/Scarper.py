import requests
from bs4 import BeautifulSoup

base_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='

target_labels = [
    "TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
    "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"
]


def load_fiscal_year(year):
    return requests.get(base_url + str(year))


def get_all_fiscal_data_for_year(year):
    fiscal_data = load_fiscal_year(year)
    results = {}
    parser = BeautifulSoup(fiscal_data.text, 'html.parser')
    for node in parser.find_all(class_="libellepetit G"):
        if node.text in target_labels:
            key = node.text[-1]
            results[key] = extract_amounts(node)
    return results


def extract_amounts(node):
    decode = lambda text: int(text.replace(u'\xa0', '').replace(u' ', ''))
    children = node.parent.findAll(class_="montantpetit G")
    return decode(children[1].text), decode(children[2].text)


def get_all_fiscal_data_for_years(years):
    fiscal_data = {}
    for year in years:
        fiscal_data[year] = get_all_fiscal_data_for_year(year)
    return fiscal_data


print(get_all_fiscal_data_for_years([2009, 2010, 2011, 2012, 2013]))
