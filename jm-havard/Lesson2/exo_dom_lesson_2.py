# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 19:21:47 2016

@author: havard-macpro
"""
import requests
from bs4 import BeautifulSoup

def extractLikeDislikeFromDOM(soup, classname , position):
    res_str = soup.find_all(class_ = classname)[position].text.replace(u'\xa0','').replace('&nbsp;','').replace(' ','')
    res = int(res_str)
    return res

def computIndicator(url):
    print(url)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    tot_prod_fonctionnement = extractLikeDislikeFromDOM(soup,'montantpetit G',1)
    tot_charges_fonctionnement = extractLikeDislikeFromDOM(soup,'montantpetit G' ,4)
    tot_ressources_invest=extractLikeDislikeFromDOM(soup,'montantpetit G',10)
    tot_emplois_invest =extractLikeDislikeFromDOM(soup,'montantpetit G',14)
    print("=================")    
    print("tot_prod_fonctionnement = ", tot_prod_fonctionnement)
    print("tot_charges_fonctionnement = ", tot_charges_fonctionnement)
    print("tot_ressources_invest = ", tot_ressources_invest)
    print("tot_emplois_invest = ", tot_emplois_invest)
    
    print("=================")    
    
    metrics = {}
    metrics['tot_prod_fonctionnement'] = tot_prod_fonctionnement
    metrics['tot_charges_fonctionnement'] = tot_charges_fonctionnement
    metrics['tot_ressources_invest'] = tot_ressources_invest
    metrics['tot_emplois_invest'] = tot_emplois_invest
       
    return metrics



def getallmetricsparis():
    all_metrics = []
    max_annee=2013
    for i in range(2010, max_annee+1):
        annee=str(i)
        all_metrics = computIndicator('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%s' %annee)        
    
 
    return all_metrics


metrics_paris = getallmetricsparis()


