

import requests
from lxml import html
import re
import pandas as pd
import numpy as np

lst = list()

regions = ['ile_de_france', 'aquitaine', 'nord_pas_de_calais']
for region in regions:
    for i in range(1, 20):

        url_listing = 'https://www.leboncoin.fr/voitures/offres/{}/?o={}&q=zoe&it=1'.format(
            region, i)
        base = requests.get(url_listing)
        tree_base = html.fromstring(base.content)
        car_add = tree_base.xpath(
            '//section[@class="tabsContent block-white dontSwitch"]//a/@href')

        for add in car_add:
            url = 'https:' + add
            page = requests.get(url)
            tree = html.fromstring(page.content)

            prices = tree.xpath(
                '//*[@id="adview"]/section/section/section[2]/div[4]/h2/span[2]/text()')
            px = str(prices).split()
            px = ''.join(px)
            price = re.search(r'\d+', px)
            if price is not None:
                price = int(re.search(r'\d+', px).group())

            years = tree.xpath(
                '//*[@id="adview"]/section/section/section[2]/div[8]/h2/span[2]/text()')
            yrs = str(years).split()
            yrs = ''.join(yrs)
            year = re.search(r'\d+', yrs)
            if year is not None:
                year = int(re.search(r'\d+', yrs).group())

            kilometers = tree.xpath(
                '//*[@id="adview"]/section/section/section[2]/div[9]/h2/span[2]/text()')
            kiloms = str(kilometers).split()
            kiloms = ''.join(kiloms)
            km = re.search(r'\d+', kiloms)
            if km is not None:
                km = int(re.search(r'\d+', kiloms).group())

            models = tree.xpath('//*[@id="adview"]/section/header/h1/text()')
            models = str(models).split()
            models = ''.join(models).lower()

            types = ['zen', 'intens', 'life']
            mod = ''.join([typ for typ in types if typ in models])

            data = {'Model': mod, 'Prix': price, 'Année': year, 'Km': km}
            lst.append(data)

table = pd.DataFrame(lst)
table['Argus'] = ""

lst2 = list()
# print(table)
count = -1
for index, row in table.iterrows():
    count += 1
    if (~np.isnan(row['Année']) and len(row['Model']) > 0):
        b = int(row['Année'])
        a = row['Model']

        url_arg = 'http://www.lacentrale.fr/cote-auto-renault-zoe-{}+charge+rapide-{}.html'.format(
            a, b)
        arg = requests.get(url_arg)
        arg_base = html.fromstring(arg.content)
        argus_dat = arg_base.xpath(
            '/html/body/section/section[2]/div[1]/div[2]/div[1]/div[1]/div[1]/strong/text()')
        argus = str(argus_dat).split()
        argus = ''.join(argus)
        argus = re.search(r'\d+', argus)
        if argus != None:
            table['Argus'].iloc[count] = argus.group()

print(table)
