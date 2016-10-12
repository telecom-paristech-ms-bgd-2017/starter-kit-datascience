import requests
import numpy as np
from bs4 import BeautifulSoup


def extractPrice(html_code):
    res = html_code.replace(u'</sup>', '') \
    .replace(u'</span>', '') \
    .replace(u'€','.') \
    .replace(u',','.')
    
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
    
    discounts = [new_prices[i] / old_prices[i] - 1 \
                 if old_prices[i]!=0 else 0.0 \
                 for i in range(len(old_prices))]
        
    return discounts


def computeIndicatorForPage(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    # title = soup.title.text
    discounts = extractDiscounts(soup, 'price')
    # result = (real_prices/old_prices-1)
    return np.mean(discounts)


def getMostDiscountedPC():
    marques = ['acer', 'dell']
    incompleted_url = "http://www.cdiscount.com/search/10/ordinateur+"
    url_part2 = ".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm." \
    + "DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search" \
    + "&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX" \
    + "&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm." \
    + "CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0" \
    + "&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2" \
    + "&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4" \
    + "&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6" \
    + "&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8" \
    + "&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10" \
    + "&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12" \
    + "&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=" \
    + "&FacetForm.SelectedFacets.Index=14&SortForm.SelectedNavigationPath=&" \
    + "ProductListTechnicalForm.Keyword=ordinateur%2Bacer&page="
    url_end = "&_his_"
    discountPerPage = {}
    MAX_PAGE = 10
    for m in marques:
        discountPerPage[m] = []
        for page in range(1, MAX_PAGE + 1):
            discountPerPage[m].append(computeIndicatorForPage(incompleted_url + m + url_part2 + str(page) + url_end))

    return discountPerPage

print(getMostDiscountedPC())
# print(computeIndicatorForPage('http://www.cdiscount.com/search/10/ordinateur+acer.html#_his_'))