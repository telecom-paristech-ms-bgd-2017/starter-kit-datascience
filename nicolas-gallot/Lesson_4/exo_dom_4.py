# L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine.
# Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année,
# kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
# Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

from bs4 import BeautifulSoup
import requests
import class_car_ad as ca
import pandas as pd
from multiprocessing import Pool
import sys

BASE_URL = "https://www.leboncoin.fr/voitures/offres/{0}/?o={1}&q=Renault%20Zoe"
REGIONS = ['ile_de_france']



def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_url(region, page_id):
    return BASE_URL.format(region, page_id)


def is_valid_url(url):
    bs = getBeautifulSoupObjectfromUrl(url)
    not_found = bs.find_all(class_='noResult clearfix listing_thumbs ab-testing_A')
    if len(not_found) > 0:
        return False
    return True

# This function would have to be changed to retrieve values from the website
def get_argus_data():

    df = pd.DataFrame(columns=['Model', 'Year', 'Argus'])

    df.loc[0] = ['intens', '2012', 9599]
    df.loc[1] = ['life', '2012', 9121]
    df.loc[2] = ['zen', '2012', 9434]

    df.loc[3] = ['intens', '2013', 10642]
    df.loc[4] = ['life', '2013', 10113]
    df.loc[5] = ['zen', '2013', 10459]

    df.loc[6] = ['intens', '2014', 11799]
    df.loc[7] = ['life', '2014', 11212]
    df.loc[8] = ['zen', '2014', 11596]

    df.loc[9] = ['intens', '2015', 12921]
    df.loc[10] = ['life', '2015', 12265]
    df.loc[11] = ['zen', '2015', 12694]

    df.loc[12] = ['intens', '2016', 15099]
    df.loc[13] = ['life', '2016', 13741]
    df.loc[14] = ['zen', '2016', 14821]

    return df


def get_argus_value(model, year, argus_data):
    args = [model, year]
    try:
        return argus_data.loc[argus_data[['Model', 'Year']] == args]
    except:
        return "NA"


def get_single_car_data(html_car_info):
    attrs = html_car_info.attrs
    txt_price = html_car_info.findChildren(class_="item_price")[0].text.lower()
    return ca.CarAd(attrs, txt_price)


def get_car_data_by_region_and_page_parallel(url):
    pool = Pool()
    bs = getBeautifulSoupObjectfromUrl(url)
    classes = bs.find_all(class_="list_item clearfix trackable")
    return pool.map(get_single_car_data, classes)


def get_car_data_by_region_and_page_sequential(url):
    res = []
    bs = getBeautifulSoupObjectfromUrl(url)
    classes = bs.find_all(class_="list_item clearfix trackable")
    for c in classes:
        res.append(get_single_car_data(c))
    return res


def cars_list_to_dataframe(cars):
    res = pd.DataFrame(columns=['Model', 'Year', 'Kilometrage', 'Add_Type', 'Phone number', 'Price'])
    i = 0
    for c in cars:
        res.loc[i] = c.to_df()
        i += 1
    return res


###### MAIN SCRIPT

sys.setrecursionlimit(100000)
regions = ['aquitaine', 'ile_de_france', 'provence_alpes_cote_d_azur']
pages = range(1, 10)
df = pd.DataFrame(columns=['Model', 'Year', 'Kilometrage', 'Add_Type', 'Phone number', 'Price'])
frames = []

# urls = [(get_url(r, p)) for r in regions for p in pages] #map(get_url, regions, pages)

for r in regions:
    for p in pages:
        url = get_url(r, p)
        if not is_valid_url(url):
            break
        print(url)
        cars = get_car_data_by_region_and_page_parallel(url)
        df_c = cars_list_to_dataframe(cars)
        frames.append(df_c)


df = pd.concat(frames)
argus = get_argus_data()
res = pd.merge(df, argus, how='left', on=('Model', 'Year'))
res_clean = res.dropna(subset=['Argus'])
print(res_clean)
