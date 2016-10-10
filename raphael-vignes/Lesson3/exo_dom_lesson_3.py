#Récupérer les 256 top contributors de https://gist.github.com/paulmillr/2657075
from __future__ import division
import requests
from bs4 import BeautifulSoup
import json
import numpy as np


def getSoup(url):
    request = requests.get(url)
    result_soup = BeautifulSoup(request.text,'html.parser')
    return result_soup

def getBody(soup):
    body = soup.find("tbody")
    return body

def getTr(body_soup):
    trList = body_soup.find_all("tr")
    return trList

def getName256(trList):
    name_list = []
    for tr in trList:
        name = tr.text.split(' ')[2]
        name_list.append(name[: tr.text.find('(')])
    return name_list

test = getBody(getSoup("https://gist.github.com/paulmillr/2657075"))
test_tr = getTr(test)
names = getName256(test_tr)
for name in names:
    print(name)

#Using Github API get number of stars for each of their repositories


#Authentication


#Retrieving infos

token = input('token :')
credentials = {'Authorization':'token '+token}
baseUrl = 'https://api.github.com'
rank = []
for user in names:
    repos = requests.get(baseUrl+'/'+'users/'+user+'/'+'repos', headers = credentials)
    result = json.loads(repos.text)
    starcount = []
    for repo in result:
        sc = float(repo['stargazers_count'])
        starcount.append(sc)
    avgsg = np.mean(starcount)
    rank.append([user, avgsg])
rank.sort(key=lambda x: x[1], reverse = True)
i = 1
for user in rank:
    print('#'+str(i)+' User: ' + user[0] + ' Average stars : ' + str(user[1]))
    i +=1