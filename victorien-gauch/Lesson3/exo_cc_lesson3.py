import requests
from bs4 import BeautifulSoup
import re

listMarques = ['dell','acer','apple']
pages = [1,2]

def getData(marque,page):

	url = requests.get('http://www.cdiscount.com/search/10/' + marque + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=' + marque + '&page=' + str(page) + '&_his_')
	soup = BeautifulSoup(url.text,'html.parser')
	return soup

def parcourirPage(soup):
	pourcentage = 0
	data = soup.find_all(class_="prdtPrSt")

	for el in data:
		
		if el.text != '':
			oldPrice = el.text.split(',')
			oldPrice = int(oldPrice[0]) + (int(oldPrice[1]) / 100)

			newPrice = el.parent.parent.parent.find(class_='price').text.split('€')
			newPrice = int(newPrice[0]) + (int(newPrice[1]) / 100)
			pourcentage += ((oldPrice - newPrice) / oldPrice) * 100.

	return pourcentage / len(soup.find_all(class_="price"))


def parcourirPlusieursPages(marques,pages):
	dico = {}

	for marque in marques:
		p = 0
		for page in pages:
			data = getData(marque,page)
			p += parcourirPage(data)
			p = p / len(pages)
		
		dico[marque] = p

	return dico

results = parcourirPlusieursPages(listMarques,pages)

print(results)



	
	








	





