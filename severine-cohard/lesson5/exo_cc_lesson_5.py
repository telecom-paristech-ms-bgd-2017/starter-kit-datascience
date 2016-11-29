#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:24:15 2016

@author: severine
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from pandas import Series, DataFrame

################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')
################################################################################################
# Returns a soup object from a given url

medicament =  'ibuprofene'
url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
params = {'page': 1
     , 'affliste': 0
     , 'platformId': 1
     ,'affNumero' : 0
     ,'isAlphabet':0
     ,'inClauseSubst':0
     , 'nomSubstances':''
     ,'typeRecherche':0
     , 'choixRecherche':'medicament'
     ,'txtCaracteres': medicament
     , 'radLibelle':2
     ,'txtCaracteresSub':''
     , 'radLibelleSub':4}
result = requests.post(url, data=params)
soup = BeautifulSoup(result.text)

balises = soup.find_all(class_="standart")
names = [x.text for x in balises]
names = Series(names)
names = names.str.strip()
print (names)

reg_string = r'(\d+,?\d*)'
reg = re.compile(reg_string)

res = names.str.findall(reg)
print (res)
