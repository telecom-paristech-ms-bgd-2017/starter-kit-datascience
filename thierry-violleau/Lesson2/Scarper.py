import requests
from bs4 import BeautifulSoup

base_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=118&dep=014&type=BPS&param=5&exercice=2013

params = {
    'icom': '???',
    'dep': '???',
    'type': 'BPS',
    'param': 5,
    'exercice': 2013
}

target_labels = [
    "TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
    "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"
]


def load_fiscal_year(icom, dep, year):
    params['icom'] = icom
    params['dep'] = dep
    params['year'] = year
    return requests.get(base_url, params=params)


def get_all_fiscal_data_for_year(icom, dep, year):
    fiscal_data = load_fiscal_year(icom, dep, year)
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


def get_all_fiscal_data_for_years(icom, dep, years):
    fiscal_data = {}
    for year in years:
        fiscal_data[year] = get_all_fiscal_data_for_year(icom, dep, year)
    return fiscal_data

def pretty_print(data):
    pass

cities = {
    "Paris" : ('056', '075'),
    "Caen": ('118', '045'),

}
for city in cities.keys():
    print("Data for " + city + ": ")
    icom, dep = cities[city]
    print(get_all_fiscal_data_for_years(icom, dep, [2009, 2010, 2011, 2012, 2013]))

