Le# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 22:46:56 2016

@author: Stephan
"""

import requests
from bs4 import BeautifulSoup


def getContent(brand, page):
    result = requests.get('http://www.cdiscount.com/search/10/' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=' + brand + '&page=' + str(page) + '&_his_')
    soup = BeautifulSoup(result.text, 'html.parser')
    
    return soup
    
def extractPriceFromDOM(soup):
    metrics = {}   
    percent = 0    
    res_str = soup.find_all(class_="prdtPrSt")
    for element in res_str:
        if element.text != '':
            old_P = element.text.split(',')
            old_Price = int(old_P[0]) + (int(old_P[1]) / 100)  
            new_P = element.parent.parent.parent.find(class_='price').text.split('€')
            new_Price = int(new_P[0]) + (int(new_P[1]) / 100)            
            percent += ((old_Price - new_Price) / old_Price) * 100.
            metrics["reduction"] = percent
            title = soup.title.text
            print('=====')
            print(title)
            print("reduction sur la page = ", str(metrics["reduction"]) + "%")
            print('=====')
            
            return  metrics

def getAllMetricsForAllBrandandPage():
    brands = ['Acer', 'Dell']    
    all_metrics = []
    for brand in brands:
        for page in range(1, 3):
            data = getContent(brand, page)
            metrics = extractPriceFromDOM(data)
            all_metrics.append(metrics)
    
    return all_metrics         
            
results = getAllMetricsForAllBrandandPage()
    

    