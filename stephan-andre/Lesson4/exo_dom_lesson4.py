# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:26:10 2016

@author: Stephan
"""

#Renault Zoé

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def getContentMain(region, page):
    result = requests.get("https://www.leboncoin.fr/voitures/offres/" + region + "/?o=" + str(page) + "&brd=Renault&mdl=Zoe")
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup
''' 
    links = []
    list_cars= map(lambda x: 'https:' + x['href'], soup.find_all(class_ = "list_item"))
    for link in list_cars:
        links.append(link)

    result2 = requests.get(link)
    soup2 = BeautifulSoup(result2.text, 'html.parser')
    return soup, soup2 
'''
    


#def extractDataFromDOMMain(soup, soup2):
def extractDataFromDOMMain(soup):  
    
    modele = []
    res_str = soup.find_all(class_="item_title")
    for element in res_str:        
        if 'zen' in str(element).lower():
            modele.append('zen')
        elif 'intens' in str(element).lower():
            modele.append('intens')
        elif 'life' in str(element).lower():
            modele.append('life')
        else:
            modele.append('NA')
    
    pro = []  
    res_str2 = soup.find_all(class_="item_infos")
    for element2 in res_str2:       
        if '(pro)' in str(element2).lower():
            pro.append('pro')   
        else:
            pro.append('NA')
    
    return modele, pro
            
'''    dico = {}
    car_properties = soup2.find_all(class_='property')

    for car_property in car_properties:
        if car_property.text.lower() == 'prix':
            value = car_property.parent.find(class_='value').text.strip()
            regex = re.search('(\d* *\d*),?(\d*)', value)
            if regex == None:
                dico['Prix'] = 'NA'
            else:
                dico['Prix'] = float(regex.group(1).replace(' ',''))
            
    prix = ()
    prix.append(dico.values())
'''            



def DataFrameModelePro(modele, pro):
    df = pd.DataFrame([modele, pro])

    return df
    

region = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']    
for regions in region:
    for page in range(1):
        (data) = getContentMain(regions, page)
        (result1, result2) = extractDataFromDOMMain(data)
        df = DataFrameModelePro(result1, result2) 
#        (data, data1) = getContentMain(regions, page)
#        (result1, result2, result3) = extractDataFromDOMMain(data, data1)
#        df = DataFrameModelePro(result1, result2, result3)         
        print(df)
        df.to_csv("RenaultZoe.csv", index = False)

'''
pattern_year = "[0-9]{4}"
re_year = re.compile(pattern_year)
pattern_km = "[0-9]{1,20}"
re_km = re.compile(pattern_km)
pattern_city = "[A-Z._ %+-]{1,100}"
re_city = re.compile(pattern_city, flags=re.IGNORECASE)
pattern_type = "(zen|life|intens)"
re_type = re.compile(pattern_type, flags = re.IGNORECASE)
pattern_phone = "([+0-9]{11}|[0-9]{10})"
re_phone = re.compile(pattern_phone)


'''