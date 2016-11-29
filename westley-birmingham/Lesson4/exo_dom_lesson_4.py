import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import pylev
import pandas as pd
import re
import os
import matplotlib as plt
import seaborn


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

    vendeur_tmp = soup.find_all(class_='line line_pro noborder')[0].text
    if re.search("(?i)(Num(é|e)ro)( )*(SIREN)(\s*:*\s*)(?P<siren>\w+)", vendeur_tmp) is not None:
        vendeur = 'Numéro SIREN : ' + re.search("(?i)(Num(é|e)ro)( )*(SIREN)(\s*:*\s*)(?P<siren>\w+)", vendeur_tmp)\
            .group('siren')
    else:
        vendeur = 'Particulier'

    characteristics_price_tmp = (soup.find_all(class_='line')[2].text.replace(' ', '') \
                                .replace(u'\n', '').replace('nan', '') \
                                .replace('Prix', '').replace(u'\xa0', '').replace('€', ''))

    if re.search('([0-9]+)', characteristics_price_tmp) is not None:
        characteristics_price = float(re.search('([0-9]+)', characteristics_price_tmp).group(0))
    else:
        characteristics_price = 0


    characteristics_year_tmp = soup.find_all(class_='line')[6].text.replace(' ', '') \
                               .replace(u'\n', '').replace(u'\xa0', '').replace('Année-modèle', '')

    if re.search('([0-9]+)', characteristics_year_tmp) is not None:
        characteristics_year = re.search('([0-9]+)', characteristics_year_tmp).group(0)
    else:
        characteristics_year = 0


    characteristics_kilometrage_tmp = soup.find_all(class_='line')[7].text.replace('Kilométrage', '').replace('KM', '')\
        .replace(' ', '').replace(u'\n', '').replace(u'\xa0', '').replace(u'\t', '')

    if re.search('([0-9]+)', characteristics_kilometrage_tmp) is not None:
        characteristics_kilometrage = re.search('([0-9]+)', characteristics_kilometrage_tmp).group(0)
    else:
        characteristics_kilometrage = 0


    # commande synthetique
    #   .select(".tabscontent > ul > li > a")

    characteristics_version_full = soup.find_all(class_='no-border')[0].text

    # soup.text.replace(u'\n', '').replace(u'\t', '').strip()

    characteristics_description = soup.find_all(class_='line properties_description')[0].text.replace(u'\n', '') \
        .replace('Description :', '')

    if re.search('((0|\\+33|0033)[1-9][0-9]{8})|((0|\\+33|0033)[1-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})|((0|\\+33|0033)[1-9].[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2})', characteristics_description) is not None:
        tel_clean = re.search('((0|\\+33|0033)[1-9][0-9]{8})|((0|\\+33|0033)[1-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2})|((0|\\+33|0033)[1-9].[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]{2})', characteristics_description).group(0)
    else:
        tel_clean = 'NaN'



    if re.search('(INTENS|ZEN|LIFE)', characteristics_version_full.upper()) is not None:
        version_clean = re.search('(INTENS|ZEN|LIFE)', characteristics_version_full.upper()).group(0)
        if re.search('(TYPE(\s)?2)', characteristics_version_full.upper()) is not None:
            version_clean = version_clean + ' ' + re.search('(TYPE(\s)?2)', characteristics_version_full.upper()).group(0)
    else:
        if re.search('(INTENS|ZEN|LIFE)', soup.main.h1.text.upper()) is not None:
            version_clean = re.search('(INTENS|ZEN|LIFE)', soup.main.h1.text.upper()).group(0)
            if re.search('(TYPE(\s)?2)', soup.main.h1.text.upper()) is not None:
                version_clean = version_clean + ' ' + re.search('(TYPE(\s)?2)', soup.main.h1.text.upper()).group(0)
        else:
            version_clean = 'LIFE'


    df_zoe_tmp3 = df_zoe_tmp3.append([{'region': region_url,
                                       'url': url,
                                       'price': characteristics_price,
                                       'year': characteristics_year,
                                       'kilometrage': characteristics_kilometrage,
                                       'version': version_clean,
                                       'telephone': tel_clean,
                                       'description': characteristics_description,
                                       'vendeur': vendeur}], ignore_index=True)
    return df_zoe_tmp3


# Pool.map(extract_characteristics(), listURLGlob)

def save_car_data(df_url_to_crawl):
    for url_car in df_url_to_crawl['url']:
        df_zoe_tmp4 = pd.DataFrame(
            columns=['region', 'url', 'price', 'year', 'kilometrage', 'version', 'telephone', 'description', 'vendeur',
                     'argus'])
        df_zoe_tmp4 = extract_characteristics(url_car, df_url_to_crawl[df_url_to_crawl['url'] == url_car]['region'])

        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'price'] = float(df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'price'].values)
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'year'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'year'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'kilometrage'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'kilometrage'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'version'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'version'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'telephone'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'telephone'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'description'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'description'].values
        df_url_to_crawl.loc[df_url_to_crawl.url == url_car, 'vendeur'] = df_zoe_tmp4[df_zoe_tmp4['url'] == url_car][
            'vendeur'].values
    return df_url_to_crawl


