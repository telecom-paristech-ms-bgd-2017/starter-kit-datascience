from __future__ import division
import requests
from operator import itemgetter
import json
import sys
from collections import defaultdict
from pprint import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool

##############
# CONSTANTES #
##############
users_api_url = 'https://api.github.com/users/'
repos_api_url = 'https://api.github.com/repos/'

######################
# VARIABLES GLOBALES #
######################
stars = defaultdict(lambda: 0)
username = None
password = None

#############
# FONCTIONS #
#############
def best_contributors(gist):
    url = 'https://gist.github.com/' + gist;
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    rows = soup.select('#readme table tr')[1:]
    return [r.select('td:nth-of-type(1) > a')[0].text for r in rows]

def contributor_repos(contributor):
    url = users_api_url + contributor + '/repos'
    return [repo['name'] for repo in json.loads(api_get(url))]

def get_stars(contributor, repo):
    resp = api_get(repos_api_url + contributor + '/' + repo + '/stargazers')
    return (contributor, len(json.loads(resp)))

def add_stars(contributor_stars):
    global stars
    stars[contributor_stars[0]] += contributor_stars[1]


#########
# UTILS #
#########
def api_get(url):
    return requests.get(url, auth=(username, password)).text

def set_credentials():
    try:
        cred = json.loads(open('credentials.json').read())
        global username
        global password
        username, password = cred['username'], cred['password']
        if not username or not password:
            raise Exception
    except Exception:
        print('You must provide your GitHub credentials in "credentials.json"')
        print('Template: {"username":"<username>", "password":"<password>"}')
        sys.exit(1)

########
# MAIN #
########
def main():
    set_credentials()

    global stars
    repos_per_contributor = {}
    for contributor in best_contributors("paulmillr/2657075"):
        repos = contributor_repos(contributor)
        repos_per_contributor[contributor] = len(repos)

        with Pool(30) as pool:
            for repo in repos:
                args = {'args': (contributor, repo), 'callback': add_stars}
                pool.apply_async(get_stars, **args)
            pool.close()
            pool.join()

        stars[contributor] /= len(repos)

    sorted_stars = sorted(stars.items(), key=itemgetter(1), reverse=True)
    for contributor, avg_stars in sorted_stars:
        print(contributor.ljust(20) + ": {s:.2f}".format(s=avg_stars))

if __name__ == '__main__':
    main()