# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Jean-Michel Ycre
"""

import sys, os, csv, json, xlrd, openpyxl, requests, pytz
import bs4
import pandas as pd
import numpy as np

def getsoup(cat, marque, bout, number):
    url = "http://www.cdiscount.com/search/"+bout+"/"+cat+"+"+marque+".html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword="+cat+"%2B"+marque+"+&page="+str(number)+"&_his_"
    pageweb = requests.get(url)
#    pageweb = requests.get("http://www.cdiscount.com/search/"+bout+"/"+cat+"+"+marque+".html#his_")
    print(pageweb)
    soup = bs4.BeautifulSoup(pageweb.text, 'html.parser')
    return soup

def extract_prices_FromDOM(soup, classnamePt, classnamePd, classnameAPx, classnameNPx):
    col = ['nom_produit', 'nouveau_prix', 'ancien_prix']
    df_prix_liste = pd.DataFrame()
    liste_prod = soup.find_all(class_=classnamePt)
    for produit in liste_prod:
        nom_produit = produit.find(class_ = classnamePd).text
        nouveau_prix = produit.find(class_ = classnameNPx).text
        nouveau_prix = nouveau_prix.replace("€",".")
        nouveau_prix = nouveau_prix.replace(",",".")
        nouveau_prix = float(nouveau_prix)
        if produit.find(class_ = classnameAPx):
            if produit.find(class_ = classnameAPx).text:
                ancien_prix = produit.find(class_ = classnameAPx).text
                ancien_prix = ancien_prix.replace("€",".")
                ancien_prix = ancien_prix.replace(",",".")
                ancien_prix = float(ancien_prix)
            else:
                ancien_prix = nouveau_prix
        else:
            ancien_prix = nouveau_prix
        df_prix_liste = df_prix_liste.append({'nom_produit': nom_produit,
                                              'nouveau_prix': nouveau_prix,
                                              'ancien_prix': ancien_prix}, ignore_index=True)
    return df_prix_liste


def calcul_indicateurs(df):
    df['Rabais (%)'] = (df['nouveau_prix']-df['ancien_prix'])/df['ancien_prix']
    return df['Rabais (%)'].mean()

classe_produit = "prdtBloc"
classe_nom_produit = "prdtBTit"
classe_ancien_prix = "prdtPrSt"
classe_nouveau_prix = "price"

liste_marque = ['lenovo', 'dell', 'acer', 'toshiba']
liste_boutique = ['10']
liste_produits = ['ordinateur']
rabais_marque = {}
produits = {}

for mark in liste_marque:
    rabais = []
    for categ in liste_produits:
        for boutique in liste_boutique:
            for number in range(1,3):
                soup = getsoup(categ, mark, boutique, number)
                df = extract_prices_FromDOM(soup, classe_produit, classe_nom_produit,
                                              classe_ancien_prix, classe_nouveau_prix)
                rabais.append(calcul_indicateurs(df))
            rabais_marque[mark] = np.mean(rabais)
            print("Rabais marque", mark,": ", "%.2f%%" % (rabais_marque[mark]*100))

rabais_max = min(rabais_marque.values())
for key in rabais_marque.keys():
    if rabais_marque[key] == rabais_max:
        marque_max = key

print("\nLa marque dont le rabais moyen est le plus important est : ", marque_max)
print("Ce rabais est de : ", "%.2f%%" % (rabais_max * 100))
