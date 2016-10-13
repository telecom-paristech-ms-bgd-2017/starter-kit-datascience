import requests
from bs4 import BeautifulSoup
import numpy as np


def get_url(brand, page_id):
    url_template = "http://www.cdiscount.com/search/10/{0}.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=dell&page={1}&_his_"
    return url_template.format(brand.lower(), str(page_id))

def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


#main script


res = {'asus':[], 'dell':[]}

for page_id in range(1, 10):
    for b in res.keys():
        url = get_url(b, page_id)
        bs = getBeautifulSoupObjectfromUrl(url)
        class_name = 'prdtBloc'
        classes = bs.find_all(class_=class_name)
        for c in classes:
            title = c.findChildren(class_='prdtBTit')[0].text
            category = c.findChildren(class_='prdtBCat')[0].text
            if b.lower() in title.lower() and 'ordinateur' in category.lower():
                prices_old = c.findChildren(class_='prdtPrSt')
                prices_new = c.findChildren(class_='price')
                price_old = -999
                price_new = -999
                try:
                    if len(prices_old) == 1:
                        price_old = float(prices_old[0].text.replace(',', '.'))
                    if len(prices_new) == 1:
                        price_new = float(prices_new[0].text.replace('€', '.'))
                except Exception:
                        continue
                finally:
                    if price_old != -999 and price_new != -999:
                        discount = (price_old - price_new)/price_old
                        res[b].append(discount)
for b in res.keys():
    print("Brand : {0}. Number of items : {1}. Average discount : {2:.0f}%".format(b.upper(), len(res[b]), 100*np.mean(res[b])))


