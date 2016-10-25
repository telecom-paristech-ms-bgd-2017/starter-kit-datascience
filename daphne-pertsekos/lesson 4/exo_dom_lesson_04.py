# coding: utf8
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import urllib2
import re
import pandas as pd
import  unicodedata

def get_DOM(url):
    html_doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def get_car_features(soup):
    price = soup.find("h2", {"class": "item_price clearfix"})["content"]
    release = int(soup.find("span", {"itemprop": "releaseDate"}).text)
    prix = soup.find("meta", {"itemprop": "priceCurrency"}).parent.find('span', {"class": "value"}).text.replace(u"€",'').replace(' ', '').replace('\n','')
    prix = unicodedata.normalize("NFKD", prix)
    properties = soup.find_all("span", {"class": "property"})
    for propriete in properties:
        if propriete.text == u"Kilom\xe9trage":
            kilometrage = propriete.parent.find_all("span")[1].text.replace("KM", '').replace(' ', '')
    description = soup.find("div", {"class": "line properties_description"}).find_all("p")[1].text
    tel =  re.search("0[1-9]([-. ]?[0-9]{2}){4}$", description.lower())
    tel = tel.group(0) if tel else None

    return [release, prix, kilometrage, tel]

def get_modele(annonce):
    modele = ""
    for modele_type in ["life", "intens", "zen"]:
        if modele_type in annonce.find("h2", {"class": "item_title"}).text.lower():
            modele = modele_type
    return modele

def get_features(url):
    soup = get_DOM(url)
    section = soup.find("section", {"class": "list mainList tabs"})
    voitures = section.find("ul").find_all("li")

    for voiture in voitures:
        href =  voiture.find("a")["href"]
        is_pro = voiture.find("span", {"class": "ispro"})
        is_pro = 1 if is_pro else 0
        modele = get_modele(voiture)
        href = "https://"+href[2:]
        soup = get_DOM(href)
        release, prix, kilometrage, tel = get_car_features(soup)
        cote = cotes[str(release)][modele] if release != 2016 and release and modele else None
        car_features = [release, prix, kilometrage, tel, modele, is_pro, cote]
        features.append(car_features)
        #print "Release : {} - Prix : {} - Kilometrage : {} - modele : {} - isPro : {} - Tel : {} ".format(release, prix, kilometrage, modele, is_pro, tel)
    return  features

def get_argus():
    releases = ['2012', '2013', '2014', '2015']
    models=['intens+charge+rapide', 'life+charge+rapide','zen+charge+rapide']
    cotes = {}
    for release in releases:
        cotes[release]={}
        for model in models:
            url = "http://www.lacentrale.fr/cote-auto-renault-zoe-{}-{}.html".format(model, release)
            soup = get_DOM(url)
            cote = soup.find("strong", {"class":"f24 bGrey9L txtRed pL15 mL15"})
            cote = cote.text.replace('€','').replace(u' ','') if cote else None
            cotes[release][model.split('+')[0]] = cote.replace('\n','')
    return cotes

regions = ["ile_de_france", "aquitaine","provence_alpes_cote_d_azur"]
features = []
cotes = get_argus()
for region in regions:
    params = "/?th=1&parrot=0&brd=Renault&mdl=Zoe"
    url = "https://www.leboncoin.fr/voitures/offres/"+region+params
    get_features(url)

df = pd.DataFrame(data=features)
df.to_csv("renault.csv",header=['release', 'prix', 'kilometrage', 'tel', 'modele', 'is_pro', 'cote'], encoding="utf-8")


