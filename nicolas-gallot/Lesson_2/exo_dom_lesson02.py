# Crawling des resultats de la ville de Paris pour  2009 -- 2013
# Source : http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013

import requests
from bs4 import BeautifulSoup


def geturltemplate():
    return "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="


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


# Main script

years = [2009, 2010, 2011, 2012, 2013]
className = "libellepetit G"

for year in years:
    url = geturltemplate() + str(year)
    soup = getBeautifulSoupObjectfromUrl(url)
    classes = soup.find_all(class_=className)
    for d in dataTypeMapping():
        for c in columnMameMapping():
            value = extractvaluefromclasses(c, d, classes)
            printresult(year, c, d, value)




