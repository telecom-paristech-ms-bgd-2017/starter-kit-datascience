# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:25:49 2016

@author: Stephan
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

def getContentMain(page, molecule):
    molecules = ["IBUPROFENE"]
    
    result = requests.post("http://base-donnees-publique.medicaments.gouv.fr/index.php#", data=
    {  
   		"page":page,
   		"affliste":0,
   		"affNumero":0,
   		"isAlphabet":0,
   		"inClauseSubst":0,
   		"nomSubstances":"",
   		"typeRecherche":0,
   		"choixRecherche":"medicament",
   		"paginationUsed":0,
   		"txtCaracteres":molecule.lower(),
   		"btnMedic.x":0,
   		"btnMedic.y":0,
   		"btnMedic":"Rechercher",
   		"radLibelle":2,
   		"radLibelleSub":4
    })
    soup = BeautifulSoup(result.text, 'html.parser')
    drogList = soup.find_all(class_="standart")

    return drogList

def extractDataFromDOMMain(soup):
    list = []
    expression = r"IBUPROFENE\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+), ([\w\sé])"
#    name2 = []
#    expression2 = r"^IBUPROFENE?[A-Z]{}"
    res_str = soup.find_all(class_="ResultRowDeno")
    for element in res_str:        
        while re_search(res_str, expression) is None:
            name.append('IBUPROFENE')
#        while re_search(res_str, expression2) is None:
#            name2.append()
    return name            

data = getContentMain()
result = extractDataFromDOMMain(data)