
import requests
from bs4 import BeautifulSoup as bs4
import numpy as np
import json
import pandas as pd
from IPython.display import display


def getNames(url):

    result = requests.get(url)
    soup = bs4(result.text, 'html.parser')

    allTr = soup.find_all('tr')
    allNames = []
    for ii in allTr[1:]:
        obj = ii.find('td')
        temp = obj.text
        allNames.append(temp[0: temp.find('(')].strip())
    print(str(len(allNames)))
    print(str(allNames))
    return allNames


def getStars(baseUrl, finRepo, allNames, auth):

    allStars = pd.DataFrame(columns=['Contributors', 'Stars'])
    for ii in list(enumerate(allNames)):
        print('Scanning n0 ' + str(ii[0]) + ' : ' + ii[1])
        urlRep = baseUrl + finRepo.replace('<user>', ii[1])
        resp = requests.get(urlRep, auth=auth)
        allJson = json.loads(resp.text)
        count_Star = 0
        for jj, kk in enumerate(allJson):
            count_Star += kk['stargazers_count']
        if jj != 0:
            count_Star = np.round(count_Star / jj)
        else:
            count_Star = 0
        temp = [ii[1], count_Star]
        allStars.loc[ii[0]] = temp

    allStars.sort_values('Stars', ascending=False, inplace=True)
    return allStars


url = 'https://gist.github.com/paulmillr/2657075'
baseUrl = 'https://api.github.com/'
finRepo = "users/<user>/repos"
token = "c337552fc71ad17d08e09a4091c8bbbc79a32db0"
auth = ('jibeka', token)

allNames = getNames(url)
allStars = getStars(baseUrl, finRepo, allNames, auth)
display(allStars.head(1))
