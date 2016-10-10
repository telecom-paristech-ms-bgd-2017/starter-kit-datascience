import requests
from bs4 import BeautifulSoup


def extractSource(soup, line):
    tables = soup.body.findAll('table')
    if len(tables) >= 3:
        lineA = tables[2].findAll('tr')[line]
        Ahabit = int(lineA.findAll('td')[1].text.replace("\xa0", "")
                     .replace(" ", ""))
        Amean = int(lineA.findAll('td')[2].text.replace("\xa0", "")
                    .replace(" ", ""))
        return (Ahabit, Amean)


def extractA(soup):
    return extractSource(soup, 7)


def extractB(soup):
    return extractSource(soup, 11)


def extractC(soup):
    return extractSource(soup, 19)


def extractD(soup):
    return extractSource(soup, 24)


def getAllMetricsForCity(city):
    metrics = dict()
    for year in range(2009, 2013):
        # Upload html page
        url = ("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?"
               "icom=" + city + "&dep=075&type=BPS&param=5"
               "&exercice=" + str(year)
               )
        print(url)
        result = requests.get(url)
        # Parse it with BeautifulSoup
        soup = BeautifulSoup(result.text, "html.parser")
        # Extract metrics
        metrics[year] = dict()
        metrics[year]['A'] = extractA(soup)
        metrics[year]['B'] = extractB(soup)
        metrics[year]['C'] = extractC(soup)
        metrics[year]['D'] = extractD(soup)
    return metrics


def displayMetrics(metrics):
    for myear, operations in metrics.items():
        print("-------")
        print(myear)
        print("Opérations    |   Euros par habitant    |    " +
              "Moyenne de la strate")
        for op, col in operations.items():
            if col is not None:
                print(op + "             |          " + str(col[0]) +
                      "           |     " + str(col[1]))
        print()


metrics = getAllMetricsForCity('056')
displayMetrics(metrics)
