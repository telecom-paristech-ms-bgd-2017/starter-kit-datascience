#! /usr/bin/python3.5
import requests
from bs4 import BeautifulSoup
import pandas as pd
from os import getenv
import os.path as osp

users_url = 'https://gist.github.com/paulmillr/2657075'
api_url = 'https://api.github.com'

results_users = requests.get(users_url)
soup = BeautifulSoup(results_users.text, 'html.parser')


def get_top_users():
    users = []
    # Get text of the first 'a' tag every 4 'td' of 'tbody'
    for i, column in enumerate(soup.tbody.find_all("td")):
        if(i % 4 == 0):
            users.append(soup.tbody.find_all('td')[i].a.text)
    return users


def get_average_stars(username):
    print('Getting average stars for user: ' + username)

    stars = 0
    avg = 0

    #  [Using personal token as temporary auth method]
    token_path = osp.join(getenv('HOME'),'github/token')
    try:
        file = open(token_path, 'r')
    except:
        print("Error while opening ~/github/token file: please get a personal token and save it in ~/github/token")
    personal_token = file.readline()[0:40]

    rep_data_list = requests.get(
        api_url + '/users/' + username + '/repos',
        headers={'Authorization': 'token %s' % personal_token}).json()

    for i, repository in enumerate(rep_data_list):
        stars += rep_data_list[i].get('stargazers_count')
        try:
            avg = float(stars / len(rep_data_list))
        except:
            print("Exception")
            continue
    print(avg)
    return(avg)

# MAIN

avg_stargazers = []
top_users = get_top_users()
for u, username in enumerate(top_users):
    avg = get_average_stars(username)
    avg_stargazers.append(avg)

df = pd.DataFrame()
df['Users'] = top_users
df['Avg_stargazers'] = avg_stargazers
df.to_csv('./github_top.csv')
print(df.sort_values(by='Avg_stargazers'))
