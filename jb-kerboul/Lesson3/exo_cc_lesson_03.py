
import requests
from bs4 import BeautifulSoup as bs4
import numpy as np


def getSoupFromUrl(url, brand, params, nbPages):
    print('retrieving page ' + str(params['page']))

    result = requests.get(url, params)
    soup = bs4(result.text, 'html.parser')
    if nbPages == -1:
        li = soup.find('div', id='pager').find_all('li')
        nbPages = int(li[-1].text)
    params['page'] += 1
    print(
        'retrieved page ' + str(params['page']) + ' on ' +
        str(nbPages) + 'pages')
    return soup, nbPages, params


def computeFromSoup(soup):
    print('processing')
    oldPrice = list()
    newPrice = list()
    objToSell = soup.find_all(class_='prdtBZPrice')
    for ii in objToSell:
        temp = ii.find(class_='prdtPrSt')
        if temp is not None:
            if temp.text != '':
                temp2 = ii.find(class_='price')
                oldPrice.append(float(temp.text.replace(',', '.')))
                newPrice.append(float(temp2.text.replace('€', '.')))

    newPrice = np.asarray(newPrice)
    oldPrice = np.asarray(oldPrice)
    return oldPrice, newPrice


def loopThroughBrands(Brands, dicoPrix):
    for bb in Brands:
        dicoPrix[bb] = {}
        dicoPrix[bb]['oldPrice'] = np.array([])
        dicoPrix[bb]['newPrice'] = np.array([])

        url = baseUrl.replace('<brand>', bb)
        params = {'page': 1}
        nbPages = -1

        while params['page'] != nbPages:
            print(str(params['page'] != nbPages))
            print('boucle ' + str(params['page']) + ' ' + str(nbPages))
            soup, nbPages, params = getSoupFromUrl(url, bb, params, nbPages)
            oldPrice, newPrice = computeFromSoup(soup)
            dicoPrix[bb]['oldPrice'] = np.append(
                dicoPrix[bb]['oldPrice'], oldPrice)
            dicoPrix[bb]['newPrice'] = np.append(
                dicoPrix[bb]['newPrice'], newPrice)

        dicoPrix[bb]['promo'] = (np.mean((dicoPrix[bb]['oldPrice'] -
                                          dicoPrix[bb]['newPrice']) * 100 /
                                         dicoPrix[bb]['oldPrice']))
    return dicoPrix


def printRes(Brands, dicoPrix):

    for ii in Brands:
        print(str(ii) + ' remise moyenne de ' + str(dicoPrix[ii]['promo']) +
              '%\n sur ' + str(len(dicoPrix[ii]['oldPrice'])) + ' articles')


# Bas d'adresse URL
# BaseUrl = 'http://www.cdiscount.com/search/10/ordinateur+portable+<brand>.html'

baseUrl = ("http://www.cdiscount.com/search/10/ordinateur+portable+<brand>.html?\
TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId\
=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&\
TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath\
=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index\
=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index\
=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index\
=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index\
=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index\
=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort\
=PERTINENCE&ProductListTechnicalForm.Keyword=ordinateur%2Bportable%2B<brand>&&_his_")


Brands = ['acer', 'dell']
dicoPrix = loopThroughBrands(Brands, {})
printRes(Brands, dicoPrix)
