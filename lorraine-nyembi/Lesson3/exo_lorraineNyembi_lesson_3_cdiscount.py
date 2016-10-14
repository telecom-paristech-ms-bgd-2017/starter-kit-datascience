# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine
"""

import requests
from bs4 import BeautifulSoup

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
      
def extractDataForPage(soup):  
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
      dictRes.update({ _promoPC[index] : _modelePC[index] })  
    
  print (dictRes)

def computeDataFromDOMForPage(url, marque):

  MAX_PAGE = 3
  for page in range(1, MAX_PAGE):
      s = url + str(marque) + '.html#_his_' + str(page)
      print(s)
      results = requests.get(s)
      soup = BeautifulSoup(results.text,'html.parser')
      extractDataForPage(soup)

computeDataFromDOMForPage('http://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-', 'acer')

