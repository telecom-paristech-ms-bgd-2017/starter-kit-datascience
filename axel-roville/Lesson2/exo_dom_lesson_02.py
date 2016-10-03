import requests
import re
import datetime
import sys, getopt
from bs4 import BeautifulSoup

##############
# CONSTANTES #
##############
base_url = "http://alize2.finances.gouv.fr/communes/eneuro/"
detail_base_url = base_url + "detail.php"
dep_base_url = base_url + "RDep.php"

# Le titre et l'index des lignes qui nous intéressent
lines = {
    "TOTAL DES PRODUITS DE FONCTIONNEMENT = A":     7,
    "TOTAL DES CHARGES DE FONCTIONNEMENT = B":      11,
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C":    19,
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D":       24
}

# Expression régulière pour récupérer l'ID de la commune dans le href
regex_id = re.compile("'ICOM':'([0-9]*)'")

#############
# FONCTIONS #
#############
def dataByYearAndDep(year, dep):
    for commune in communesByDepartment(dep):
        dataByYearAndDepAndCom(year, dep, commune)

def dataByYearRangeAndDep(r, dep):
    for year in r:
        dataByYearAndDep(year, dep)

def dataByYearRangeAndDepAndCom(r, dep, com):
    for year in r:
        dataByYearAndDepAndCom(year, dep, com)

def dataByYearAndDepAndCom(year_int, dep_int, com_int):
    year = str(year_int)
    dep = str(dep_int).zfill(3)
    com = str(com_int).zfill(3)

    # Construire l'URL où les données sont disponibles
    params = {'type': 'BPS', 'exercice': year, 'dep': dep, 'icom': com}
    url = buildUrl(detail_base_url, params)

    # Parser la réponse, et se concentrer sur la table qui nous intéresse
    tables = soupFromUrl(url).select("table")
    if len(tables) < 3:
        print("No data for parameters:" + str(params))
        return

    extractData(tables[2], com_int, dep_int, year)

# Récupérer seulement l'information demandée
def extractData(table, com_id, dep, year):
    com = table.select('tr')[1].select('td')[1].text
    print('==================================================')
    print("Commune: " + com + " (id: " + str(com_id) + "), year: " + year)

    for key, lineNb in lines.items():
        cells = list(map(cleanCell, cellsInLine(table, lineNb)))
        print(key)
        print("\tEuros par habitant   : " + cells[0])
        print("\tMoyenne de la strate : " + cells[1])

# Récupérer la ligne numéro 'lineNb' de table, cellules 1 et 2 (0 based)
def cellsInLine(table, lineNb):
    return table.select("tr")[lineNb].select("td")[1:3]

# Élagage du contenu de la cellule
def cleanCell(cell):
    return cell.text.replace(u'\xa0', '').replace(' ', '')

# Récupère toutes les communes appartenant à un département
def communesByDepartment(dep_int):
    # On formatte le code du département sur 3 caractères
    dep = str(dep_int).zfill(3)

    data = {'DEP': dep, 'TYPE': 'BPS'}
    result = []

    # Pour chaque initiale
    for lettre in getInitials(dep):
        data['LETTRE'] = lettre

        # Les communes dont le nom commence par 'lettre' ne sont pas disponibles
        # par un simple GET, il faut d'abord poster avec les bons critères, puis
        # parser la réponse
        resp = requests.post(dep_base_url, data = data)
        cols = BeautifulSoup(resp.text, 'html.parser').select("table")[1:]

        # On rassemble les communes des 2 colonnes
        communes = cols[0].select('td')
        communes.extend(cols[1].select('td'))

        # Enfin, on récupère l'ID et on le met à sa place
        for commune in communes:
            match_id = regex_id.search(commune.select('a')[0]['href'])
            result.append(match_id.group(1))

    return result

def getInitials(dep):
    # On navigue sur la page des "communes par département"
    url = buildUrl(dep_base_url, {'type': 'BPS', 'dep': dep})
    table = soupFromUrl(url).find("table")
    return [td.text for td in table.select("td")[3:-1]]


###########
# HELPERS #
###########
def buildUrl(url, params):
    return url + '?' + '&'.join([k + '=' + v for k, v in params.items()])

def soupFromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def printHelp():
    print('usage: exo_dom_lesson02.py -d <department> [-c <commune>]')
    print("\t[-y=<year> | [-s <year-start> [-e <year-end>]]")
    print("\nEx:")
    print("Paris (75), between 2009 and 2013:")
    print("\texo_dom_lesson02.py -d 75 -c 56 -s 2009 -e 2013")
    print("Calvados in 2012:")
    print("\texo_dom_lesson02.py -d 14 -y 2012")

def isInt(s):
    if s is None:
        return True
    try:
        int(s)
        return True
    except ValueError:
        return False

########
# MAIN #
########
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:c:y:s:e:",
                ['departement=', 'commune=','year=','start=','end=','help'])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    com, dep, year, start, end = (None,) * 5

    for o, a in opts:
        if o == '-h':
            printHelp()
            sys.exit()
        elif o == '-d':
            dep = a
        elif o == '-c':
            com = a
        elif o == '-y':
            year = a
        elif o == '-s':
            start = a
        elif o == '-e':
            end = a
        else:
            assert False, 'unhandled exception'

    if dep is None or (year is None and start is None):
        printHelp()
        sys.exit(1)

    if any([not isInt(s) for s in [dep, com, year, start, end]]):
        print("Arguments must be integers")
        sys.exit(1)

    if year:
        if com:
            dataByYearAndDepAndCom(year, dep, com)
        else:
            dataByYearAndDep(year, dep)
    else:
        if not end:
            end = datetime.datetime.now().year
        r = range(int(start), int(end) + 1)
        if com:
            dataByYearRangeAndDepAndCom(r, dep, com)
        else:
            dataByYearRangeAndDep(r, dep)
    print()


if __name__ == '__main__':
    main(sys.argv[1:])
