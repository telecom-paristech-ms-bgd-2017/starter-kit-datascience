# -*- coding: utf-8 -*-
'''
Created on 6 oct. 2016

@author: utilisateur
'''
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


# sur cdiscount, + de remises sur ordinateurs asus que acer

def get_brand(desc):
    if desc.startswith('Pack'):
        brand = desc.split()[1]
    else:
        brand = desc.split()[0]
    print brand
    return brand.upper()

def get_prix1(prix1):
    return float(prix1.replace(',','.'))

def get_prix2(prix2):
    p = prix2[:-3] + '.' + prix2[-2:]
    return float(p)

url = {}
url['laptop'] = 'http://www.cdiscount.com/informatique/ordinateurs-pc-portables/v-10709-10709.html'
# url['bureau'] = 'http://www.cdiscount.com/informatique/achat-pc-ordinateur/v-10708-10708.html'
url['bureau'] = 'http://www.cdiscount.com/informatique/achat-pc-ordinateur/tous-les-pc-de-bureau-ici/l-1070840.html#_his_'


cols = ['brand', 'price1', 'price2']
products = pd.DataFrame()

for _,u in url.items():
    r = requests.get(u)
    soup = BeautifulSoup(r.text, 'html.parser')
    allproducts = soup.find_all(class_="prdtBZnTxt")
    for prod in allproducts:
        name = get_brand(prod.find(class_="prdtBTit").text)
        prix1 = get_prix1(prod.find(class_="prdtPrSt").text)
        prix2 = get_prix2(prod.find(class_="price").text)
#         print prod
#         print name
#         print prix1
#         print prix2
        products = products.append({'brand': name,
                                    'price1': prix1,
                                    'price2': prix2},
                                   ignore_index=True)

# tri par marque
products = products.sort_values(['brand'], ascending=True)
products = products.reset_index(drop=True)

# calcul de la remise avec %age / prix initial
products['reduc'] = products['price1'] - products['price2']
products['reduc_perc'] = 100. * (products['reduc'] / products['price1'])
# brands = products.drop_duplicates(['brand'], keep='first')
# print brands
print products
tmp = products.groupby(products['brand'])

# statistiques par marque
print tmp.describe()
# moyennes par marque
print tmp.mean()

