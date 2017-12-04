import requests
import bs4
import csv
import os
import pandas as pd
import numpy as np
import re


def get_title(soup_tmp):
    version = soup_tmp.find_all("title")[0].text.replace(" - leboncoin.fr", "")
    if "INTENS" in version.upper():
        version = "intens"
    elif "LIFE" in version.upper():
        version = "life"
    elif "ZEN" in version.upper():
        version = "zen"
    else:
        version = version
    return version


def get_status(soup_tmp):
    res_tmp = soup_tmp.find_all("div", class_="line line_pro noborder")
    # status=res_tmp[0].find("span").text
    if "SIREN" in res_tmp[0].text:
        status = "pro"
    else:
        status = "particulier"
    return status


def get_price(soup_tmp):
    res_tmp = soup_tmp.find_all("h2", class_="item_price clearfix")
    prix = res_tmp[0].text.strip()
    # prix = prix.replace("\n", "").replace(u'\xa0','').replace("Prix","").strip()
    prix = prix.replace("\n", "").replace(u'\xa0', '').replace("Prix", "").strip().replace("€", "")
    prix = float(prix.replace(" ", ""))
    return prix


def get_year(soup_tmp):
    res_tmp = soup_tmp.find_all("span", class_="value")
    year = res_tmp[4].text.strip().replace("\n", "")
    return year


def get_kilometrage(soup_tmp):
    res_tmp = soup_tmp.find_all("span", class_="value")
    kilometrage = res_tmp[5].text
    return kilometrage


def get_id(url_tmp):
    url_tmp = l_idf[0]
    fin = url_tmp.find(".htm")
    debut = url_tmp.find("s/")
    id = url_tmp[debut + 2:fin]
    return id


def get_tel(soup_tmp):

    res_tmp = soup_tmp.find("div", {"class": "line properties_description"}).find_all("p")[1].text
    num = re.search('0[1-9]([-. ]?[0-9]{2}){4}$', res_tmp)
    num = num.group(0) if num else None
    return num


regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]
url_test = "https://www.leboncoin.fr/voitures/offres/" + region + "/?th=" + str(page) + "&parrot=0&brd=Renault&mdl=Zoe"
url = url_ile_de_france
url_a

for region in regions:
    url_test = "https://www.leboncoin.fr/voitures/offres/" + region + "/?th=" + str(
        page) + "&parrot=0&brd=Renault&mdl=Zoe"

for url in url_all:
    R = requests.get(url)
soup = bs4.BeautifulSoup(R.content, 'html.parser')
res = soup.find_all("ul")
res[10]  # bloc avec les liens vers les autres voitures
taille = len(res[10].find_all("a", class_='list_item clearfix trackable'))


l_idf = []
for i in range(taille):
    adress = res[10].find_all("a", class_='list_item clearfix trackable')[i].get('href')
    l_idf.append("https:" + adress)

L = []
for a in l_idf:
    url_tmp = a
    list_tmp = []
    R_tmp = requests.get(url_tmp)
    soup_tmp = bs4.BeautifulSoup(R_tmp.content, 'html.parser')

    version = get_title(soup_tmp)
    list_tmp.append(version)

    status = get_status(soup_tmp)
    list_tmp.append(status)

    prix = get_price(soup_tmp)
    list_tmp.append(prix)

    year = get_year(soup_tmp)
    list_tmp.append(year)

    kilometrage = get_kilometrage(soup_tmp)
    list_tmp.append(kilometrage)

    id = get_id(url_tmp)
    list_tmp.append(id)

    num = get_tel(soup_tmp)
    list_tmp.append(num)

    L.append(list_tmp)
Data = pd.DataFrame(L)
Data.columns = ["VERSION", 'PRO', 'PRIX', "ANNEE", "KM", "ID_Tel", "NUM"]

def get_kilometrage(soup_tmp):
    res_tmp = soup_tmp.find_all("span",class_="value")
    kilometrage = res_tmp[5].text
    kilometrage =float( kilometrage.replace("KM","").replace(" ",""))
    return kilometrage


kilometrage = 6975
url = "http://www.lacentrale.fr/cote_proxy.php?km=7700&month=01"
my_referer =" http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide+type+2-2013.html"
a = requests.get(url, headers={'referer': my_referer})
print(a)

def get_argus(version):
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