from __future__ import division
from collections import defaultdict
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, json, sys
from operator import itemgetter

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

def contributor_stars(contributor):
    repos = json.loads(api_get_repos(contributor))
    total_stars = sum([repo['stargazers_count'] for repo in repos])
    return (contributor, total_stars / len(repos))

def add_stars(contributor_stars):
    global stars
    stars[contributor_stars[0]] = contributor_stars[1]


#########
# UTILS #
#########
def api_get_repos(contributor):
    url = 'https://api.github.com/users/' + contributor + '/repos'
    resp = requests.get(url, auth=(username, password))
    if resp.status_code != 200:
        print(json.loads(resp.text)['message'])
        resp.raise_for_status()
    return resp.text

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
    global stars
    repos_per_contributor = {}
    contributors = best_contributors("paulmillr/2657075")

    pool = Pool(30)
    for contributor in contributors:
        args = {'args': (contributor,), 'callback': add_stars}
        pool.apply_async(contributor_stars, **args)
    pool.close()
    pool.join()

    sorted_stars = sorted(stars.items(), key=itemgetter(1), reverse=True)

    i = 1
    for contributor, avg_stars in sorted_stars:
        print((str(i) + ') ' + contributor).ljust(20) + ": {s:.2f}".format(s=avg_stars))
        i += 1

if __name__ == '__main__':
    set_credentials()
    main()