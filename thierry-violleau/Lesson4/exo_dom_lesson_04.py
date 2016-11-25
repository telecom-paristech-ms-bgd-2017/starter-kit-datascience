import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
Vous utiliserez leboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année,
 kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site
 http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿

"""

# Url to the "leboncoin.fr" web site.
Le_bon_coin_url = 'https://www.leboncoin.fr/voitures/offres/{region}/'
Le_bon_coin_ad_url_pattern = '//www.leboncoin.fr/voitures/'

# Url to the "lacentrale.fr" web site.
La_centrale_url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide-{year}.html'
La_centrale_url_2 = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{version}+charge+rapide+gamme+{nyear}-{year}.html'

# Common HTTP request query parameters, if any
Params = {
    'q': '???'
}

Car_quote_cache = {}


# Retrieves the quote of 'Renault Cloe' cars of the specified version and year from the "La Centrale" web site;
# returns the quote as a string.
def get_car_quote(version, year):
    if (version, year) not in Car_quote_cache:
        nyear = int(year) + 1
        for url in [La_centrale_url.format(version=version, year=year),
                    La_centrale_url_2.format(version=version, year=year, nyear=nyear)]:
            data = requests.get(url)
            parser = BeautifulSoup(data.text, 'html.parser')
            node = parser.find('h2', string=re.compile(r"\s*Cote\s+brute\s*"))
            if node:
                node = node.parent.find(class_="txtRed")
                if node:
                    price = extract_price(node)
                    Car_quote_cache[(version, year)] = price
                    return price
        Car_quote_cache[(version, year)] = 'N/A'
        return 'N/A'
    return Car_quote_cache[(version, year)]


# Extracts the price from the text of the designated DOM node.
def extract_price(node):
    return float(node.text.replace(u'\xa0', '').replace(u' ', '').replace(u'€', '.').replace(u',', u'.'))


# Retrieves the urls and type (pro or not) of ads for "Renault Cloe" cars from the "Le Bon Coin" web site;
# returns a dictionary of <url, boolean> values.
def get_car_ads_for_region(region, car_name):
    url = Le_bon_coin_url.format(region=region)
    params = Params.copy()
    params['q'] = car_name
    data = requests.get(url, params=params)
    results = {}
    parser = BeautifulSoup(data.text, 'html.parser')
    for ad_node in parser.findAll(class_="list_item"):
        url = ad_node.attrs['href']
        if url.startswith(Le_bon_coin_ad_url_pattern):
            pro = ad_node.find(class_="ispro") is not None
            results[url] = pro
    return results


# Retrieves all the "Renault Cloe" car ads for the specified regions from the "Le Bon Coin" web site;
# returns a data frame containing the brand, model, version, the year, the offered price and quote of advertised cars.
def get_car_ads_for_regions(regions):
    car_name = 'Renault Zoé'
    properties = {'Marque': 'brand', 'Modèle': 'model', 'Kilométrage': 'mileage', 'Année-modèle': 'releaseDate',
                  'Prix': 'price', 'Description :': 'description'}
    results = []
    for region in regions:
        for url, pro in get_car_ads_for_region(region, car_name).items():
            url = 'https:' + url
            data = requests.get(url)
            parser = BeautifulSoup(data.text, 'html.parser')
            ad = {'url': url, 'pro': pro}
            for prop_node in parser.findAll(class_="property"):
                if prop_node.text in properties.keys():
                    value_node = prop_node.parent.find(class_=["value", "clearfix"])
                    if value_node:
                        try:
                            prop = value_node.attrs['itemprop']
                        except KeyError:
                            try:
                                prop = value_node.parent.attrs['itemprop']
                            except:
                                prop = properties[prop_node.text]
                        if prop in properties.values():
                            try:
                                value = value_node.attrs['content']
                            except KeyError:
                                value = value_node.text.strip()
                        ad[prop] = value
            node = parser.find(class_="adview_header")
            ad['all_text'] = node.text
            results.append(ad)
    df = pd.DataFrame(results)
    return clean_data(df)

# Cleans the provided data frame containing raw data collected from all the "Renault Cloe" car ads for the specified
# regions from the "Le Bon Coin" web site;
# returns a data frame containing the version, the year, the announcer's phone, the offered price and quote of advertised cars.
def clean_data(df):
    df = df[df['brand'].str.lower() == 'renault']
    df = df[df['model'].str.lower() == 'zoe']
    df['price'] = df['price'].apply(lambda m: m.replace(' ', '').replace('€', ''))
    df['mileage'] = df['mileage'].apply(lambda m: m.replace(' ', '').replace('KM', ''))
    df['version'] = df[['description', 'all_text']].apply(extract_version, axis=1)
    df['phone'] = df['description'].apply(extract_phone)
    df['quote'] = df[['version', 'releaseDate']].apply(lambda x: get_car_quote(*x), axis=1)
    df = df.drop(['brand', 'model', 'description', 'all_text', 'url'], axis=1)
    return df

# Extracts the version of the "Renault Zoe" car from its ad's description and overall text content.
#  returns the version: Zen, Life or Intens or an empty string if not found within the description or overall ad text.
def extract_version(text):
    re_str = r"\s*.*(renault\s*|)zo[eé][\s,]*(zen|life|intens).*"
    m = re.match(re_str, text[0].lower())
    if m is None:
        m = re.match(re_str, text[1].lower())
    return m.group(2).lower() if m is not None else ''


# Extracts the phone of the "Renault Zoe" car announcer's from its ad's description and overall text content.
#  returns the phone number in a canonical form or an empty string if not found within the description.
def extract_phone(description):
    m = re.match(".*[^\d]((\s?\d){9,10}).*", description.lower())
    phone = m.group(1).replace(' ', '') if m is not None else ''
    if len(phone) == 9:
        phone = "0" + phone
    return  phone


df = get_car_ads_for_regions(['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine'])
print(df)
