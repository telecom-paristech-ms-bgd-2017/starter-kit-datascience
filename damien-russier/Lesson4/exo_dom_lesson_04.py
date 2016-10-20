# -*- coding: utf-8 -*-
'''
Created on 6 oct. 2016

@author: utilisateur
'''

import unittest
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

'''
L'objectif est de générer un fichier de données sur le prix des
Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine. 
Vous utiliserezleboncoin.fr comme source. Le fichier doit être
propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous
récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables
(pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins
chere que sa cote moyenne.﻿
'''

regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']

# https://www.leboncoin.fr/annonces/offres/ile_de_france/?q=Renault%20Zo%E9&f=c
# https://www.leboncoin.fr/annonces/offres/aquitaine/?q=Renault%20Zo%E9&f=c
# https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?th=1&q=Renault%20Zo%E9&parrot=0


def find_tel_number(strg):
    '''
    https://openclassrooms.com/courses/apprenez-a-programmer-en-python/les-expressions-regulieres
    http://python.developpez.com/cours/DiveIntoPython/php/frdiveintopython/regular_expressions/phone_numbers.php
    0X XX XX XX XX
    0X-XX-XX-XX-XX
    0X.XX.XX.XX.XX
    0XXXXXXXXX
    '''
    regex = r"0[0-9]([ .-]?[0-9]{2}){4}"
    # regex = r"0[0-9]{9}"
    m = re.search(regex, strg)
    if m:
        num = m.group().replace('.', '').replace('-', '').replace(' ', '')
        # print num
        return num
    else:
        return 'NA'


def find_version(strg):
    regex = [r" ZEN ", r" INTENS ", r" LIFE "]
    match = False
    for r in regex:
        m = re.search(r, strg.upper())
        if m:
            # print m.group()
            match = True
            return m.group().strip()
    if not match:
        return 'NA'


def find_type(strg):
    s = re.sub('\s+', ' ', strg).strip()
    # print s
    regex = r"TYPE 2"
    m = re.search(regex, s.upper())
    if m:
        # print m.group()
        return 2
    else:
        return 1


def get_argus(version, annee, type):
    if (int(annee) >= 2016):
        return 'NA'
    if (version == 'NA'):
        return 'NA'
#     http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2013.html
#     http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide+type+2-2013.html
    url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + version.lower() + \
    '+charge+rapide'
    if type == 2:
        url += '+type+2-' + annee
    else:
        url += '-' + annee
    url += '.html'
    # print url
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            cote = soup.find(class_="f24 bGrey9L txtRed pL15 mL15").text.strip()
            cote = float(''.join(cote.split()[:-1]))
            # print cote
            return cote
        except AttributeError:
            print url
            return 'NA'
    else:
        return 'NA'


voitures = pd.DataFrame()
for reg in regions:
    print "***************** région : ", reg
    i = 1
    url = 'https://www.leboncoin.fr/voitures/offres/' + reg + '/'
    count = 0
    while True:
        params = {'q': 'renault zoe', 'o': i}
        r = requests.get(url, params=params)
        # print url
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            listcars = soup.find_all(class_='tabsContent block-white dontSwitch')\
            [0].find_all('a', class_='list_item clearfix trackable')
            i += 1
            for car in listcars:
                count += 1
                print 'Voiture %03i : ' % (count) +\
                car.find(class_='item_title').text.strip()
                urlcar = car['href'].replace('//', 'https://')
                # print urlcar
                rcar = requests.get(urlcar)
                soupcar = BeautifulSoup(rcar.text, 'html.parser')
                prix = float(soupcar.find(itemprop='price')['content'])
                annee = soupcar.find(itemprop='releaseDate').text.strip()
                km = int(soupcar.find_all('h2', class_='clearfix')[5].\
                     find(class_='value').text.replace(' ', '').\
                     replace('KM', ''))
                ispro = soupcar.find(class_='line line_pro noborder').\
                find(class_='ispro')
                if (ispro):
                    pro = 'YES'
                else:
                    pro = 'NO'
                desc = soupcar.find(class_='line properties_description').\
                find(itemprop='description').text
                tel = find_tel_number(desc)
                version = find_version(desc)
                type = find_type(desc)
                argus = get_argus(version, annee, type)
                if (prix > argus):
                    pascher = 'NO'
                else:
                    pascher = 'YES'
#             print prix
#             print annee
#             print km
#             print tel
#             print pro
#             print argus
#             print type
#             print cher
                voitures = voitures.append({'version': version,
                                        'année': annee,
                                        'km': km,
                                        'prix': prix,
                                        'tél': tel,
                                        'pro': pro,
                                        'argus': argus,
                                        'bon marché': pascher},
                                       ignore_index=True)
        except:
            break  # sort de la boucle si dépasse la page maximum

# print voitures
voitures.to_csv('voitures.csv', encoding="utf-8")


# unit tests
class FunctionTests(unittest.TestCase):

    def testTelNumber(self):
        self.assertEqual(find_tel_number('bla 0623456789, bla'), '0623456789')
        self.assertEqual(find_tel_number('bla 06.23.45.67.89, bla'), '0623456789')

    def testFindVersion(self):
        self.assertEqual(find_version("renault zEn type 2"), 'ZEN')
        self.assertEqual(find_version("renault intens type 2"), 'INTENS')
        self.assertEqual(find_version("renault LiFe type 2"), 'LIFE')
        self.assertEqual(find_version("renault zebu type 2"), 'NA')

    def testFindType(self):
        self.assertEqual(find_type("renault zEn type 1"), 1)
        self.assertEqual(find_type("renault zEn type 2"), 2)
        self.assertEqual(find_type("renault zEn type   2"), 2)

    def testgetArgus(self):
        self.assertEqual(get_argus('INTENS', '2013', 2), 10700.)


def main():
    unittest.main()

if __name__ == '__main__':
    main()


