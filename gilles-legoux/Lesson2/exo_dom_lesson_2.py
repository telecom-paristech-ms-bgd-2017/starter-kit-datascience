#!/usr/bin/env python2
# encoding: utf-8
# execute: ./exo_dom_lesson_2.py

import re
import requests
from bs4 import BeautifulSoup
import sys


def number(string):
    return int(''.join(re.findall('\d+', string)))


def extractTableElement(soup):
    table = soup.find_all('table', attrs={'width': '100%'})
    return table[1]


def extractFromCellElement(table, r_pos, c_pos):
    return table.find_all('tr', recursive=False)[r_pos] \
        .find_all('td', recursive=False)[c_pos].contents[0]


def extractMultipleDataFromRow(table, r_pos):
    return {
        'title': str(extractFromCellElement(table, r_pos, 3)),
        'per_inhabitant': number(extractFromCellElement(table, r_pos, 1)),
        'per_area': number(extractFromCellElement(table, r_pos, 2))
    }


def extractDataFromPage(url, params):
    try:
        result = requests.get(url, params=params)
        soup = BeautifulSoup(result.text, 'html.parser')
        table = extractTableElement(soup)
        a = extractMultipleDataFromRow(table, 5)
        b = extractMultipleDataFromRow(table, 9)
        c = extractMultipleDataFromRow(table, 17)
        d = extractMultipleDataFromRow(table, 22)
        return a, b, c, d
    except IndexError:
        sys.stderr.write('ERROR: no data for url {}.\n'.format(result.url))
        return ()


def extractData(years):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php'
    params = {'icom': '056', 'type': 'BPS', 'param': '5', 'dep': '075'}
    for year in years:
        print('*** Comptes de la ville de Paris pour {} ***'.format(year))
        params['exercice'] = str(year)
        print(extractDataFromPage(url, params))


if __name__ == "__main__":
    extractData(range(2009, 2016))
