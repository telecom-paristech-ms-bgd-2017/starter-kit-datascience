# -*- coding: utf-8 -*-
'''
Created on 3 oct. 2016

@author: utilisateur
'''
import requests
from bs4 import BeautifulSoup

url_paris = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
url_caen  = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=118&dep=014&type=BPS&param=5&exercice='


def str2int(strg):
    return int(''.join(strg.split()))
    
def get_data_1year(url, year):
    r = requests.get(url + str(year))
    soup = BeautifulSoup(r.text, 'html.parser')
    EurParHab = {}
    MoyStrate = {}
    index = {'A': 1,
             'B': 4,
             'C': 10,
             'D': 13}
    for k, v in index.items():
        EurParHab[k] = str2int(soup.find_all(class_="montantpetit G")[v  ].text)
        MoyStrate[k] = str2int(soup.find_all(class_="montantpetit G")[v+1].text)
    return EurParHab, MoyStrate

def get_data_2010_2013(url):
    EurParHab = {}
    MoyStrate = {}
    for year in range(2010, 2014):
        EurParHab[year], MoyStrate[year] = get_data_1year(url, year)
    return EurParHab, MoyStrate

def print_data_2010_2013(url, city='Paris'):
    EurParHab, MoyStrate = get_data_2010_2013(url)
    strg = ''
    newline = ' \n'
    sep = "=========== "
    cols = "                         A      B      C      D"
    eph = "Euros par habitant : "
    mps = "Moyenne par strate : "
    lst = ['A','B','C','D']
    strg += sep + city+ newline
    for year in range(2010, 2014):
        strg += sep + str(year) + newline + cols + newline
        strg += eph
        for e in lst:
            strg += "%5i" % EurParHab[year][e] + '  '
        strg += newline
        strg += mps
        for e in lst:
            strg += "%5i" % MoyStrate[year][e] + '  '
        strg += newline * 2
    print strg

print_data_2010_2013(url_paris)
print_data_2010_2013(url_caen, 'caen')


