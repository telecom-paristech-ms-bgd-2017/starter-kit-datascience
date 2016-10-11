from lxml import html
import requests
from bs4 import BeautifulSoup
import numpy as np 


def countDiscount(brand):
    rabais = []
    for page in range(1, 2):
        url = 'http://www.cdiscount.com/search/10/pc+' + brand + \
            '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=pc%2B' + \
            brand + '&page=' + str(page) + '&_his_'
        page_brand = requests.get(url)
        soup = BeautifulSoup(page_brand.text, 'html.parser')
        lis_prom = dict()
        lis_p = dict()
        for i in range(0, len(soup.find_all(class_="prdtPInfoTC"))):
            lis_p[i] = (soup.find_all(class_="prdtPInfoTC")
                        [i].text.replace(",", "."))

        for j in range(0, len(soup.find_all(class_="prdtPrice"))):
            lis_prom[j] = (soup.find_all(class_="prdtPrice")
                           [j].text.replace("€", "."))

        for j in range(0, len(lis_p)):

            if lis_p[j] == "":
                rabais.append(0)
            else:
                rabais.append((float(lis_p[j]) / float(lis_prom[j])) - 1)
    return rabais 


def compareBrand(brand1,brand2):
	vec_rab1 = countDiscount(brand1)
	vec_rab2 = countDiscount(brand2)
	win_brand = brand1 if np.mean(vec_rab1)>np.mean(vec_rab2) else brand2 
	#On calcule le rabais moyen
	print("Le rabais moyen de sur la marque %s est de %s pourcent" % (brand1,round(np.mean(vec_rab1),2)*100))
	print("Le rabais moyen de sur la marque %s est de %s pourcent" % (brand2,round(np.mean(vec_rab2),2)*100))
	print("La marque qui réalise le plus de rabais est donc : %s" % (win_brand))



compareBrand('asus','dell')
