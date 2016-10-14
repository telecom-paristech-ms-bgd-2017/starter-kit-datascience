import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import operator

Token = "b919878cf4d9f39e156eb1c1aa6bf4fc0d602baa"


def extract_from_url(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find_all('table')[0]
    return table 


def extract_users(table):
    users = []
    for i in range(1, 257):
        #print(str(i) + ' : ' + table.find_all('tr')[i].find('td').text.replace('\xa0', '').split()[0])
        users.append(table.find_all('tr')[i].find('td').text.replace('\xa0', '').split()[0])
    return users


def average_stars(user):
    nb_stars = 0.0
    nb_repos = 0.0

    url = "https://api.github.com/users/" + user + "/repos"
    repos = requests.get(url=url, headers={"Authorization": "token " + Token})
    repos_user = json.loads(repos.text)

    for repo in repos_user:
        nb_stars += repo['stargazers_count']
        nb_repos += 1

    try:
        average_star = nb_stars / nb_repos
    except ZeroDivisionError:
        average_star = 0

    return round(average_star,2)


def results_average_stars(users):

    results = {}
    for user in users:
        results[user] = average_stars(user)

    return results



if __name__ == "__main__":
    url = 'https://gist.github.com/paulmillr/2657075'
    users = extract_users(extract_from_url(url))
    Resultat = results_average_stars(users)

    Resultat = OrderedDict(sorted(Resultat.items(), key=operator.itemgetter(1), reverse=True))

    for user, avg_star in Resultat.items():
        print( user +" had " + str(avg_star) + " stars per repository")


