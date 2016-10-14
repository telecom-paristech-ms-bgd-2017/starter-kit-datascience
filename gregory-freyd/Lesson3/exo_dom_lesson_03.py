import requests
from bs4 import BeautifulSoup
import json
import numpy as np

def getTopContributors(limit):
    # Returns list of the top Github contriutor logins
    all_contributors_request = requests.get("https://gist.github.com/paulmillr/2657075")
    all_contributors_soup = BeautifulSoup(all_contributors_request.text, 'html.parser')
    list_contributors_table = all_contributors_soup.find_all('tbody')
    list_contributors = list_contributors_table[0].find_all('tr')
    contributor_logins = []

    for contributor, index in zip(list_contributors, range(limit)):
        contributor_login = contributor.find('a').text.replace(u'\xa0', '')
        contributor_logins.append(contributor_login)
    return contributor_logins

def rankContributors(list_contributor_logins):
    token_from_user = input('token :')
    connection_string = {'Authorization': 'token ' + token_from_user}
    baseUrl = 'https://api.github.com'
    average_star_ranking = []
    for login in list_contributor_logins:
        repos_request = requests.get(baseUrl + '/' + 'users/' + login + '/' + 'repos', headers=connection_string)
        repos_list = json.loads(repos_request.text)
        star_ranking = []
        for repo in repos_list:
            star_ranking.append(float(repo['stargazers_count']))
        average_star_ranking.append([login, round(np.mean(star_ranking), 2)])
    average_star_ranking.sort(key=lambda x: x[1], reverse=True)

    return average_star_ranking


top_contributors_list = getTopContributors(256)
average_star_ranking = rankContributors(top_contributors_list)
global_rank = 1
for login in average_star_ranking:
    print('#' + str(global_rank) + ' Contributor: ' + login[0] + ' Average stars : ' + str(login[1]))
    global_rank += 1
