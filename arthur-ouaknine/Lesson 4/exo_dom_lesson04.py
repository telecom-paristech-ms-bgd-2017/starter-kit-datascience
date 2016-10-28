# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:42:08 2016

@author: arthurouaknine
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re


# url = 'https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&q=Renault%20Zo%E9&parrot=0'
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')

modeleDico = {'version':'NA', 'annee':'NA', 'km':'NA', 'prix':'NA'}


def getLiens(urls, classe):
    liens = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        liens += map(lambda x: 'http:'+x['href'], soup.find_all(class_=classe))
    return liens


def getPageURL(pages,regions):
    urls = []
    for region in regions:
        for page in range(pages+1):
            urls.append('https://www.leboncoin.fr/voitures/offres/'+str(region)+'/?o='+str(page)+'&q=Renault%20Zo%E9')
    return urls


URLParVoiture = 'https://www.leboncoin.fr/voitures/1032643293.htm?ca=12_s'
reqParVoiture = requests.get(URLParVoiture)
soupParVoiture = BeautifulSoup(reqParVoiture.text, 'html.parser')

# SANS REGEX

def collectDataPourUneVoiture(soupParVoiture):
    modeleDico = {'version': 'NA', 'annee': 'NA', 'km': 'NA', 'prix': 'NA', 'typevendeur': 'NA'}
    title = soupParVoiture.find_all('h1')[0].text.replace('\xa0', '').replace('\n', '').replace('\t', '').strip().upper()
    if 'ZEN' in title:
        modeleDico['version'] = 'ZEN'
    elif 'LIFE' in title:
        modeleDico['version'] = 'LIFE'
    elif 'INTENS' in title:
        modeleDico['version'] = 'INTENS'
    modeleDico['prix'] = int(soupParVoiture.find_all(class_='item_price clearfix')[0]['content'])
    caracteristiquesParVoitures = soupParVoiture.find_all('h2')
    for element in caracteristiquesParVoitures:
        if element.find(class_='property').text.replace('\xa0','') == 'Kilométrage':
            modeleDico['km'] = int(element.find(class_='value').text.replace('\xa0', '').replace('KM', '').replace(' ', ''))
        if element.find(class_='property').text.replace('\xa0', '') == 'Année-modèle':
            modeleDico['annee'] = int(element.find(class_='value').text.replace('\xa0', ''))
    descriptionPro = soupParVoiture.find_all(class_='ispro')
    if descriptionPro != [] and 'Pro' in descriptionPro[0].text.replace('\xa0', '').upper():
        modeleDico['typevendeur'] = 'professionel'
    else:
        modeleDico['typevendeur'] = 'particulier'
    return modeleDico


def collectDataPourUnePage(links):
    allData = []
    for link in links:
        reqParVoiture = requests.get(link)
        soupParVoiture = BeautifulSoup(reqParVoiture.text, 'html.parser')
        allData.append(collectDataPourUneVoiture(soupParVoiture))
    return allData


def getCleanData(allData):
    return pd.DataFrame(allData)


def importData(df):
    df.to_csv('exo_dom_lesson4.csv')

regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
urls = getPageURL(2, regions)
tousLesLiens = getLiens(urls, "list_item clearfix trackable")
InfoCompletes = getCleanData(collectDataPourUnePage(tousLesLiens))
   

# A compléter avec la comparaison lacentrale

# AVEC REGEX
# caracteristiquesParVoitures = soupParVoiture.find_all(class_='value')
# caracteristiquesParVoitures = map(lambda x: x.text.replace('\xa0','') \
# .replace('\n','').strip(), soupParVoiture.find_all(class_='value'))

# regYear = r'[0-9]{4}'
# regex_year = re.compile(regYear)
# regKm = r'[0-9]*\s[A-Z]{2}'
# regex_regKm = re.compile(regKm)
