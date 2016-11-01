import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import json
import numpy as np

MAX_PAGE = 5

lacentrale = "http://www.lacentrale.fr/cote-voitures-renault-zoe--{}-.html"
leboncoin = "https://www.leboncoin.fr/_vehicules_/offres/{}/?o={}&q={}"


def processLeboncoinZOE(liste_region, search):

    search_tab = search.split(' ')
    query = search_tab[0]
    if (len(search_tab) > 1):
        for search_elem in search_tab[1:]:
            query += '%20' + search_elem

    car_list = []
    for region in liste_region:
        for page in range(1, MAX_PAGE + 1):
            req = leboncoin.format(region, page, query)
            print req
            response = requests.get(req)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print soup.prettify()
            # attrs={"aria-label": "Stargazers"}
            item_list = soup.find_all(
                "a", class_='list_item clearfix trackable')
            #pattern1 = r'<a>.*Renault ZOE ZEN.*<\/a>'
            #pattern2 = r'<a>(\d+)</td><td>(\w+)</td>\<td>(\w+)</a>'
            #item_list = re.findall(pattern1, response.text)
            # print len(item_list)
            if (len(item_list) == 0):
                break
            for item in item_list:
                item_infos = item.find(class_='item_infos')
                item_supp = item_infos.find(class_='item_supp')
                match_item = re.search(
                    r'Voitures', item_supp.text, re.IGNORECASE)
                if match_item:
                    car = {}
                    car_name = item.find(class_='item_title').text.strip()
                    car['name'] = car_name
                    item_link = item['href']
                    #item_link = re.search(r'www.*', item_link).group()
                    item_response = requests.get('https:'+item_link)
                    item_response_soup = BeautifulSoup(
                        item_response.text, 'html.parser')
                    # print item_response_soup.prettify()
                    price = item_response_soup.find(
                        class_='item_price').find("span", class_='value').text
                    car['price'] = re.search(
                        r'\d+\s\d+', price).group().replace(" ", "")
                    car_name_match = re.search(
                        r'Zen|Intens|Life', car_name, re.IGNORECASE)
                    if car_name_match:
                        car['version'] = car_name_match.group()
                    else:
                        car['version'] = 'N/A'
                    year = item_response_soup.find(
                        attrs={"itemprop": "releaseDate"}).text.strip()
                    car['year'] = year
                    kilo_balise = re.search(
                        r'<span.*>.*KM.*<\/span>', item_response.text, re.IGNORECASE).group()
                    car['mileage'] = re.search(
                        r'\d+\s\d*', kilo_balise).group().replace(" ", "")
                    match_type = re.search(
                        r'pro', item_supp.text, re.IGNORECASE)
                    if match_type:
                        car['type'] = 'Pro'
                    else:
                        car['type'] = 'Par'
                    # Lacentrale processing
                    lacentrale_response = requests.get(
                        lacentrale.format(car['year']))
                    lacentrale_response_soup = BeautifulSoup(
                        lacentrale_response.text, 'html.parser')
                    list_of_model = lacentrale_response_soup.find_all(
                        "div", class_="listingResultLine f14 auto")
                    ind_max_matching = -1
                    size_max_matching = -1
                    # print "   ----   "+car['name'].lower()
                    if (len(list_of_model) > 0):
                        ind_max_matching = 0
                        size_max_matching = len(list_of_model[0])
                        del list_of_model[0]
                    for ind, model in enumerate(list_of_model):
                        model_value = model.find(
                            "h3", class_="f14").text.strip()
                        # print model_value.lower()
                        if model_value.lower() in car['name'].lower():
                            if len(model_value) > size_max_matching:
                                ind_max_matching = ind
                                size_max_matching = len(model_value)
                    if (ind_max_matching >= 0):
                        # print "maximum:
                        # "+(list_of_model[ind_max_matching].find("h3", class_
                        # = "f14").text.strip())
                        cote_link = "http://www.lacentrale.fr/" + \
                            list_of_model[ind_max_matching].find("a")['href']
                        lacentrale_response_cote_brute = requests.get(
                            cote_link)
                        lacentrale_response_cote_brute_soup = BeautifulSoup(
                            lacentrale_response_cote_brute.text, 'html.parser')
                        # print lacentrale_response_cote_brute_soup.prettify()
                        cote_brute = lacentrale_response_cote_brute_soup.find(
                            'strong', class_="f24 bGrey9L txtRed pL15 mL15")
                        car['largusPrice'] = re.sub(
                            r'\D', "", cote_brute.text.strip())

                    car_list.append(car)

    return car_list

car_list = processLeboncoinZOE(['ile_de_france','aquitaine','provence_alpes_cote_d_azur'],'Renault Zoe')
df_car = pd.DataFrame(car_list, columns=[
                      'name', 'price', 'version', 'year', 'mileage', 'type', 'largusPrice', 'plus_chere_cote'])
df_car['plus_chere_cote'] = np.where(
    df_car['price'].astype(int) > df_car['largusPrice'].astype(int), 'vrai', 'Faux')
df_car.to_csv('Zoe.csv', index=False, encoding='utf-8')
