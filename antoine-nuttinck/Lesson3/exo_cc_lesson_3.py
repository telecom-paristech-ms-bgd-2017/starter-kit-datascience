import requests
import numpy as np
from bs4 import BeautifulSoup


def extractPrice(html_code):
    res = html_code.replace(u'</sup>', '') \
            .replace(u'</span>', '') \
            .replace(u'€', '.') \
            .replace(u',', '.')

    if res == '':
        return float(0)
    else:
        return float(res)


def extractDiscounts(soup, classname):
    parent = soup.find_all(class_='prdtBZPrice')
    new_prices = []
    old_prices = []
    for par in parent:
        price_children = par.findChildren(class_='price')
        for pc1 in price_children:
            new_prices.append(extractPrice(pc1.text))
        prdtPrSt_children = par.findChildren(class_='prdtPrSt')
        for pc2 in prdtPrSt_children:
            old_prices.append(extractPrice(pc2.text))

    discounts = [new_prices[i] / old_prices[i] - 1
                 if old_prices[i] != 0 else 0.0
                 for i in range(len(old_prices))]

    return discounts


def computeIndicatorForPage(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    # title = soup.title.text
    discounts = extractDiscounts(soup, 'price')

    return discounts  # np.mean(discounts)


def getMostDiscountedPC():
    marques = ['acer', 'dell']
    incompleted_url = "http://www.cdiscount.com/search/10/ordinateur+"
    url_p2 = ".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm." \
        + "DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search" \
        + "&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX" \
        + "&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm." \
        + "CurrentSelectedNavigationPath=0&page="
    url_end = "&_his_"
    discountPerPage = {}
    MAX_PAGE = 5
    for m in marques:
        discountPerPage[m] = []
        for page in range(1, MAX_PAGE + 1):
            discountPerPage[m].append(
                 computeIndicatorForPage(incompleted_url + m +
                                         url_p2 + str(page) + url_end))

    return discountPerPage

print(getMostDiscountedPC())
