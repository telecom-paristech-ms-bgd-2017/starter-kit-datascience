# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def extractPromo(_promoPC):
    #get from "<span>" and before "</span>"      
   jstart = _promoPC.find(str("<span>"))
   jstop = _promoPC.find(str("</span>"))
   res = _promoPC[(jstart + len(str("<span>"))):jstop]
   return res

def extractModele(_modelePC):
    #get from "prdtBTit>" and before "</div"    
   jstart = _modelePC.find(str('<div class="prdtBTit">'))
   jstop = _modelePC.find(str("</div"))
   res = _modelePC[(jstart + len(str('<div class="prdtBTit">'))):jstop]
   return res
      
def extractDataForPage(soup, marque):  
  li_all = []
  class_prdtBloc = []
  class_jsQs = []
  _promoPC = []
  _modelePC = []
  dictRes = {}
  
  

  li_all = soup.find_all('li')
  for li in li_all:
      class_prdtBloc.extend(li.find_all(class_='prdtBloc'))
    
  for _class in class_prdtBloc:
      class_jsQs.extend(_class.find_all(class_='jsQs'))

  for _class in class_jsQs:
      _promoPC.append(str(_class.find_all(class_='ecoBlk')))
      _modelePC.append(str(_class.find_all(class_='prdtBTit')))

  for index, object in enumerate(_promoPC):
      _promoPC[index] = extractPromo(object)
    
  for index, object in enumerate(_modelePC):
      _modelePC[index] = extractModele(object)
      dictRes.update({ _modelePC[index] : _promoPC[index] })  
    
 # print (dictRes)
  df = pd.DataFrame({"Modele de PC":  _modelePC, "Marque" : marque.upper(), "Promo en €" : _promoPC})
  
  #print (df)
  #print("\n\n")
  return df

#http://pandas.pydata.org/pandas-docs/stable/merging.html
def computeDataFromDOMForPage(marque):

  MAX_PAGE = 15
  frames = []
  finalDf = pd.DataFrame()
  for page in range(MAX_PAGE):
      s = "http://www.cdiscount.com/search/10/ordinateur+portable.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets%5B0%5D=0&FacetForm.SelectedFacets%5B0%5D=1&FacetForm.SelectedFacets%5B0%5D=2&FacetForm.SelectedFacets%5B0%5D=3&FacetForm.SelectedFacets%5B0%5D=f%2F6%2F" \
           + marque \
           + "&FacetForm.SelectedFacets%5B0%5D=4&FacetForm.SelectedFacets%5B0%5D=5&FacetForm.SelectedFacets%5B0%5D=6&FacetForm.SelectedFacets%5B0%5D=7&FacetForm.SelectedFacets%5B0%5D=8&FacetForm.SelectedFacets%5B0%5D=9&FacetForm.SelectedFacets%5B0%5D=10&FacetForm.SelectedFacets%5B0%5D=11&FacetForm.SelectedFacets%5B0%5D=12&FacetForm.SelectedFacets%5B0%5D=13&FacetForm.SelectedFacets%5B0%5D=14&FacetForm.SelectedFacets%5B0%5D=15&FacetForm.SelectedFacets%5B0%5D=16&FacetForm.SelectedFacets%5B0%5D=17&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=ordinateur%2Bportable&page=" \
           + str(page)\
           + "&_his_"
      
      try:
          results = requests.get(s)
          soup = BeautifulSoup(results.text,'html.parser')
          print("Extraction: " + marque + " page " + str(page))
          frames.append (extractDataForPage(soup, marque))
          
          finalDf = pd.concat(frames)
          finalDf["Promo en €"] = finalDf["Promo en €"].str.replace('€', '')
          finalDf["Modele de PC"] = finalDf["Modele de PC"].str.replace(',', ';')
          finalDf["Promo en €"] = pd.to_numeric(finalDf["Promo en €"], errors='coerce')
          finalDf = finalDf.fillna(0.0)
          
      except KeyError:
          print("La page " + page + " intouvable pour " + marque.upper())
  return finalDf  
  
df_hp = computeDataFromDOMForPage("hp")
df_acer = computeDataFromDOMForPage("acer")

dff = pd.concat([df_hp, df_acer])
dff = dff.set_index(np.arange(dff.shape[0]))
dff.to_csv('reductions_de_prix_et _metrics_PC_ACER_vs_HP_CDISCOUNT.csv')
print(dff)

# FAIRE METRICS AVEC LA dff