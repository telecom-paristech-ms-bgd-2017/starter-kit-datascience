# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 19:12:09 2016

@author: Antoine
"""

import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def getBestContributors():
    req = requests.get('https://gist.github.com/paulmillr/2657075')
    soup = BeautifulSoup(req.text, 'html.parser')
    names = {}

    for contributor in soup.find('tbody').find_all('tr'):
        username = str(contributor.a).split('>')[1] \
                       .replace('</a', '') \
                       .strip()
        names[username] = stargazers_avg(username)

    return names


def stargazers_avg(username):
    with open('API_GitHub.txt', 'r') as APIfile:
        my_token = APIfile.read().replace('\n', '')

    rq_headers = {'Authorization': 'token %s' % my_token}
    # api_url = 'https://api.github.com/users/{}/repos'.format(username)
    api_url = 'https://api.github.com/users/' + username + '/repos'
    r = requests.get(api_url, headers=rq_headers)
    stars = []
    if(r.ok):
        all_repos = json.loads(r.text or r.content)

        # peut être parallléliser avec pool.map()
        for repo in all_repos:
            stars.append(repo['stargazers_count'])
        return np.mean(stars)
    else:
        return -1


contributors_sortedBy_stars = pd.Series(getBestContributors()) \
                              .sort_values(axis=0, ascending=False)
