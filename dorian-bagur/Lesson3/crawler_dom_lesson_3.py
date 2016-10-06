import requests
from bs4 import BeautifulSoup


def extractPromotions(soup, className):
    tables = soup.find_all("div", class_=className)
    result = []
    for i, price in enumerate(tables):
        result.append(int(price.find('span').text.replace('\u20ac', '')
                          .replace('%', '')))
    return result


def extractNumberOfArticles(soup, className):
    return len(soup.find_all("div", class_=className))


def extractEco(soup):
    sum = 0
    prices = extractPromotions(soup, 'ecoBlk')
    for price in prices:
        sum = sum + price
    return sum / extractNumberOfArticles(soup, 'prdtBloc')


def getAllMetricsFor(brand):
    # Upload html page
    url = ("http://www.cdiscount.com/search/10/" + brand + ".html"
           )
    print(url)
    result = requests.get(url)
    # Parse it with BeautifulSoup
    soup = BeautifulSoup(result.text, "html.parser")
    # Extract metrics
    return extractEco(soup)


def displayMetrics(brand):
    print("Montant moyen des réductions pour un ordinateur " + brand + ": " +
          str(round(getAllMetricsFor(brand), 1)))

displayMetrics('acer')
displayMetrics('dell')
