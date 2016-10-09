#Récupérer les 256 top contributors de https://gist.github.com/paulmillr/2657075
import requests
from bs4 import BeautifulSoup
import github3 as gh3
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
gh = gh3.login('rvi008',input('pw :'))
rvi = gh.user()
baseUrl = 'https://api.github.com/repos'
rank = []
for user in names:
    repos = gh3.iter_user_repos(user, type = 'owner')
    starcount = []
    for repo in repos:
        req = requests.get(baseUrl+'/'+str(repo)).text
        result = json.loads(req)
        print(result)
        sc = int(result['stargazers_count'])
        starcount.append(sc)
    avgsg = np.mean(starcount)
    print(avgsg)
    rank = rank.append([user, avgsg])
sorted_rank = rank.sort(key=lambda x: x[1])
print(sorted_rank)