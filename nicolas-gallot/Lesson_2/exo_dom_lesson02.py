# Crawling des resultats de la ville de Paris pour  2009 -- 2013
# Source : http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013

import requests
from bs4 import BeautifulSoup
import numpy as np
import itertools
from multiprocessing import Pool

def get_int_to_url_str_format(int):
    if int < 10:
        return "00{0}".format(str(int))
    elif int < 100:
        return "0{0}".format(str(int))
    elif int < 1000:
        return str(int)

def geturl(id_commune, dept, year):
    str_com = get_int_to_url_str_format(id_commune)
    str_dept = get_int_to_url_str_format(dept)
    str_year = str(year)
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom={0}&dep={1}&type=BPS&param=5&exercice={2}"
    return url.format(str_com, str_dept, str_year)

def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def dataTypeMapping():
    res = \
    {
        'A': "TOTAL DES PRODUITS DE FONCTIONNEMENT = A",
        'B': "TOTAL DES CHARGES DE FONCTIONNEMENT = B",
        'C': "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
        'D': "TOTAL DES EMPLOIS D'INVESTISSEMENT = D",
    }
    return res

def columnMameMapping():
    res = \
    {
        'Euros par habitant': 1,
        'Moyenne de la strat': 2
    }
    return res


def extractvaluefromclasses(columnName, dataType, classes):
    columnNameMapped = columnMameMapping()[columnName]
    dataTypeMapped = dataTypeMapping()[dataType]

    for c in classes:
        if c.text == dataTypeMapped:
            p = c.parent
            montants = p.findChildren(class_="montantpetit G")
            return montants[columnNameMapped].text
    return "not found"


def printresult(year, columnName, dataType, value):
    msg = "Year : " + str(year) + ";Column : " + columnName + ";Data type " + dataType + " ====> Value = " + value
    print(msg)


def process_commune_dept_year_combination(combination):
    commune = combination[0]
    departement = combination[1]
    year = combination[2]
    className = "libellepetit G"
    url = geturl(commune, departement, year)
    try:
        soup = getBeautifulSoupObjectfromUrl(url)
        classes = soup.find_all(class_=className)
        for d in dataTypeMapping():
            for c in columnMameMapping():
                value = extractvaluefromclasses(c, d, classes)
                if value != "not found":
                    return commune, departement, year, d, c, value
                else:
                    return []
    except:
        print("No data for : Commune {0}, dept {1}, year {2}".format(commune, departement, year))


# Main script - sequential

def main_sequential(combinations_):

    results = []

    for combination in combinations_:
        res = process_commune_dept_year_combination(combination)
        results.append(res)

    return results


def main_parallel(combinations_):
    pool = Pool()
    return pool.map(process_commune_dept_year_combination, combinations_)

def display_results(results):
    for res in results:
        if len(res)>0:
            print("Commune : {0}. Departement : {1}. Year : {2}. Datatype : {3}. Column : {4}. Value : {5}".format(res[0], res[1], res[2], res[3], res[4], res[5]))



# Main launcher
communes = np.arange(1, 50, dtype=np.int)
departements = [14, 75]
years = [2009, 2010, 2011, 2012, 2013]

# communes = np.arange(1, 3, dtype=np.int)
# departements = [14, 75]
# years = [2010, 2011]

combinations = itertools.product(communes, departements, years)

#results = main_sequential(combinations)
results = main_parallel(combinations)

display_results(results)
print ("Number of results : {0}".format(len(results)))




