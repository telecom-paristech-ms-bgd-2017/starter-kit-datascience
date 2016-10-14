# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 22:46:56 2016
@author: Stephan
"""


import requests
from bs4 import BeautifulSoup

def MetricsPerYear(year):    
    all_exercice = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year))
    soup_exercice = BeautifulSoup(all_exercice.text,'html.parser')
    return getData(soup_exercice)

def getLineData(soup_exercice,index):
    return soup_exercice.find_all(class_ = "montantpetit G")[index].text.replace('\xa0','') 

#nth-of-type﻿ (Balise 2 et 3 dans le td du tr)
def getData(soup_exercice):
    metrics = {}
    metrics['habitantA'] = getLineData(soup_exercice,1)
    metrics['strateA'] = getLineData(soup_exercice,2)
    metrics['habitantB'] = getLineData(soup_exercice,4)
    metrics['strateB'] = getLineData(soup_exercice,5)
    metrics['habitantC'] = getLineData(soup_exercice,10)
    metrics['strateC'] = getLineData(soup_exercice,11)
    metrics['habitantD'] = getLineData(soup_exercice,13)
    metrics['strateD'] = getLineData(soup_exercice,14)
    
    return metrics
        
def printData(metrics):
    print("Euro par habitant A : " + metrics['habitantA'] + " / Moyenne de la strate A : " + metrics['strateA'])
    print("Euro par habitant B : " + metrics['habitantB'] + " / Moyenne de la strate B : " + metrics['strateB'])
    print("Euro par habitant C : " + metrics['habitantC'] + " / Moyenne de la strate C : " + metrics['strateC'])
    print("Euro par habitant D : " + metrics['habitantD'] + " / Moyenne de la strate D : " + metrics['strateD'])           
    
for year in range(2010,2014):
    metrics = MetricsPerYear(year)
    print("-" + str(year) + "-")
    printData(metrics)