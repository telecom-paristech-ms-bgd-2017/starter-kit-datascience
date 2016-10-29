import requests
import numpy as np
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import csv


def get_list_url(url):
    page = requests.post(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup('a')
    table_url = []  # on veut créer une liste avec tous les liens d'annonces
    for tag in tags:
        sub_url = tag.get('href', None)
        try:
            if 'htm?ca=' in sub_url and 'voitures' in sub_url:
                sub_url = sub_url.replace('//', 'http://')
                table_url.append(sub_url)
        except:
            continue
    return table_url

def get_info(tab, Region):
    url_temp = tab
    page_temp = requests.post(url_temp)
    soup_temp = BeautifulSoup(page_temp.text, 'html.parser')
    script = soup_temp.find_all('script')
    test = str(script)
    el1 = "oas_cat"
    el2 = "urgent"
    if el1 in test:
        start = test.find(el1)
        stop = test.find(el2) + 41
    test2 = '{\n' + test[start:stop]
    # use regex to match json code
    test2 = re.sub(r"{\s*'?(\w)", r'{"\1', test2)
    test2 = re.sub(r",\s*'?(\w)", r',"\1', test2)
    test2 = re.sub(r"(\w)'?\s*:", r'\1":', test2)
    test2 = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', test2)

    # turn text from javascript into json
    result = json.loads(test2, "utf-8")
    #print(result)
    titre = result.get("titre").casefold()
    titre.split('_')
    type_vendeur = result.get("offres")
    km = float(result.get("km"))
    annee = int(result.get("annee"))
    prix = float(result.get("prix"))
    test4 = soup_temp.find_all(class_="line properties_description")
    for el in test4:
        description = str(el.find(class_="value")).casefold()
        description = description.replace('<br>', '').replace('<p class="value" itemprop="description">', '').replace(
            '</br>', '').replace('</p>', '').replace('.', '').replace(',', '').replace(':','')  # faudrait utiliser une regex
    descript = description.split()
    if 'zen' in descript or 'zen' in titre:
        model_car = 'zen'
    elif 'life' in descript or 'life' in titre:
        model_car = 'life'
    elif 'intens' in descript or 'intens' in titre:
        model_car = 'intens'
    else:
        model_car = 'inconnu'
    # on cherche le tel dans la description
    phone_pattern = re.compile(r'(0{1})(\d{1})\D*(\d{2})\D*(\d{2})\D*(\d{2})\D*(\d{2})$')
    for el in descript:
        #print(el)
        ph = phone_pattern.findall(el)
        if ph != []:
           phone = ''.join(''.join(s) for s in ph)
        else:
            phone = 'None'
    information = {"type_vendeur": type_vendeur, "kilometrage": km, "année": annee, "prix": prix, "modèle": model_car, "phone": phone, "Region": Region}
    return information

#df.columns = ["type_vendeur","kilometrage","année","prix","modèle","phone"]
def get_result_for_3region(url):
    Region = ['ile_de_france','aquitaine', 'provence_alpes_cote_d_azur']
    data = []
    for el1 in url:
        tab = get_list_url(el1)
        reg = el1.split('/')
        if Region[0] in reg:
            nomreg = Region[0]
        if Region[1] in reg:
            nomreg = Region[1]
        if Region[2] in reg:
            nomreg = Region[2]
        for el2 in tab:
            info = get_info(el2, nomreg)
            data.append(info)
    df = pd.DataFrame(data)
    return df

url = ['https://www.leboncoin.fr/voitures/offres/provence_alpes_cote_d_azur/?th=1&parrot=0&brd=Renault&mdl=Zoe',
       'https://www.leboncoin.fr/voitures/offres/aquitaine/?th=1&parrot=0&brd=Renault&mdl=Zoe',
       'https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&parrot=0&brd=Renault&mdl=Zoe']

df = get_result_for_3region(url)
print(df)