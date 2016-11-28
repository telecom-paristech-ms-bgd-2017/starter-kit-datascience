from __future__ import unicode_literals

import requests
from bs4 import BeautifulSoup
import locale
import os
import sys
import unicodedata
import pandas as pd
import numpy as np
import json

#!/usr/bin/env python3
#"""
#Get the mean number of stars among the most active GitHub users.
#Persist data in two files:
#- data.csv: all repositories for each GitHub contributor
#- data-sorted.csv: sorted contributors by mean number of stars by repository.
#"""


def extract_user_list_using_returning_dict(in_url, in_nombre):
    model_name = []
    metrics = {}

    result = requests.get(in_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for key in range(1, in_nombre + 1):
        model_name = soup.find_all('tr')[key].get_text().replace(',', '.').split(' ')
        metrics[key] = model_name[2]

        # print(metrics.values())

    return (metrics)


def extract_user_list_using_DataFrame(url0,nombre):

    model_name = []
    df = pd.DataFrame(model_name, index=range(1, 257), columns=['pos', 'user'])

    result = requests.get(url0)
    soup = BeautifulSoup(result.text, 'html.parser')
    for key in range(1, nombre + 1):
        model_name = soup.find_all('tr')[key].get_text().replace(',', '.').split(' ')
        df.pos[key] = key
        df.user[key] = model_name[2]

    return (df)



if __name__ == "__main__":

    total_user = 256
    url_users = 'https://gist.github.com/paulmillr/2657075'

    # getting user list from a Dictionnary Datas
    tableau_from_dict = extract_user_list_using_returning_dict(url_users,total_user)
    datFrame_tableau_from_dict = pd.DataFrame(tableau_from_dict,index = range(1,257), columns=['pos','user'])
    datFrame_tableau_from_dict.pos = tableau_from_dict.keys()
    datFrame_tableau_from_dict.user = tableau_from_dict.values()

    #getting user list from a DataFramme Datas
    tableau_from_DataFrame = extract_user_list_using_DataFrame(url_users, total_user)
    #print '=========Liste from Dictionnary datas \n', datFrame_tableau_from_dict
    print('*********Liste from DataFramme datas\n', tableau_from_DataFrame.head(10))

    # https://github.com/settings/tokens/new for sucribing the OAuth Key
    url_api = 'https://api.github.com/users/'
    key = '7e4fb621a8c145096988ad4e8dcc7c7742b81fc8'
    authkey = ('sidoinis', key)

    resp = requests.get(url= url_api, auth = authkey)
    data = json.loads(resp.text)

    #for user in tableau_from_DataFrame.user:

    for user in tableau_from_DataFrame.user[:1]:
        url_xuser = url_api + user
        resp = requests.get(url=url_xuser, auth=authkey)
        data = json.loads(resp.text)

        #resp_i = requests.get(url=data['starred_url'], auth=authkey)
        resp_i = requests.get(url='https://api.github.com/users/GrahamCampbell/starred', auth=authkey)#????????
        data_tot = json.loads(resp_i.text)

        print (data_tot)

    print (data)
    print (data['starred_url'])
    print ('\ntotal repos ' +str(user)+' = ',data['public_repos'])
    print ('\nfollowers_total ' +str(user)+ ' = ',data['followers'])


    #for user in liste_user