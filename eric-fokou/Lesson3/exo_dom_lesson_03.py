import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

MAX_PAGE = 2
API_GITHUB = 'https://api.github.com'


def get_github_token():
    with open('token.txt') as f:
        return f.read()


def getListRepository():
    return


def AVG_star(user):


    url = API_GITHUB+'/users/{}/repos'.format(user)
    headers = {'Authorization': 'token {0}'.format(token_git)}

    star = 0
    count = 0

    #API VERSION
    response = requests.get(url, headers=headers)
    repositories = json.loads(response.text)

    for repository in repositories:
        try:
            star = star + repository['stargazers_count']
            count = count + 1
        except:
            continue
    if count == 0:
        return 0
    else:
        return star / count

    # Beautiful soup version (passer le user_link en parametre a la place)
    #for page in range(1, MAX_PAGE + 1):
    #    
    #    if (page == 1):
    #        r = requests.get(
    #            user_link+"?tab=repositories", headers=headers)
    #    else:
    #        params = {'page': page}
    #        r = requests.get(
    #            user_link+"?tab=repositories", params=params, headers=headers)
    #    soup = BeautifulSoup(r.text, 'html.parser')
    #    # print soup.prettify()
    #    repo_list = soup.find_all("a", attrs={"aria-label": "Stargazers"})
    #    for repo in repo_list:
    #        # print int(re.findall('\d+', repo.contents[2])[0])
    #        star = star + int(re.findall('\d+', repo.contents[2])[0])
    #        count = count + 1

    if count == 0:
        return -1
    else:
        return star / count

token_git = get_github_token()

r = requests.get('https://gist.github.com/paulmillr/2657075',
                 auth=('ericfokou', 'Fodebert161090'))
soup = BeautifulSoup(r.text, 'html.parser')
contributors = []
for i in range(256):
    contributor = {}
    contrib = soup.find("th", string="#"+str(i+1)).parent
    contributor['Rang'] = i+1
    contributor['user'] = contrib.find("a").string
    contributor['user_link'] = contrib.find("a")['href']
    contributor['contrib'] = contrib.find_all("td")[1].string
    contributor['location'] = contrib.find_all("td")[2].string
    contributor['AVG_star'] = AVG_star(contributor['user'])
    print contributor
    contributors.append(contributor)


df_contributors = pd.DataFrame(
    contributors, columns=['Rang', 'user', 'user_link', 'contrib', 'location', 'AVG_star'])
df_contributors = df_contributors.sort(columns="AVG_star", ascending=False)
print df_contributors.ix[0:5]
df_contributors.to_csv('Contributors.csv', index=False, encoding='utf-8')
