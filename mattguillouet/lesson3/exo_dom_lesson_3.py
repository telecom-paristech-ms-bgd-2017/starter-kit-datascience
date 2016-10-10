import requests
import sys
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
import ipdb
from requests.auth import HTTPBasicAuth


url = 'https://gist.github.com/paulmillr/2657075'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

rowContribs = soup.select('table > tbody > tr')

contribList = []
for contrib in rowContribs:
    ranking = re.search('#(\d+)', contrib.select('th:nth-of-type(1)')[0].text.strip()).group(1)

    username_name = contrib.select('td:nth-of-type(1)')[0].text.strip()
    username_re = re.search('(\w+) \((.+)\)', username_name)

    if username_re is not None:
        username = username_re.group(1).strip()
        name = username_re.group(2).strip()
    else:
        username = username_name.strip()
        name = ''

    location = contrib.select('td:nth-of-type(3)')[0].text.strip()
    nbContribs = contrib.select('td:nth-of-type(2)')[0].text.strip()

    tmpDict = {'ranking': ranking, 'username': username, 'name': name, 'location': location, 'nbContribs': nbContribs}
    contribList.append(tmpDict)


gitAPIUrl = 'https://api.github.com/'
gitGetRepos = 'users/{0}/repos'
gitGetRepoInfo = 'repos/{0}/{1}'
nbPeople = len(contribList)

token = '0b1212b57d80525a7ab538c625551449cb4e08a6'
username_gitAPI = 'matthibou'

auth = {'X-Github-Username': username_gitAPI, 'X-Github-API-Token': token}

for contrib in contribList:
    repos = requests.get(gitAPIUrl + gitGetRepos.format(contrib['username'].strip()), auth=HTTPBasicAuth(username, token))

    strR = 'request {0}/{1} for {2}'.format(contrib['ranking'], nbPeople, contrib['username'])
    print('{:100s}'.format(strR), end='\r')
    if repos.status_code == 200:
        jsonRepos = json.loads(repos.text)
        nbRepo = len(jsonRepos)
        nbStars = 0
        for repo in jsonRepos:
            nbStars += repo['stargazers_count']

        if not nbRepo == 0:
            contrib['meanStars'] = nbStars / nbRepo
        else:
            contrib['meanStars'] = 0
    else:
        print('Warning !!! HTTP status = {0} for {1}'.format(repos.status_code, contrib['name']))

# sort contrib list
contribList = sorted(contribList, key=lambda x: x['meanStars'], reverse=True)


print('-------------------Top 20 of the best contributors on GitHub-------------------')
print('computed with the mean of stars on their public repositories\n')
for ii in range(20):
    idUser = '{:}. {:}, {:}'.format(ii + 1, contribList[ii]['name'], contribList[ii]['location'])
    idGit = 'Username: {:}, Nb Contribs {:}, Mean Stars {:.1f}'.format(contribList[ii]['username'], contribList[ii]['nbContribs'], contribList[ii]['meanStars'])
    print('{:50s} |   '.format(idUser) + idGit)
