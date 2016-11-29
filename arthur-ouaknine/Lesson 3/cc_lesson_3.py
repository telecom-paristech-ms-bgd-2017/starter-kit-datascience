# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:32:31 2016

@author: arthurouaknine
"""

from bs4 import BeautifulSoup
import requests
import numpy as np


def lookingForChildren(subclass, soupParent):
    listeChildren = []
    for element in soupParent:
        listeChildren.append(element.findChildren(class_=subclass))
    return listeChildren

def cleanList(liste):
    for i in range(len(liste)):
        if liste[i] == []:
            liste[i] = ''
        else:
            liste[i] = liste[i][0].text.replace('</div>', '') \
                .replace(',', '.').replace('€', '.')
            if liste[i] != '':
                liste[i] = float(liste[i])
    return liste

def calculTauxRemiseMoyen(listePrixBase, ListePrixNouveau):
    tauxRemise = []
    for i in range(len(ListePrixNouveau)):
        if listePrixBase[i] == '':
            tauxRemise.append(0.0)
        else:
            tauxRemise.append(
                (listePrixBase[i] - ListePrixNouveau[i])/ListePrixNouveau[i])
    return sum(tauxRemise)/float(len(tauxRemise))



def defineURLs(marque, nbPages):
    urls = []
    for page in range(nbPages+1):
        urls.append('http://www.cdiscount.com/search/10/'+str(marque)+'+ordinateur\
        .html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10 \
        &TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm \
        .SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm \
        .LazyLoading.ProductSheets=False&NavigationForm.CurrentSelected \
        NavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm \
        .SelectedFacets.Index=1&FacetForm.SelectedFacets \
        .Index=2&FacetForm.SelectedFacets.Index=3&FacetForm \
        .SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5 \
        &FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets \
        .Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm \
        .SelectedNavigationPath=&ProductListTechnicalForm \
        .Keyword='+str(marque)+'%2Bordinateur&page='+str(page)+'&_his_')
    return urls


def computeTheMeanOfRate(dicoRate):
    conclusion = {}
    for k,v in dicoRate.items():
        conclusion[k] = np.mean(v)
    return conclusion

def appelEtAffichage():
    tauxDeRemiseMoyen = {}
    marques = ['acer', 'dell']
    nbPages = 5
    for marque in marques:
        tauxDeRemiseMoyen[marque] = []
        listURLs = defineURLs(marque, nbPages)
        for url in listURLs:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            contenuTotal = soup.find_all(class_="prdtBZPrice")
            prixNouveau = lookingForChildren("price",contenuTotal)
            prixBase = lookingForChildren("prdtPrSt",contenuTotal)
            prixBase = cleanList(prixBase)
            prixNouveau = cleanList(prixNouveau)
            tauxDeRemiseMoyen[marque].append(calculTauxRemiseMoyen(prixBase, prixNouveau))
    print(computeTheMeanOfRate(tauxDeRemiseMoyen))

appelEtAffichage()
