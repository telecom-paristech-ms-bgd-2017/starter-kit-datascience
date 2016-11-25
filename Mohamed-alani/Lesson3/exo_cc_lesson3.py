import requests
from bs4 import BeautifulSoup
import numpy as np
import sys

URLBASE = "http://www.cdiscount.com/search/10/ordinateur+"

def loadHTML(URL):
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')

def getURL(marque, page):
    return loadHTML(URLBASE+marque+".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnpagesType=Search&TechnicalForm.SellerId=&TechnicalForm.pagesType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=ordinateur%2B"+marque+"&pages="+str(page)+"&_his_#_his_")

def analyserPrix(marque,pages):
    promoPC = []
    for page in range(pages) :
        soup_pc= getURL(marque,page+1)


        produits = soup_pc.findAll("div", {"class": "prdtBloc"})

        allOldPrice = []
        allNewPrice = []
        promo = []
        for pc in produits :
            try:
                oldPrice = pc.find("div", {"class": "prdtPrSt"})
                newPrice = pc.find("div", {"class": "prdtPrice"})
                if oldPrice.text !='':
                    old = float(oldPrice.text.replace(",","."))
                    new = float(newPrice.text.replace("€","."))
                allOldPrice.append(old)
                allNewPrice.append(new)
            except Exception as e:
                continue
            promoPC.append(100-new*100/old)

        # print(allNewPrice)
        # print(allOldPrice)
    return(np.mean(promoPC))

def remises(pages):
    print("Remise acer : "+str(analyserPrix("acer", pages)) + "   ||   Remise dell : "+str(analyserPrix("dell", pages)))

remises(20)
# 1 load URL en fonction d'une marque
