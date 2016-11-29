import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import re

regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
pages = [1, 2]


def get_data(region, page):
    url = requests.get(
        'https://www.leboncoin.fr/voitures/offres/' + region + '/?o=' + str(page) + '&brd=Renault&mdl=Zoe')
    soup = BeautifulSoup(url.text, 'html.parser')

    links = []

    cars = map(lambda x: 'https:' + x['href'], soup.find_all(class_="list_item"))
    for link in cars:
        links.append(link)

    return links


def item_content(link):
    dic = {}
    result = requests.get(link)
    soup = BeautifulSoup(result.text, 'html.parser')
    car_p = soup.find_all(class_='property')

    for car_property in car_p:
        if car_property.text.lower() == 'prix':

            value = car_property.parent.find(class_='value').text.strip()
            regex = re.search('(\d* *\d*),?(\d*)', value)
            if regex == None:
                dic['Prix'] = None
            else:
                dic['Prix'] = float(regex.group(1).replace(' ', ''))

        if car_property.text.lower() == 'année-modèle':
            value = car_property.parent.find(class_='value').text.strip()
            dic['Année'] = int(value)

        if car_property.text.lower() == 'kilométrage':
            value = car_property.parent.find(class_='value').text.strip()
            regex = re.search('(\d* \d*)', value)
            if regex == None:
                dic['Km'] = None
            else:
                dic['Km'] = float(regex.group(1).replace(' ', ''))

        if car_property.text.lower() == 'description :':
            value = car_property.parent.find_all(class_='value')[0].text.strip()
            regex = re.search('(0|\+33)[1-9]([-. ]?[0-9]{2}){4}', value)
            if regex == None:
                dic['Phone'] = None
            else:
                dic['Phone'] = regex.group(0)

            regex = re.search('(LIFE|INTENS|ZEN)', value.upper())
            if regex == None:
                dic['Version'] = None
            else:
                dic['Version'] = regex.group(0).strip()

    isPro = (len(soup.find_all(class_="ispro")) > 0)
    if isPro == True:
        dic['Pro'] = 'Véhicule professionnel'
    else:
        dic['Pro'] = 'Véhicule particulier'

    return dic


def All_content(links):
    liste = []

    for link in links:
        liste.append(item_content(link))
    return DataFrame(liste)


def generate_csv(dataframe):
    dataframe.to_csv("Renault Zoé.csv")


all_links = []

for region in regions:
    for page in pages:
        all_links += get_data(region, page)

listeCars = All_content(all_links)
generate_csv(listeCars)
