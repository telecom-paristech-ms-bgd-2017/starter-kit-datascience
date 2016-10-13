# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 22:46:56 2016

@author: Stephan
"""

import requests
from bs4 import BeautifulSoup


def getContent(brand,page):
    result = requests.get('http://www.cdiscount.com/search/10/' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=' + brand + '&page=' + str(page) + '&_his_')
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup



#print(soup)

def extractReductionFromDOM(soup):
    res_str = soup.find_all(class_="ecoBlk").text.replace(u'\xa0','').replace('€','')
    res = int(res_str)
    return res
    
def extractOldPriceFromDOM(soup):
    res_str = soup.find_all(class_="prdtPrSt")
    
    for el in res_str:
        if el.text != '':
            oldP = el.text.split(',')
            oldP = int(oldP[0]) + (int(oldP[1]) / 100)
            
    return res_str

soup = getContent('acer',1)
res = extractOldPriceFromDOM(soup)

def computeIndicatorForPage1(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    reduction = extractReductionFromDOM(soup)
    #.replace('\xa0','') 
    old_price = extractOldPriceFromDOM(soup, 0)
    #.replace('\xa0','') 
    indicator = (1 - (old_price - reduction ) / old_price) * 100

    print('=====')
    print("reduction", reduction)
    print("old_price", old_price)
    print("%reduction", indicator)
    print('=====')
    metrics = {}
    metrics['reduction'] = reduction
    metrics['old_price'] = old_price
    metrics['indicator'] = indicator
    return  metrics

def getAllMetricsForABrand():
    all_metrics = []
    for brand in ['Acer', 'Dell']:
        metrics = computeIndicatorForPage1("http://www.cdiscount.com/search/10/ordinateur+de+bureau+" + brand + ".html#_his_")
        all_metrics.append(metrics)
    return all_metrics
    


'''


def MetricsPerPC(Brand):    
    url = requests.get("http://www.cdiscount.com/search/10/ordinateur+de+bureau+" + Brand + ".html#_his_")
    soup = BeautifulSoup(url.text,'html.parser')
    return getData(soup)

def getLineData(soup):
    numbers = soup.find_all(class_ = "prdtPrSt")[0].text.replace('\xa0','') 
    return numbers  
    for inputs in numbers:
        if inputs.text != "":
            Price = inputs.text
            Price = int(Price)
            Discount_price = inputs.parent.parent.parent.find(class_='price')[0].text.replace('\xa0','') 
            Discount_price = int(Discount_price)            
            return round(Discount_price / Price)
            
def getData(soup):
    n = len(soup.find_all(class_="prdtPrSt"))
    metrics = {}    
    for i in range(1,n):
        metrics[i] = getLineData(soup)
        return metrics
      
def printDiscount(metrics):
    print(" discount per all PC : " + str(metrics))
    
for Brand in ['Acer', 'Dell']:
    metrics = MetricsPerPC(Brand)
    print("-" + str(Brand) + "-")
    printDiscount(metrics)
    '''
