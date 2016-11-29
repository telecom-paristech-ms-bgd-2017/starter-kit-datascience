import requests
from bs4 import BeautifulSoup

# =========================================================
#
# Quel est le plus gros remiseur entre Asus et Acer ???
#
# =========================================================


def extractPrice(soup):
    txr = 0
    TxR = 0
    for el in soup.find_all(class_='prdtBZPrice'):
        if len(el.find_all(class_='price')) > 0:
            priceNew = el.find_all(class_='price')[0].text.replace(u'\xa0', '').replace(' ', '').replace(',', '.').replace('€', '.')
            if len(el.find_all(class_='prdtPrSt')) > 0:
                priceOld = el.find_all(class_='prdtPrSt')[0].text.replace(u'\xa0', '').replace(' ', '').replace(',', '.').replace('€', '.')
            else:
                priceOld = '0'
        if priceNew != '' and priceOld != '' and float(priceOld) > 0:
            txr = (float(priceOld) - float(priceNew)) / float(priceOld)
        else:
            txr = 0
        TxR += txr
    return TxR/len(soup.find_all(class_='price'))

def comparateur(pageMax):
    marque = {'acer': 0, 'asus': 0, 'dell': 0, 'mac': 0}
    page = range(1, pageMax + 1)
    for el in marque.keys():
        TxP = 0
        for el2 in page:
            result = requests.get('http://www.cdiscount.com/search/10/ordinateur+' + str(el) + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateur%2Basus&page=' + str(el2) + '&_his_').text
            soup = BeautifulSoup(result, 'html.parser')
            TxP += extractPrice(soup)
            marque[el] = round(100 * TxP / len(page), 2)
    print(marque)


comparateur(10)