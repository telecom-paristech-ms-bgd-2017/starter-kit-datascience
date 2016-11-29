import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def extractPrice(html_code):

    if html_code:
        res = html_code[0].text.replace(u'</sup>', '') \
            .replace(u'</span>', '') \
            .replace(u'€', '.') \
            .replace(u',', '.')

        if (res == ''):
            return float(0)
        else:
            return float(res)
    else:
        return float(0)


def extractDiscounts(soup):
    parent = soup.find_all(class_='prdtBZPrice')
    discounts = []
    for par in parent:
        new_price = extractPrice(par.findChildren(class_='price'))
        old_price = extractPrice(par.findChildren(class_='prdtPrSt'))
        if new_price > 200.0:  # eliminer tout ce qui ne peut pas être un ordi
            if old_price == 0:
                discounts.append(0.0)
            else:
                discounts.append(new_price / old_price - 1)

    return discounts


def computeIndicatorForPage(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    discounts = extractDiscounts(soup)

    return discounts


def getPCDiscounts(brds):

    incompleted_url = "http://www.cdiscount.com/search/10/ordinateur+"
    url_p2 = ".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm." \
        + "DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search" \
        + "&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX" \
        + "&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm." \
        + "CurrentSelectedNavigationPath=0&page="
    url_end = "&_his_"
    discountPerBrand = {}
    MAX_PAGE = 5
    for m in brds:
        discountPerBrand[m] = []
        for page in range(1, MAX_PAGE + 1):
            discountPerBrand[m].extend(
                computeIndicatorForPage(incompleted_url + m + url_p2 +
                                        str(page) + url_end))

    return discountPerBrand


results = getPCDiscounts(['acer', 'dell'])
BestDiscounts = pd.DataFrame()
for brand, discount in results.items():
    BestDiscounts[brand] = pd.Series([np.mean(discount), np.min(discount)],
                                     index=['mean', 'max'])

print("Le tableau ci-dessous résume les réductions proposées par chacune" +
      " des marques :")
print(BestDiscounts)
