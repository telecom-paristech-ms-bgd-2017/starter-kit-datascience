#!/usr/bin/env python3

# standard library imports
import re

# related third party imports
import requests
import pandas
from bs4 import BeautifulSoup


def _number(string):
    return int(''.join(re.findall('\d+', string)))


class ScrapingLeBonCoin:
    FILE = 'renault-zoe-leboncoin-fr.csv'
    URL = 'https://www.leboncoin.fr/voitures/offres/{area}/'

    def __init__(self):
        pass

    class Car:
        def __init__(self, id, link, location, is_pro):
            self.id = id
            self.link = link
            self.location = location
            self.is_pro_owner = is_pro
            self.version = None
            self.year = None
            self.km = None
            self.price = None
            self.phone_owner = None
            self.is_expensive = None

        def set_car(self, car_link):
            result = requests.get(car_link)
            bs = BeautifulSoup(result.text, 'html.parser')
            lines = bs.find_all('div', class_='line')
            self.km = ScrapingLeBonCoin.Car._get_km(lines)
            self.price = ScrapingLeBonCoin.Car._get_price(lines)
            self.year = ScrapingLeBonCoin.Car._get_year(lines)

        @staticmethod
        def _get_km(lines):
            return _number(lines[6].find('span', class_='value').contents[0])

        @staticmethod
        def _get_price(lines):
            return _number(lines[1].find('span', class_='value').contents[0])

        @staticmethod
        def _get_year(lines):
            return _number(lines[5].find('span', class_='value').contents[0])



    # public methods

    @staticmethod
    def get(area):
        options = {'area': area}
        url = ScrapingLeBonCoin.URL.format(**options)
        params = {'q': 'Renault Zoé'}
        result = requests.get(url, params=params)
        bs = BeautifulSoup(result.text, 'html.parser')
        markup_items = bs.find('section', class_='tabsContent') \
            .find('ul', recursive=False)
        cars = []
        for li_elt in markup_items.find_all('li', recursive=False):
            _id, link = ScrapingLeBonCoin._get_id_and_link(li_elt)
            is_pro = ScrapingLeBonCoin._is_pro(li_elt)
            car = ScrapingLeBonCoin.Car(_id, link, area, is_pro)
            car.set_car(car.link)
            cars.append(car)
        return cars

    # private methods

    @staticmethod
    def _get_id_and_link(li_elt):
        text = li_elt.find('a')['href']
        text = re.sub(r'\?.*$', '', text)
        link = 'https:{}'.format(text)
        match = re.search(r'\/(\d+)', text)
        _id = match.group(1)
        return _id, link

    @staticmethod
    def _is_pro(li_elt):
        return li_elt.find('span', class_='ispro') is not None

    @staticmethod
    def persist(cars):
        if len(cars) == 0:
            return pandas.DataFrame()
        car_dicts = [car.__dict__ for car in cars]
        columns = list(car_dicts[0].keys())
        df = pandas.DataFrame(car_dicts, columns=columns)
        df.to_csv(ScrapingLeBonCoin.FILE, index=False)
        return df


if __name__ == '__main__':
    areas = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']
    cars = []
    for area in areas:
        cars.extend(ScrapingLeBonCoin.get(area))
    ScrapingLeBonCoin.persist(cars)
