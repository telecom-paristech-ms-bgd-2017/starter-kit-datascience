#!/usr/bin/env python3

# standard library imports
import sys
import json
import itertools
import re

# related third party imports
import requests
import pandas
import configparser
from bs4 import BeautifulSoup


class ScrapingBonCoin:
    FILE = 'renaud-zoe-car-leboncoin-fr.csv'
    URL = 'https://www.leboncoin.fr/voitures/offres/{area}/'

    def __init__(self):
        pass

    class Car:

        def __init__(self):
            self.id = None
            self.link = None
            self.version = None
            self.km = None
            self.price = None
            self.phone_owner = None
            self.is_pro_owner = None
            self.is_expensive = None

    # public methods

    @staticmethod
    def get(area):
        options = {'area': area}
        url = ScrapingBonCoin.URL.format(**options)
        params = {'q': 'Renault Zoé'}
        result = requests.get(url, params=params)
        bs = BeautifulSoup(result.text, 'html.parser')
        markup_items = bs.find('section', class_='tabsContent') \
            .find('ul', recursive=False)
        items = []
        for item in markup_items.find_all('li', recursive=False):
            print(ScrapingBonCoin._get_id(item))
            items.append(item)
        return items

    @staticmethod
    def _get_id_and_link(self, li_elt):
        pass

    @staticmethod
    def _get_price(li_elt):
        pass

    @staticmethod
    def _get_name(li_elt):
        pass

    @staticmethod
    def _is_pro(li_elt):
        pass

    @staticmethod
    def persist(item):
        if len(item) == 0:
            return pandas.DataFrame()
        item_dicts = [item.__dict__ for item in item]
        columns = list(item_dicts[0].keys())
        df = pandas.DataFrame(item_dicts, columns=columns)
        df.to_csv(ScrapingBonCoin.FILE, index=False)
        return df


if __name__ == '__main__':
    ScrapingBonCoin.get('provence_alpes_cote_d_azur')
