# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:02:21 2016

@author: arthurouaknine
"""

from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import pandas as pd


def getNames():
    url = 'https://gist.github.com/paulmillr/2657075'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    body = soup.find('tbody').find_all('tr')
    names = []
    for dude in body:
        infos = []
        infos.append(str(dude.a.next_sibling).replace('(', '').replace(')', '').strip(' '))
        infos.append(str(dude.a).replace('</a>','').split('>')[1])
        names.append(infos)
    return names


def getRepo(name):
    authentification = {'Authorization': 'token %s' % 'f3c3f17a15d97ecef34c2345521fa1b4721f7281'}
    urlRepos = 'https://api.github.com/users/' + str(name) + '/repos'
    read = requests.get(urlRepos, headers=authentification)
    if(read.ok):
        dataRepo = json.loads(read.text or read.content)
    else:
        dataRepo = 'not found'
    return dataRepo


def getMeanStar(listRepo):
    listStars = []
    if type(listRepo) != str:
        for repo in listRepo:
            listStars.append(float(repo['stargazers_count']))
        return np.mean(listStars)
    else:
        return listRepo


def getUsersStars(names):
    dicoOfUsersStars = {}
    for name in names:
        repos = getRepo(name[1])
        dicoOfUsersStars[name[1]] = getMeanStar(repos)
    result = pd.Series(dicoOfUsersStars)
    return result.sort_values(axis=0, ascending=False)

print(getUsersStars(getNames()))
