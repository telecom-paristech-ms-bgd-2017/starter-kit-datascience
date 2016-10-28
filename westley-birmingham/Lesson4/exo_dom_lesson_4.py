import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import pandas as pd
import re
import os

# url = 'https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&q=Renault%20Zoe&parrot=0'
url_base = 'https://www.leboncoin.fr/voitures/offres/{0}/?th=1&q=Renault%20Zoe&parrot=0'
df_zoe = pd.DataFrame(
    columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
             'argus'])
region_list_full = ('ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine')


def car_url_list(region, url):
    result = requests.get(url).text
    soup = BeautifulSoup(result, 'html.parser')
    df_zoe_tmp1 = pd.DataFrame(
        columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
                 'argus'])

    for index_url in range(len(soup.main.find_all('ul')[0].find_all('li'))):
        ad_list_id = soup.main.find_all('ul')[0].find_all('li')[int(index_url)] \
            .a['data-info'].split(',')[2].split(':')[1].replace('"', '').replace(' ', '')

        # is_pro = soup.main.find_all('ul')[0].find_all('li')[int(el)].find_all(class_='ispro').text
        # BeautifulSoup(requests.get('https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&q=Renault%20Zoe&parrot=0').text, 'html.parser').main.find_all('ul')[0].find_all('li')[int(el)].find_all(class_='ispro').text

        new_url = soup.main.find_all('ul')[0].find_all('li')[int(index_url)].a['href'].replace('//', 'https://')

        df_zoe_tmp1 = df_zoe_tmp1.append([{'id': ad_list_id, 'region': region, 'url': new_url}], ignore_index=True)

    return df_zoe_tmp1


def extract_urls_car(region_list, url_b):
    df_zoe_tmp2 = pd.DataFrame(
        columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
                 'argus'])

    for region_i in region_list:
        df_zoe_tmp2 = pd.concat([df_zoe_tmp2, car_url_list(region_i, url_b.format(region_i))])
        df_zoe_tmp2.reset_index()
    return df_zoe_tmp2


def extract_characteristics(url, region_url):
    df_zoe_tmp3 = pd.DataFrame(
        columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
                 'argus'])
    result = requests.get(url).text
    soup = BeautifulSoup(result, 'html.parser')

    characteristics_price = int(soup.find_all(class_='line')[2].text.replace(' ', '') \
                                .replace(u'\n', '').replace('nan', '') \
                                .replace('Prix', '').replace(u'\xa0', '').replace('€', ''))

    characteristics_year = int(soup.find_all(class_='line')[6].text.replace(' ', '') \
                               .replace(u'\n', '').replace(u'\xa0', '').replace('Année-modèle', ''))

    characteristics_kilometrage = (soup.find_all(class_='line')[7].text.replace(' ', '').replace('Kilométrage', '') \
                                   .replace(u'\n', '').replace(
                                'KM', '').replace(u'\xa0', '').replace(u'\t', ''))



    # characteristics_version = soup.find_all(class_='line')[5]\
    #                            .text.replace(' ', '').replace(u'\n', '')\
    #                            .replace(u'\xa0', '').replace('Modèle', '')

    # commande synthetique
    #.select(".tabscontent > ul > li > a")

    characteristics_version_full = soup.find_all(class_='no-border')[0] \


    # soup.text.replace(u'\n', '').replace(u'\t', '').strip()

    characteristics_description = soup.find_all(class_='line properties_description')[0].text.replace(u'\n', '') \
        .replace('Description :', '')

    if re.search('(\d{10})', characteristics_description):
        tel_clean = re.search('(\d{10})', characteristics_description).group(0)
    else:
        tel_clean = 'NaN'

    if re.search('(INTENS|ZEN|LIFE) *(TYPE *2)?', characteristics_version_full.upper()):
        version_clean = re.search('(INTENS|ZEN|LIFE) *(TYPE *2)?', characteristics_version_full.upper()).group(0)
    else:
        version_clean = 'NaN'

    df_zoe_tmp3 = df_zoe_tmp3.append([{'region': region_url,
                                       'url': url,
                                       'price': characteristics_price,
                                       'year': characteristics_year,
                                       'kilometrage': characteristics_kilometrage,
                                       'version': version_clean,
                                       'telephone': tel_clean,
                                       'description': characteristics_description}], ignore_index=True)
    return df_zoe_tmp3


# Pool.map(extract_characteristics(), listURLGlob)

def save_car_data(df_url_to_crawl):
    for url_car in df_url_to_crawl['url']:
        df_zoe_tmp4 = pd.DataFrame(
            columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
                     'argus'])
        df_zoe_tmp4 = extract_characteristics(url_car, df_url_to_crawl[df_url_to_crawl['url'] == url_car]['region'])

        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'price'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'price'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'year'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'year'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'kilometrage'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'kilomtrage'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'version'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'version'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'telephone'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'telephone'].values
        # df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'description'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
        #    'description'].values

    return df_url_to_crawl


def export_data_car(df):
    path = os.path.realpath('')
    df.to_csv(path + '/data_set_zoe.csv', sep=';', header=True, index=False)


# Alimentation du dateframe initial
time_begin = time.time()
df_zoe = extract_urls_car(region_list_full, url_base)
time_end = time.time()
print('Temps execution f1 : {:.{prec}f}s'.format(time_end - time_begin, prec=4))
#   '{:_<10}'.format('test')

# print(extract_characteristics('https://www.leboncoin.fr/voitures/1035061660.htm?ca=12_s', 'ile_de_france'))



time_begin = time.time()
print(save_car_data(df_zoe))
time_end = time.time()
print('Temps execution f2 : {:.{prec}f}s'.format(time_end - time_begin, prec=4))

export_data_car(df_zoe)
print(df_zoe.count())