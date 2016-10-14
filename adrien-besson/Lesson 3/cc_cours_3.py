# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re

brands = ['dell','acer']
pages = [1,2,3]

def loadHtml(brand,page):
	url = "http://www.cdiscount.com/search/10/" + brand + ".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=" + brand + "&page=" + str(page) + "&_his_"
	r = requests.get(url)
	return BeautifulSoup(r.text,"html.parser")

def getDatasOnPage(soup):
	dico = {}
	dataPage = soup.find_all(class_="prdtPrSt")
	priceOnPage = len(soup.find_all(class_="price"))

	addForPage = 0
	for element in dataPage:
		initialPriceTxt = element.text
		newPriceTxt = element.parent.parent.parent.find_all(class_="price")[0].text

		if newPriceTxt != "" and initialPriceTxt != "":
			m = re.search('(\d*)(,|€)(\d*)',newPriceTxt)
			newPrice = int(m.group(1)) + int(m.group(3))/100
			m = re.search('(\d*)(,|€)(\d*)',initialPriceTxt)
			initialPrice = int(m.group(1)) + int(m.group(3))/100

			pourcentage = ((initialPrice - newPrice) / initialPrice) * 100.
			addForPage += pourcentage

	dico['SumOfReductions'] = addForPage
	dico['NumberOfPriceOnPage'] = priceOnPage

	return dico

def getSummaryForPage(brand, page):
	soup = loadHtml(brand,page)
	return getDatasOnPage(soup)

def reductionsForBrandAndPages(brand):
	totalPriceOnPages = 0
	totalReductionsOnPages = 0
	for page in pages:
		dico = getSummaryForPage(brand,page)
		totalPriceOnPages += dico['NumberOfPriceOnPage']
		totalReductionsOnPages += dico['SumOfReductions']

	return totalReductionsOnPages / totalPriceOnPages

def comparaisonOnReductions():
	comparaisons = []
	for brand in brands:
		dico = {}
		dico['Marque'] = brand
		dico['Reduction_moyenne'] = reductionsForBrandAndPages(brand)
		comparaisons.append(dico)

	for comparaison in comparaisons:
		print("Marque : " + comparaison['Marque'])
		print("Reduction moyenne : " + str(comparaison['Reduction_moyenne']))
		print("")

comparaisonOnReductions()