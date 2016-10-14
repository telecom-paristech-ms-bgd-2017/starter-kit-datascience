import requests
from bs4 import BeautifulSoup
import numpy as np
import json
from multiprocessing import Pool

# En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories
# qui leur appartiennent. Pour finir classer ces 256 contributors par leur note moyenne.﻿

GITHUB_API = 'https://api.github.com'

def getBeautifulSoupObjectfromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_gt_users():
    url = 'https://gist.github.com/paulmillr/2657075'
    bs = getBeautifulSoupObjectfromUrl(url)
    table = bs.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    users = []
    for row in rows:
        cols = row.find_all('td')
        c = cols[0]
        name = c.next.text
        users.append(name)
    return users


def get_git_user_repos_average_stars(user_name):
    headers_credentials = {'Authorization': 'token {0}'.format(TOKEN)}
    url = 'https://api.github.com/users/{}/repos'.format(user_name)
    repos = requests.get(url, headers=headers_credentials)
    repos_info = json.loads(repos.text)
    stars = []
    for ri in repos_info:
        try:
            stars.append(ri['stargazers_count'])
        except:
            pass
    if len(stars) > 0:
        return user_name, np.mean(stars)
    else:
        return user_name, -1


def get_git_info_parallel():

    users = get_gt_users()
    pool = Pool()
    return pool.map(get_git_user_repos_average_stars, users)


# Main script :

TOKEN = input('Token :')
data = get_git_info_parallel()
res = sorted(data, key=lambda d: d[1], reverse=True)
print("Number of results : {0}".format(len(res)))
print("")
for r in res:
    print("User : {0}. Avg stars : {1}".format(r[0], r[1]))
