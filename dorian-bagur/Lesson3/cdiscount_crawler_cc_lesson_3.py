import requests
from bs4 import BeautifulSoup


def extractSources(soup, className):
    return soup.find_all("div", class_=className)


def extractPromotions(soup):
    result = []
    for i, price in enumerate(extractSources(soup, 'ecoBlk')):
        result.append(int(price.find('span').text.replace('\u20ac', '')
                          .replace('%', '')))
    return result


def extractNumberOfArticles(soup):
    return len(extractSources(soup, 'prdtBloc'))


def computeMeanPromotion(promotions, nb):
    sum = 0
    for pr in promotions:
        sum = sum + pr
    return sum / nb


def getAllMetricsFor(brand):
    # Upload html page
    url = ("http://www.cdiscount.com/search/10/" + brand + ".html"
           )
    print(url)
    result = requests.get(url)
    # Parse it with BeautifulSoup
    soup = BeautifulSoup(result.text, "html.parser")
    # Extract metrics
    return computeMeanPromotion(extractPromotions(soup),
                                extractNumberOfArticles(soup))


def displayMetrics(brand):
    print("Montant moyen des réductions pour un ordinateur " + brand + ": " +
          str(round(getAllMetricsFor(brand), 1)))

displayMetrics('acer')
displayMetrics('dell')
