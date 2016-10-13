# coding: utf8

"""

L'exercice pour le cours prochain est le suivant:
- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075
- En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens
de stars des repositories qui leur appartiennent. Pour finir classer ces 256 contributors par leur note moyenne.﻿
"""

import requests
import sys
import pandas
import re
from bs4 import BeautifulSoup

debug_this_sh = True


def view_tag(tag, n=0):
    """
    For debug, display tag content.
    """

    print(n * '\t' + '--------Tag--------')
    print(n * '\t', tag)
    print(n * '\t', '--------Tag Attributes--------')
    print(n * '\t', tag.attrs)
    print(n * '\t', '--------Tag String--------')
    print(n * '\t', tag.string)


def to_integer(tag):
    """
    To convert a string into integer and remove tricky chars from utf8.
    """

    return int(tag.text.replace('\xa0', '').replace(' ', ''))


def clean_string_to_float(in_string):
    """
    :param in_string: the string to clean, like "13€32" or "13,32"
    :return: 13.32
    """
    if len(in_string) > 0:
        out_string = in_string.replace(',', '.')
        out_string = out_string.replace('€', '.')
    else:
        out_string = '0'

    return out_string


def main():
    """

    Craw 2 pages from cdiscount to reveal the total item price and the average discount.
    vendor_list = {'acer', 'dell'} (you can add amstrad if you want)

    :return: nothing
    """

    # The base of the url
    url_full = 'https://gist.github.com/paulmillr/2657075'

    # Create soup
    soup = BeautifulSoup(requests.get(url_full).text, "html.parser")


    # Find the table in the page
    for tag_table in soup.find_all('table'):

        df_head = []

        # First create agnostically the DF and the header
        for tag_head in tag_table.find_all('thead'):
            for tag_th in tag_head.find_all('th'):
                if tag_th.get_text() in {'#', 'User', 'Contribs'}:
                    df_head.append(tag_th.get_text())
            df = pandas.DataFrame(columns=df_head)
            df_line_nb = -1

        for tag_body in tag_table.find_all('tbody'):
            # Then go through every line
            for tag_tr in tag_body.find_all('tr'):
                # A new line
                df_line_nb = df_line_nb + 1

                # Then go through every cells
                tag_th = tag_tr.find_all('th')
                df.loc[df_line_nb, '#'] = tag_th[0].get_text()

                tag_td = tag_tr.find_all('td')
                df.loc[df_line_nb, 'User'] = tag_td[0].get_text()
                df.loc[df_line_nb, 'Contribs'] = tag_td[1].get_text()

            print(df)


if __name__ == '__main__':
    main()