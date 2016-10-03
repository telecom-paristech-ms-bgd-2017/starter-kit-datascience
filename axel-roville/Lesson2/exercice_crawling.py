import requests
import re
from bs4 import BeautifulSoup

base_url = "http://alize2.finances.gouv.fr/communes/eneuro/"
detail_base_url = base_url + "detail.php?type=BPS"
dep_base_url = base_url + "RDep.php"

def getDataByExerciceAndDepartment(year, dep):
    for name, ID in communesByDepartment(dep).items():
        print("Commune: " + name)
        getDataByExerciceAndDepartmentAndCommune(year, dep, ID)


def getDataByExerciceAndDepartmentAndCommune(year, dep, com):
    url = detail_base_url
    url += "&exercice=" + year
    url += "&dep=" + dep
    url += "&icom=" + com

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.select("table:nth-of-type(3)")[0]
    printLines(table)

def cellsInLine(line):
    # the indices we want to look for are 1 and 2 (0 based)
    return line.select("td")[1:3]

def lineInTable(table, lineNb):
    return table.select("tr:nth-of-type(" + str(lineNb) + ")")[0]

def cell_content(cell):
    return cell.text.replace(u'\xa0', '').replace(' ', '')

def printLines(table):
    lines = {
        "TOTAL DES PRODUITS DE FONCTIONNEMENT = A": 8,
        "TOTAL DES CHARGES DE FONCTIONNEMENT = B": 12,
        "TOTAL DES RESSOURCES D'INVESTISSEMENT = C": 20,
        "TOTAL DES EMPLOIS D'INVESTISSEMENT = D": 25
    }

    for key, lineNb in lines.items():
        cells = cellsInLine(lineInTable(table, lineNb))
        clean_cells = list(map(cell_content, cells))

        print(key)
        print("\tEuros par habitant   : " + clean_cells[0])
        print("\tMoyenne de la strate : " + clean_cells[1])

def communesByDepartment(dep):
    url = dep_base_url + "?type=BPS&dep=" + dep
    main_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = main_soup.select("table:nth-of-type(1)")[0]

    regex_id_commune = re.compile("'ICOM':'([0-9]*)'")

    data = {'DEP': dep, 'TYPE': 'BPS'}

    result = {}
    for link_lettre in table.select("td")[3:-1]:
        data['LETTRE'] = link_lettre.text
        resp = requests.post(dep_base_url, data = data)
        soup = BeautifulSoup(resp.text, 'html.parser')
        cols = soup.select("table")[1:]
        communes = cols[0].select('td')
        communes.extend(cols[1].select('td'))
        for commune in communes:
            href = commune.select('a')[0]['href']
            match_id = regex_id_commune.search(href)
            result[cell_content(commune)] = match_id.group(1)
    return result

# TEST
# getDataByExerciceAndDepartmentAndCommune('2013', '075', '056')
getDataByExerciceAndDepartment('2013', '014')
