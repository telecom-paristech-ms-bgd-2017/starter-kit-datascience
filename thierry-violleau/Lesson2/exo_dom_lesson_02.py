import requests
from bs4 import BeautifulSoup

Base_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
#http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=118&dep=014&type=BPS&param=5&exercice=2013

# icom and department number could also be retrieved by scarping http://www.insee.fr/fr/bases-de-donnees/
Cities = {
    "paris" : ('056', '075'),
    "caen": ('118', '014'),

}

Params = {
    'icom': '???', # to be provided
    'dep': '???', # to be provided
    'type': 'BPS',
    'param': 5,
    'exercice': 2013
}

Target_labels = [
    "TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
    "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"
]

Data_labels = [
    "Euros par habitant",
    "Moyenne de la strate"
]

def load_fiscal_year(icom, dep, year):
    Params['icom'] = icom
    Params['dep'] = dep
    Params['year'] = year
    return requests.get(Base_url, params=Params)


def get_all_fiscal_data_for_year(icom, dep, year):
    fiscal_data = load_fiscal_year(icom, dep, year)
    results = {}
    parser = BeautifulSoup(fiscal_data.text, 'html.parser')
    for node in parser.find_all(class_="libellepetit G"):
        if node.text.strip() in Target_labels:
            key = node.text[-1] # use the last letter from the matching text as key in results
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

def get_all_fiscal_data_for_years_and_cities(cities, years):
    results = {}
    for city in cities:
        city = city.lower()
        if city in Cities:
            icom, dep = Cities[city]
            results[city] = get_all_fiscal_data_for_years(icom, dep, years)
        else:
            print("Unrecognized city: ", city)
    return results

def pretty_print(data):
    for city in data.keys():
        print("Data for " + city)
        for year in data[city].keys():
            print("\t" + str(year))
            for label in Target_labels:
                print("\t\t" + label[-1])
                for i in range(0, 2):
                    print("\t\t\t" + Data_labels[i] + "=" + str(data[city][year][label[-1]][i]))

#print(get_all_fiscal_data_for_years_and_cities(["Paris", "Caen"], [2009, 2010, 2011, 2012, 2013]))
pretty_print(get_all_fiscal_data_for_years_and_cities(["Paris", "Caen"], [2009, 2010, 2011, 2012, 2013]))

