# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import urllib

#http://www.cdiscount.com/search/10/dell.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=dell&&_his_

#url2 = requests.get('http://www.cdiscount.com/search/10/dell.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=dell&&_his_')


# reste à faire le parcour par pages
for marque in ('dell','acer'):
    url = requests.get('http://www.cdiscount.com/search/10/' + marque +'.html#_his_')
    print('http://www.cdiscount.com/search/10/' + marque +'.html#_his_')
    # url = requests.get("http://www.cdiscount.com/ProductListUC.mvc/UpdateJsonPage?isPreloaded=false&page=5")
    soup = BeautifulSoup(url.text, 'html.parser')

  #print soup.prettify()[0:1000]
    class_name_product_info = 'prdtBZPrice' # classe pere des prix 
    class_name_origin_price = "prdtPrSt" # prix d'origine
    class_name_current_price = "price"  # prix courant

  #all_origin_price = soup.find_all(class_=class_name_origin_price)

    all_product_info = soup.find_all(class_=class_name_product_info)
    k = 0
    sum_origin_price = 0
    sum_current_price = 0
    for el in all_product_info: # pour tous les produits
      #print(el.text)
      current_price = el.findChildren(class_=class_name_current_price)
      origin_price = el.findChildren(class_=class_name_origin_price)
      #print("k" + str(k))
    
      if origin_price != [] and origin_price[0] != "" and  origin_price[0].text.replace(' ','') !="":   # la balise origine peut ne pas exister ou etre list_video_artist donc on la saute
        #print(origin_price[0])
        #print ("current=" +current_price[0].text)
        #print("origin=" +origin_price[0].text.replace(',','.'))
        #print ("current=" +current_price[0].text.replace(u'€', '.'))
        sum_origin_price += float(origin_price[0].text.replace(',','.'))
        sum_current_price += float(current_price[0].text.replace(u'€', '.'))

      k += 1

    print ("sum current price ", round(sum_current_price))
    print ("sum origin price ", round(sum_origin_price))
    print("ratio en %  sur marque ", marque)
    #print (round(sum_current_price/sum_origin_price*100))
    print (round((sum_origin_price-sum_current_price)/sum_current_price*100))
