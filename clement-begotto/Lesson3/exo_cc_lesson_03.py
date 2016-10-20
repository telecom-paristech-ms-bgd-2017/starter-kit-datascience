# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

data = {'brand': [], 'price': [], 'old_price': []}
brands = ['dell', 'acer']
for i in range(1, 4):
    for brand in brands:
        cdiscount = requests.get('http://www.cdiscount.com/search/10/' +
                                 brand + '+ordinateur+portable.html?&page=' + str(i))
        soup = BeautifulSoup(cdiscount.text, 'html.parser')

        for elt in soup.find_all(class_='prdtBloc'):

        	curr_line = elt.find_all(class_='prdtPrSt')

        	if curr_line != [] and curr_line[0].text != '':

        		old_price = float(elt.find_all(class_='prdtPrSt')[
                                  0].text.replace(',', '.'))
        		new_price = float(elt.find_all(class_='prdtPrice')[0].text[
                                  :-3] + '.' + elt.find_all(class_='prdtPrice')[0].text[-2:])
        		data['brand'].append(brand)
        		data['price'].append(new_price)
        		data['old_price'].append(old_price)

df = pd.DataFrame(data)
df['reduction'] = (df['old_price'] - df['price']) / df['old_price']
print(df)
print('\nAverage reducation for Dell : ' +
      str(np.mean(df[df['brand'] == 'dell']['reduction']) * 100))
print('Average reducation for Acer : ' +
      str(np.mean(df[df['brand'] == 'acer']['reduction']) * 100))

df.to_csv('cdiscount.csv')
