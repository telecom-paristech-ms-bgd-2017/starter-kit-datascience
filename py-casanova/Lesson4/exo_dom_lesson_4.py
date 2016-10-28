#! /usr/bin/python3.5

import requests
import json
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

from itertools import product as cartesian_product
from multiprocessing import Pool

root_url = 'https://www.leboncoin.fr/voitures/offres'
apiKey = '54bb0281238b45a03f0ee695f73e704f'
flavours = ['zen', 'intens', 'life']


def get_listings_data(product, seller_type, region):
    print("Getting data for region: " + str(region) +
          " & seller type: " + str(seller_type))

    payload = {'q': product, 'f': seller_type}
    url = '/'.join([root_url, region])
    liste_annonces_results = requests.get(url, params=payload)
    soup = BeautifulSoup(liste_annonces_results.text, 'html.parser')

    # Crawling listing links
    links = []
    try:
        for i, annonce in enumerate(soup.find(id='listingAds').find_all(class_='list_item')):
            links.append(soup.find(id='listingAds').find_all(
                class_='list_item')[i].attrs['href'])
    except:
        pass

    annonces = []
    for link in links:
        url_link = 'http:' + link
        annonce_page = requests.get(url_link)
        sp = BeautifulSoup(annonce_page.text, 'html.parser')

        # Scraping price, year, car_type, kms
        price = int(sp.find_all(class_='item_price clearfix')[0].find(class_='value').text.split(
            '€')[0].replace('\n', '').replace('\xa0', '').replace(' ', ''))
        year = int(sp.find_all(class_='value', itemprop='releaseDate')[0].text.replace(
            '\n', '').replace(' ', ''))

        car_type = 'na'
        for flavour in flavours:
            if(sp.find(string=re.compile(flavour, re.IGNORECASE))):
                car_type = flavour

        kms = int(sp.find(string=re.compile("KM")).replace(
            'KM', '').replace(' ', ''))

        # Getting phone with "api"
        header = {'Origin': 'https://www.leboncoin.fr', 'Referer': url_link}
        print(url_link)
        listid = re.search('\d{9,10}', url_link).group(0)
        form_data = {'list_id': listid,
                     'app_id': 'leboncoin_web_utils', 'key': apiKey, 'text': '1'}
        form_data = json.dumps(form_data)
        phonenumber_req = requests.post(
            'https://api.leboncoin.fr/api/utils/phonenumber.json', headers=header, data=form_data)

        try:
            phone = phonenumber_req.json()['utils']['phonenumber']
        except:
            phone = 'na'
            phone = sp.find(string=re.compile('^0\d{9}'))

        annonce_data = [region, car_type, price, year, kms, phone, seller_type]
        annonces.append(annonce_data)

    return annonces


def get_listings_data_parallel(product, seller_types, regions_url):
    pool = Pool()
    product_l = [product]
    threaded_inputs = list(cartesian_product(product_l, seller_types, regions_url))
    return pool.starmap(get_listings_data, threaded_inputs)


def get_argus_quote(car_type, year, kms):
    car_type = str(car_type)
    kms = str(kms)
    # wip (year = 2013)
    year = str(year)

    params = {'km': str(kms), 'month': '01'}
    if(car_type == 'zen'):
        cookie = '_mob_=0; xtvrn=$251312$; retargeting_data=B; __troRUID=5175711b-214c-4740-a86d-c786f3ac6ccd; __sonar=16779486186693993948; php_sessid=2b9ec45a8e16a0f4e967156350bc7df6; __uzma=5807b6668e0156.47210791; __uzmb=1476900454; __troSYNC=1; __uzmc=886976753498; __uzmd=1476913370; tCdebugLib=1; xtan251312=-; xtant251312=1; ry_ry-9mpyr1d3_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwiZXhwIjoxNTA4MDkzMzQwODA2fQ%3D%3D; ry_ry-9mpyr1d3_so_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGx9'
    elif(car_type == 'intens'):
        cookie = '_mob_=0; xtvrn=$251312$; retargeting_data=B; __troRUID=5175711b-214c-4740-a86d-c786f3ac6ccd; __sonar=16779486186693993948; php_sessid=2b9ec45a8e16a0f4e967156350bc7df6; __uzma=5807b6668e0156.47210791; __uzmb=1476900454; __troSYNC=1; __uzmc=950063198580; __uzmd=1476903417; tCdebugLib=1; xtan251312=-; xtant251312=1; ry_ry-9mpyr1d3_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwiZXhwIjoxNTA4MDkzMzQwODA2fQ%3D%3D; ry_ry-9mpyr1d3_so_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGx9'
    elif(car_type == 'life'):
        cookie = '_mob_=0; xtvrn=$251312$; retargeting_data=B; __troRUID=5175711b-214c-4740-a86d-c786f3ac6ccd; __sonar=16779486186693993948; php_sessid=2b9ec45a8e16a0f4e967156350bc7df6; __uzma=5807b6668e0156.47210791; __uzmb=1476900454; __troSYNC=1; __uzmc=764324637892; __uzmd=1476911994; tCdebugLib=1; xtan251312=-; xtant251312=1; ry_ry-9mpyr1d3_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwiZXhwIjoxNTA4MDkzMzQwODA2fQ%3D%3D; ry_ry-9mpyr1d3_so_realytics=eyJpZCI6InJ5XzRCMjhGQ0I4LUZFMzYtNEQwRi1BRTRFLUY4OUFFRkJGREUyOSIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGx9'
    else:
        cookie = 'na'
        pass
    header = {'referer': 'http://www.lacentrale.fr/cote-auto-renault-zoe-' +
              str(car_type) + '+charge+rapide-' + str(year) + '.html', 'Cookie': cookie}
    argus_req = requests.get(
        'http://www.lacentrale.fr/cote_proxy.php', params=params, headers=header)
    try:
        quote = argus_req.json()['cote_perso']
    except:
        return np.NaN
    return quote

# MAIN
# p = particulier, c = pro

product = 'renault zoe'
seller_types = ['p', 'c']
regions_url = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']

# Sequential version
"""for region in regions_url:
    print("Getting data for region:" + str(region))
    for seller_type in seller_types:
        print("Getting data for seller type:" + str(seller_type))
 
        output = get_listings_data(product, seller_type, region)
        df = df.append(output)"""

# Parallelized version
# +++ All your data are belong to us ;-) +++
data_lol = get_listings_data_parallel(product, seller_types, regions_url)
data_list = [elem for sublist in data_lol for elem in sublist]
df = pd.DataFrame(data_list)

df.columns = ['region', 'car_type', 'price',
              'year', 'kms', 'phone', 'seller_type']
df['argus'] = np.NaN
#df.reset_index(inplace=True, drop=True)

# Getting argus quotes
for i, tu in enumerate(df.itertuples()):
    df['argus'][i] = get_argus_quote(
        df['car_type'][i], df['year'][i], df['kms'][i])

df['bargain'] = df['price'] < df['argus']
df.to_csv('./lbc_zoe.csv')
