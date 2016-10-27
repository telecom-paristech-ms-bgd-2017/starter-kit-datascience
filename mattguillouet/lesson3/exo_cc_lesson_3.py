import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import ipdb


def allDiscounts(brand, nbPage):

    urlbase = 'http://www.cdiscount.com/search/10/{0}.html'

    listDisount = []
    for page in range(1, nbPage + 1):
        print('process page {0}/{1} for brand {2}'.format(page, nbPage, brand),
        end='\r')
        getDict = {'TechnicalForm.SiteMapNodeId': '0',
            'TechnicalForm.DepartmentId': '10',
            'hdnPageType': 'Search', 'TechnicalForm.PageType': 'SEARCH_AJAX',
            'TechnicalForm.LazyLoading.ProductSheets': 'False',
            'NavigationForm.CurrentSelectedNavigationPath': '0',
            'ProductListTechnicalForm.Keyword': brand, 'page': page}

        r = requests.get(urlbase.format(brand), params=getDict)
        soup = BeautifulSoup(r.content, 'html.parser')

        products = soup.find_all(class_='prdtBloc')
        for prod in products:
            price = float(prod.find(class_='prdtPrice').text.replace('€', '.'))
            price_base = prod.find(class_='prdtPrSt')
            if price_base is not None:
                try:
                    price_base = float(price_base.text.replace(',', '.'))
                    listDisount.append({'price': price, 'price_base': price_base})
                except:
                    listDisount.append({'price': price, 'price_base': price})

            else:
                listDisount.append({'price': price, 'price_base': price})

    print()
    return listDisount


def processDataFrame(dataF):
    dataF['discount'] = dataF['price_base'] - dataF['price']
    dataF['discount_percent'] = 100 * dataF['discount'] / dataF['price_base']


def indicator(dataF):
    return dataF['discount_percent'].mean()


nbPage = 5

dellDisc = allDiscounts('dell', nbPage)
acerDisc = allDiscounts('acer', nbPage)

dellDiscPd = pd.DataFrame(dellDisc)
acerDiscPd = pd.DataFrame(acerDisc)

processDataFrame(dellDiscPd)
processDataFrame(acerDiscPd)

print()
print('discount indicator dell: {:.3f}'.format(indicator(dellDiscPd)))
print('discount indicator acer: {:.3f}'.format(indicator(acerDiscPd)))


'''
'FacetForm.SelectedFacets.Index': 0,
'FacetForm.SelectedFacets.Index': 1,
'FacetForm.SelectedFacets.Index': 2,
'FacetForm.SelectedFacets.Index': 3,
'FacetForm.SelectedFacets.Index': 4,
'FacetForm.SelectedFacets.Index': 5,
'FacetForm.SelectedFacets.Index': 6,
'FacetForm.SelectedFacets.Index': 7,
'FacetForm.SelectedFacets.Index': 8}
'''

'''
TechnicalForm.SiteMapNodeId=0&
TechnicalForm.DepartmentId=10&
TechnicalForm.ProductId=&
hdnPageType=Search&
TechnicalForm.SellerId=&
TechnicalForm.PageType=SEARCH_AJAX&
TechnicalForm.LazyLoading.ProductSheets=False&
NavigationForm.CurrentSelectedNavigationPath=0&
FacetForm.SelectedFacets.Index=0&
FacetForm.SelectedFacets.Index=1&
FacetForm.SelectedFacets.Index=2&
FacetForm.SelectedFacets.Index=3&
FacetForm.SelectedFacets.Index=4&
acetForm.SelectedFacets.Index=5&
FacetForm.SelectedFacets.Index=6&
FacetForm.SelectedFacets.Index=7&
FacetForm.SelectedFacets.Index=8&
GeolocForm.ConfirmedGeolocAddress=&
SortForm.SelectedNavigationPath=&
ProductListTechnicalForm.Keyword=dell&
page=1&_his_#_his_
'''

