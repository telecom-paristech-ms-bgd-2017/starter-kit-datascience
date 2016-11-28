import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def getBestContributors():
    req = requests.get('https://gist.github.com/paulmillr/2657075')
    soup = BeautifulSoup(req.text, 'html.parser')
    names = {}

    for contributor in soup.find('tbody').find_all('tr'):  # .next_sibling
        usrname = str(contributor.a).split('>')[1].replace('</a', '').strip()
        names[usrname] = stargazers_avg(usrname)

    return names


def stargazers_avg(usrname):
    my_token = ''
    rq_headers = {'Authorization': 'token %s' % my_token}
    api_url = 'https://api.github.com/users/' + usrname + '/repos'
    result = requests.get(api_url, headers=rq_headers)
    stars = []
    if(result.ok):
        all_repos = json.loads(result.text or result.content)
        for repo in all_repos:
            stars.append(repo['stargazers_count'])
        return np.mean(stars)
    else:
        return -1


print(best_contributors_stars) = pd.Series(getBestContributors()).sort_values(axis=0, ascending=False)