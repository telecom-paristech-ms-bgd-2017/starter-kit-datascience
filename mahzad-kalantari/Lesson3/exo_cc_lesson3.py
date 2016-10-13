import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#url = http://www.cdiscount.com/search/10/dell.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=dell&page=2&_his_
#http://www.cdiscount.com/search/10/dell.html#_his_




def findPromo(brand,page):
    url =  'http://www.cdiscount.com/search/10/' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=acer&page='+ str(page) + '&_his_'

    r3= requests.get(url)
    soup = BeautifulSoup(r3.text, 'html.parser')
    cells = soup.findAll('div', {"class" : "prdtBZPrice"})
    listData=[]

    for cell in cells:
        promo = cell.find('span', { "class" : 'price'})
        prix  = cell.find('div', { "class" : 'prdtPrSt'})
        #print("prix", prix)
        #print("promo",promo)

        if not promo is None and not prix is None and prix.text != '':
            pr = prix.text.replace('€', ',')

            prom = promo.text.replace('€', ',')

            moyenne = ((float(pr.replace(',','.'))-float(prom.replace(',','.')))/float(pr.replace(',','.')))*100
            listData.append(moyenne)

    return(np.mean(listData))

# MAIN
promo = findPromo('dell', '1')
print("Promo Dell en pourcentage", promo)

promo = findPromo('acer', '1')
print("Promo Acer en pourcentage ",promo)
