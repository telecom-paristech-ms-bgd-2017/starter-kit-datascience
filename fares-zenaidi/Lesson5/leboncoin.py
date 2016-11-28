from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import json
import pandas as pd
from pandas import DataFrame, Series
from multiprocessing import Pool
import time

url = 'https://www.leboncoin.fr/voitures/offres/{}/?th={}&parrot=0&brd=Renault&mdl=Zoe'
regions = ['aquitaine', 'provence_alpes_cote_d_azur', 'ile_de_france']


# Get max. number of pages for a region
def get_max_pages(region):
    url_source = 'https://www.leboncoin.fr/voitures/offres/{}/?th=1&parrot=0&brd=Renault&mdl=Zoe'
    response = requests.get(url_source.format(region))
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        max_pages = int(re.findall(r"o=(\d*)", soup.select('#last')[0]['href'])[0])
    except:
        max_pages = 1
    return max_pages


def get_car_infos(soup, region):
    cars_pointer = soup.select('.tabsContent > ul > li > a')
    car_infos = {'region': [], 'id': [], 'holder': [], 'version': [], 'year': [], 'km': [], 'price': [], 'tel': []}
    car_urls = []
    for car in cars_pointer:
        car_urls.append(car['href'].replace('//', 'https://'))
        car_infos['region'].append((region))
        car_infos['id'].append(json.loads(car['data-info'])['ad_listid'])
        if car.select('.item_infos > .item_supp')[0].select('.ispro'):
            car_infos['holder'].append('Professionnel')
        else:
            car_infos['holder'].append('Particulier')

    # Extraction des infos (version, année, kilométrage, prix, tel)
    for car_url in car_urls:
        response = requests.get(car_url)
        soup_info = BeautifulSoup(response.text, 'html.parser')
        # Price
        car_infos['price'].append(soup_info.select('.line > .item_price')[0]['content'])
        # Year
        car_infos['year'].append(soup_info.select('span[itemprop="releaseDate"]')[0].text.strip())
        # Km (kilométrage)
        car_infos['km'].append(soup_info.select('.line > .clearfix > .value')[5].text.replace('KM', '').strip())
        # Version (INTENS, LIFE, ZEN)
        try:
            reg_ex_version = re.findall(r"(ZEN|INTENS|LIFE)\s*(TYPE\s*2)?", soup_info.select('.no-border')[0].text,
                                        re.IGNORECASE)
            car_infos['version'].append((reg_ex_version[0][0]).lower())
        except:
            car_infos['version'].append('NA')
        # Téléphone
        try:
            reg_ex_tel = re.findall(r"(\d{10})", soup_info.select('p[itemprop="description"]')[0].text, re.IGNORECASE)
            car_infos['tel'].append(reg_ex_tel[0])
        except:
            car_infos['tel'].append('NA')

    return DataFrame(car_infos, columns=['id', 'region', 'holder', 'version', 'year', 'km', 'price', 'tel']).set_index('id')


def get_cars_region(region):
    max_pages = get_max_pages(region)
    df_region = DataFrame()
    for page in range(max_pages):
        response = requests.get(url.format(region, page))
        soup = BeautifulSoup(response.text, 'html.parser')
        df_page = get_car_infos(soup, region)
        df_region = pd.concat([df_region, df_page])
    return df_region


def get_cars(regions):
    df = DataFrame()
    for region in regions:
        df = pd.concat([df, get_cars_region(region)])
    return df

start_time = time.time()

# get_cars_region('ile_de_france')
print('**************** ELAPSED TIME *****************')
df = get_cars(regions)
print(df)
elapsed = time.time() - start_time
print(elapsed)
