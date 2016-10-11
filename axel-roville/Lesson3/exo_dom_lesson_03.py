from __future__ import division
from collections import defaultdict
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, json, sys
from operator import itemgetter
import threading, time

######################
# VARIABLES GLOBALES #
######################
stars = defaultdict(lambda: 0)
username = None
password = None
pool_busy = True

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

def add_stars(contributor_stars):
    global stars
    stars[contributor_stars[0]] = contributor_stars[1]


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

def animateWaiting():
    idx = 0
    anim = "|/-\\"
    start_time = time.time()
    while pool_busy:
        t = time.time() - start_time
        sys.stdout.write(anim[idx % len(anim)] + " {t:2.1f}".format(t=t) + "\r")
        idx += 1
        time.sleep(0.1)
    return

########
# MAIN #
########
def main():
    global stars
    global pool_busy
    repos_per_contributor = {}

    t = threading.Thread(target = animateWaiting)
    t.start()

    contributors = best_contributors("paulmillr/2657075")

    pool = Pool(len(contributors))
    for contributor in contributors:
        args = {'args': (contributor,), 'callback': add_stars}
        pool.apply_async(contributor_stars, **args)
    pool.close()
    pool.join()
    pool_busy = False
    t.join()

    sorted_stars = sorted(stars.items(), key=itemgetter(1), reverse=True)

    i = 1
    for c, avg in sorted_stars:
        print((str(i) + ') ' + c).ljust(22, '.') + ": {s:.2f}".format(s=avg))
        i += 1

if __name__ == '__main__':
    set_credentials()
    main()