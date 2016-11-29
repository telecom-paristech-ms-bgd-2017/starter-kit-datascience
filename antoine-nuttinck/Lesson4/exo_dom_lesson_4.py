# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:27:34 2016

@author: Antoine
"""
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup


def extract1stMatching(pattern, draw_arr, grp=0):
    regex = re.compile(pattern, re.IGNORECASE)
    for elem in draw_arr:
        res = regex.search(elem)
        if res:
            return res.group(grp).replace(' ', '')
    return res


def getCarFields(url):
    fields = {'version': 'NA',
              'annee': 'NA',
              'kilometrage': 'NA',
              'prix': 'NA',
              'telephone': 'NA',
              'professionnel': 'NA'}
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    fields['professionnel'] = (soup.find(class_='ispro') is not None)
    fields['prix'] = int(soup.find(class_='item_price clearfix')['content'])

    info_arr = list(map(lambda t: t.text, soup.find_all(class_='value')))

    fields['annee'] = int(extract1stMatching(r'(201[2-6])', info_arr))
    fields['kilometrage'] = int(extract1stMatching(r'(([0-9]+\s*)+)[K][M]',
                                info_arr, 1))
    fields['telephone'] = extract1stMatching(r'0[1-68]([-. ]?[0-9]{2}){4}',
                                             info_arr)
    info_arr.insert(0, soup.title.text)
    fields['version'] = extract1stMatching(r'zen|intense|life', info_arr)

    return fields


def getArgus(model, annee):
    url = "http://www.lacentrale.fr/cote-voitures-renault-zoe-{0}-{1}-.html."
    result = requests.get(url.format(model, annee))
    soup = BeautifulSoup(result.text, 'html.parser')

    return soup.find(class_="jsCoteAffinee").text
    # soup.find(class_="f24 bGrey9L txtRed pL15 mL15")


def getCarsData():
    allCars_bc_data = []
    MAX_PAGE = 2
    regions = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine"]
    search_url = "https://www.leboncoin.fr/voitures/offres/{0}/?o={1}&q=Renault%20Zo%E9"
    for reg in regions:
        for page in range(1, MAX_PAGE + 1):
            all_cars = requests.get(search_url.format(reg, page))
            if all_cars.ok:
                soup_search = BeautifulSoup(all_cars.text, 'html.parser')
                list_cars = map(lambda x: 'https:' + x['href'],
                                soup_search.find_all(
                                class_='list_item clearfix trackable'))
                for link in list(list_cars):
                    bc_car_data = getCarFields(link)
                    allCars_bc_data.append(bc_car_data)
    allCars_bc_df = pd.DataFrame(allCars_bc_data)
    allCars_bc_df.fillna(value=np.nan, inplace=True)
    allCars_bc_df.index = allCars_bc_df.index.map(lambda x: 'Voiture ' + str(x))

    return allCars_bc_df

print(getCarsData())
