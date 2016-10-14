
# coding: utf-8

# In[92]:


"""
Created on Mon Oct 10 20:02:37 2016

@author: laura
"""

import urllib.request
from bs4 import BeautifulSoup


#url_acer='http://www.cdiscount.com/search/10/pc+portables+acer.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=f%2F6%2Facer&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=pc%2Bportables%2Bacer&&_his_'
#url_dell='http://www.cdiscount.com/search/10/pc+portables.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets%5B1%5D=f%2F6%2Fdell&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=pc%2Bportables&&_his_'

#read file
url = "http://www.cdiscount.com/search/10/acer+pc+portable.html#_his_"
s_acer = urllib.request.urlopen(url).read()

def marque(m,page):
    if m=="acer":
        return 'http://www.cdiscount.com/search/10/pc+portables+acer.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k%2F0k%7C0k0c%7C0k0c01&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets%5B3%5D=f%2F6%2Facer&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=14&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=pc%2Bportables%2Bacer&page='+str(page)+'&_his_'
    if m=="dell":
        return 'http://www.cdiscount.com/search/10/pc+portables.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets%5B3%5D=f%2F6%2Fdell&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&GeolocForm.ConfirmedGeolocAddress=&FacetForm.SelectedFacets.Index=15&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=pc%2Bportables&page='+str(page)+'&_his_'
    

    

def analyse(url):
    #read web page
    s = urllib.request.urlopen(url).read()
    #make soup
    soup = BeautifulSoup(s,"html.parser")

    #nb de produit par page
    nb_prod=len(soup.find_all("div",class_="prdtPrice"))

    #balise avec tous les produits
    a = soup.find_all("div", class_="prdtBloc")
    taux=0
    for i in range(nb_prod):
        if (a[i].find_all("div",class_="ecoBlk"))== []:
            #pas de reduc donc taux de reduc nul
            taux=taux+0. 
        else:
            #réduction
            prix_i =(a[i].find_all("div",class_="prdtPrSt")[0].text)
            sigle=prix_i.find("€")
            initial= float(prix_i.replace(",","."))

            reduc  =(a[i].find_all("div",class_="ecoBlk")[0].text)
            sigle = reduc.find("€")
            promo=int(reduc[:sigle])
            taux=taux+promo/initial
    taux=taux/nb_prod
    return taux
    
#analyse(marque("acer",10))
#analyse(marque("dell",10))


def Ratio_all(nb_p):
    total_acer=0
    total_dell=0
    print("Calcul du meilleur taux de promo sur",nb_p,"pages")
    for i in range(1,nb_p+1): 
        total_acer+=analyse(marque("acer",i))
        total_dell+=analyse(marque("dell",i))
        print("---page",i,"---")
        print("acer:",analyse(marque("acer",i)))
        print("dell:",analyse(marque("dell",i)))
        
    if(total_acer>total_dell):
        print("ACER A DE MEILLEUR PROMOs")
    else:
        print("DELL A DE MEILLEUR PROMOs")

Ratio_all(9)
#pas d'ordi après la page 9, il y a d'autres produits


# In[ ]:



