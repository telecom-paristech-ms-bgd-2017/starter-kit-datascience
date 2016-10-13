# coding: utf8

"""
Comme exercice pour jeudi je vous demande de crawler le résultat des comptes
de la ville de Paris pour les exercices 2009 à 2013.
Voici par exemple les comptes pour 2013 .
Je vous demande de récupérer les données A,B,C et D sur les colonnes Euros
par habitant et par strate.
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
    base_url = 'http://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-'

    # Vendor list
    vendor_list = {'acer', 'dell', 'apple'}

    # A counter per laptop, per brand
    laptop_number = -1

    # This DF will contain the result of the crawl
    df = pandas.DataFrame(columns=['Vendor', 'Model', 'Initial Price', 'Final Price'])

    for vendor_name in vendor_list:

        # Crawl in the 9 first pages
        for page_num in range(1, 3):
            # Display vendor
            print(vendor_name," page ", page_num)

            # Full ur www.....html?page=1
            url_full = base_url + vendor_name + '.html?page=' + str(page_num)

            # Create soup
            soup = BeautifulSoup(requests.get(url_full).text, "html.parser")

            # This contains the relevant 'class'
            for tag_tr in soup.find_all('div'):

                # Find the correct class
                if 'class' in tag_tr.attrs:

                    if tag_tr.attrs['class'][0] == "prdtBTit":
                        # Init the line
                        laptop_number = laptop_number + 1
                        df.loc[laptop_number, 'Vendor'] = vendor_name
                        df.loc[laptop_number, 'Model'] = tag_tr.get_text()
                        df.loc[laptop_number, 'Initial Price'] = 0
                        df.loc[laptop_number, 'Final Price'] = 0

                    if tag_tr.attrs['class'][0] == "prdtPrSt":
                        df.loc[laptop_number, 'Initial Price'] = float(clean_string_to_float(tag_tr.get_text()))

                    if tag_tr.attrs['class'][0] == "prdtPrice":
                        df.loc[laptop_number, 'Final Price'] = float(clean_string_to_float(tag_tr.get_text()))

                        # No discounted laptop have only Final Price, let's update Initial Price
                        if df.loc[laptop_number, 'Initial Price'] == 0:
                            df.loc[laptop_number, 'Initial Price'] = df.loc[laptop_number, 'Final Price']


    for vendor_name in vendor_list:
        # Final result per vendo
        initial_price = df[df['Vendor'] == vendor_name]['Initial Price'].sum()
        final_price = df[df['Vendor'] == vendor_name]['Final Price'].sum()

        # Display
        print("Initial Price", vendor_name, "\t\t\t", initial_price)
        print("Final Price", vendor_name, "\t\t\t", final_price)
        print("Discount", vendor_name, "\t\t\t", 1 - final_price / initial_price)

    sys.exit(1)

if __name__ == '__main__':
    main()