import requests
from bs4 import BeautifulSoup
import urllib2
import numpy as np
# coding: utf-8

#http://www.cdiscount.com/search/10/acer.html?NavigationForm.CurrentSelectedNavigationPath%3Df%2F1%2F0k
             
def get_url(brand,page):
    return 'http://www.cdiscount.com/search/10/' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=acer&page='+ str(page) + '&_his_'
    
    

def get_dico_discount(url):
    brand = requests.get(url)
    soup = BeautifulSoup(brand.text.encode("utf8").decode('ascii', 'ignore'), 'html.parser')
    original_prices = soup.findAll('div', {"class": "prdtPrSt"})
    discounted_prices = soup.findAll('div', {"class": "prdtPrice"})
    ordis = soup.findAll('div',{"class":"prdtBloc"})
    count = 0
    dico={}
    for ordi in ordis:
        full_price = ordi.find('div',{"class":"prdtBZPrice"})
        #price_bd_span = full_price.find('div',{"class":"prdtPInfoT"}).findChildren()
        #price_ad_span = full_price.find('div',{"class":"prdtPrice"}).findChildren()
        price_bd_span = full_price.find('div',{"class":"prdtPrSt"})
        price_ad_span = full_price.find('span',{"class":"price"})
        count +=1
        price_ad = float(str(price_ad_span).split('>')[1].split('<')[0].replace(',','.'))
        if price_bd_span is None:
            price_bd = price_ad
        elif str(price_bd_span).split('>')[1]=='</div':
            price_bd = price_ad
        else:
            price_bd = str(price_bd_span).split('>')[1]
            if price_bd != '':
                price_bd = float(str(price_bd_span).split('>')[1].split('<')[0].replace(',','.'))
            else:
                price_bd = price_ad
        
        discount = (float(price_ad)-float(price_bd))/float(price_bd)
        dico[count]=discount
        #print price_ad, price_bd,discount
    return dico.values()         
      


acer_discount=[]
dell_discount=[]

for page in range(1,10):
    url = get_url('acer',page)
    acer_discount.append(get_dico_discount(url))
    
for page in range(1,10):
    url = get_url('dell',page)
    dell_discount.append(get_dico_discount(url))    
    
print 'Acer provides an average ' + str(np.mean(acer_discount)*100) + '%' + ' discount'
print 'Dell provides an average ' + str(np.mean(dell_discount)*100) + '%' + ' discount'

    
    
    
