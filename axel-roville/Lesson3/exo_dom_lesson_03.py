from __future__ import division
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, json, sys
from operator import itemgetter

######################
# VARIABLES GLOBALES #
######################
token = None

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

    try:
        return (contributor, total_stars / len(repos))
    except ZeroDivisionError:
        print("User {u} doesn't own any repo, moving on.".format(u=contributor))
        return(contributor, 0)


#########
# UTILS #
#########
def api_get_repos(contributor):
    url = 'https://api.github.com/users/' + contributor + '/repos'
    resp = requests.get(url, params=token)
    if resp.status_code != 200:
        print(json.loads(resp.text)['message'])
        resp.raise_for_status()
    return resp.text

def set_credentials():
    global token
    token = json.loads(open('credentials.json').read())

########
# MAIN #
########
def main():
    contributors = best_contributors("paulmillr/2657075")

    with Pool(len(contributors)) as pool:
        stars = pool.map(contributor_stars, contributors)

    i = 1
    for c, avg in sorted(stars, key=itemgetter(1), reverse=True):
        print((str(i) + ') ' + c).ljust(22, '.') + ": {s:.2f}".format(s=avg))
        i += 1

if __name__ == '__main__':
    set_credentials()
    main()