def export_data_car(df):
    path = os.path.realpath('')
    df.to_csv(path + '/dataset_zoe.csv', sep=';', header=True, index=False)


# Récupérer toutes les versions existantes par année pour comparaison avec la description du boncoin
def get_argus(db_zoe):
    root_path = 'http://www.lacentrale.fr/'
    df_argus = pd.DataFrame(
        columns=['year', 'url_c', 'version', 'argus'])

    for el in db_zoe[['year']].drop_duplicates().values:
        if str(el[0])[:2] == '20' and el[0] != '':
            caract_year = str(el[0])
            url_global_search = 'http://www.lacentrale.fr/cote-voitures-renault-zoe--' + str(el[0]) + '-.html'

            reqests_glob = requests.get(url_global_search)
            glob_soup = BeautifulSoup(reqests_glob.text, "html.parser")

            for el_tmp in glob_soup.find_all(class_="listingResultLine f14 auto"):
                caract_url = el_tmp.a.attrs['href']
                caract_version = el_tmp.a.h3.text

                url_tmp = root_path + caract_url
                requests_argus_tmp = requests.get(url_tmp)
                argus_soup_tmp = BeautifulSoup(requests_argus_tmp.text, "html.parser")
                argus_price_tmp = (argus_soup_tmp.find_all("strong", class_="f24")[0].text.replace(' ', '') \
                                         .replace(u'\n', '').replace('nan', '') \
                                         .replace('Prix', '').replace(u'\xa0', '').replace('€', ''))

                if re.search('([0-9]+)', argus_price_tmp) is not None:
                    argus_price = float(re.search('([0-9]+)', argus_price_tmp).group(0))
                else:
                    argus_price = 0

                print(str(caract_year) + ' : ' + str(caract_version) + ' : ' + str(url_tmp) + ' : ' + str(argus_price))
                df_argus = df_argus.append([{'year': caract_year
                                                , 'url_c': url_tmp
                                                , 'version': caract_version
                                                , 'argus': argus_price}]
                                                , ignore_index=True)

    path = os.path.realpath('')
    df_argus.to_csv(path + '/dataset_argus_zoe.csv', sep=';', header=True, index=False)
    return df_argus

# Mise à jour du Dataframe zoe avec l'argus avec le calcul de la distance Levenshtein
def maj_argus_zoe(db_zoe, df_argus):
    for el in db_zoe['id']:
        text_description = db_zoe[db_zoe['id'] == el]['description'].values
        text_version = db_zoe[db_zoe['id'] == el]['version'].values
        year_tmp = db_zoe[db_zoe['id'] == el]['year'].values[0]
        if str(year_tmp)[:2] == '20' and year_tmp != '':
            df_argus_tmp = df_argus[df_argus.year == year_tmp]
        else:
            df_argus_tmp = df_argus

        for el_argus in df_argus_tmp['version'].values:
            df_argus_sub_tmp = df_argus_tmp

            # Recherche de la version de zoe 'La centrale' la plus proche de la version leboncoin (titre/decription)
            df_argus_tmp.loc[df_argus_tmp.version == el_argus, 'select'] = pylev.levenshtein(text_description, str(el_argus))
            df_argus_sub_tmp.loc[df_argus_sub_tmp.version == el_argus, 'select'] = pylev.levenshtein(text_version,
                                                                                             str(el_argus))
            df_argus_fin_tmp = df_argus_tmp.append(df_argus_sub_tmp)
            distance_min = df_argus_fin_tmp['select'].min()

            argus_price = df_argus_fin_tmp[df_argus_fin_tmp['select'] == distance_min]['argus'].values[0]
            db_zoe.loc[db_zoe.id == el, 'argus'] = float(argus_price)
            db_zoe.loc[db_zoe.id == el, 'official_version'] = el_argus
    return db_zoe

# Indicateur de bonnes affaires
def select_good_deal(db_zoe_to_select):
    db_zoe_to_select['good_deal'] = db_zoe_to_select['price'] / db_zoe_to_select['argus']
    db_zoe_to_select['select_deal'] = db_zoe_to_select['good_deal'].apply(lambda x: True if x < 1 else False)
    return db_zoe_to_select




# Alimentation du dateframe initial
df_zoe = extract_urls_car(region_list_full, url_base)
df_zoe_more = save_car_data(df_zoe)

df_argus = get_argus(df_zoe_more)

df_zoe_maj = maj_argus_zoe(df_zoe_more, df_argus)

df_zoe_final = select_good_deal(df_zoe_maj)
export_data_car(df_zoe_final)

print(df_zoe_final)
print(df_zoe.count())
print(df_zoe.corr())



