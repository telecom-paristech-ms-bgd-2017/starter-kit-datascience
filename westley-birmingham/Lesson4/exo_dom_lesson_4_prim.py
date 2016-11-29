import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import pylev
import seaborn as sns
import numpy as np


db_zoe = pd.read_csv('dataset_zoe.csv', delimiter=';')
df_argus = pd.read_csv('dataset_argus_zoe.csv',delimiter=';')

'''
for id_car in db_zoe['id']:
    km = db_zoe[db_zoe['id'] == id_car]['kilometrage'].values[0]
    year = db_zoe[db_zoe['id'] == id_car]['year'].values[0]
    type = db_zoe[db_zoe['id'] == id_car]['version'].values[0].replace('2', ' 2').replace(' ', '+')

    url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + str(type).lower() + '-' + str(year) + '.html'
    print(url)
'''
print()

''''
db_zoe['good_deal'] = db_zoe['price']/db_zoe['argus']
db_zoe['test'] = db_zoe['good_deal'].apply(lambda x: True if x < 1 else False)
'''

''''
url2 = 'http://www.lacentrale.fr/cote_proxy.php?km=5567&month=01'
payload = {'km': str(km), 'month': '01'}
requests.get(url, params=payload)
'''


# print(BeautifulSoup(argus_request.content, "html.parser").find_all("strong", class_="f24"))
#argus_soup = BeautifulSoup(argus_request.text, "html.parser")
# argus_price_tmp =
#print(argus_soup.strong.find_all(class_='f24'))
#.find_all("strong", class_="f24")[0].text
#print(argus_price_tmp)
''''
db_zoe.loc[db_zoe.url == url_car, 'argus'] = db_zoe[db_zoe['url'] == url_car][
        'price'].values
'''



#######################################################################################################################

import matplotlib.pyplot as plt




df = db_zoe[['argus', 'price']]
df = df.drop_duplicates(['argus', 'price'])
df.plot.hist(normed=False, alpha=0.4, legend=False)
# db_zoe.hist(db_zoe, 'argus', 'price', bins=20)


#######################################################################################################################

''''
    payload = {
        'env_channel': "d",
        'env_template': "category",
        'env_work': "prod",
        'page_cat1':"auto",
        'page_cat2':"cote",
        'page_cat3':"",
        'page_error':"",
        'page_level':9,
        'page_name':"DetailCote::Occasion",
        'page_url':url,
        'user_quotation_prolile':"acheteur",
        'announce_km':str(km)
    }
'''
