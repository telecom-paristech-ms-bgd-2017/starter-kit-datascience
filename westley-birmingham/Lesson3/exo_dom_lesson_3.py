import requests
#from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup
import os
from requests_oauthlib import OAuth1
# from urllib2 import urlopen, Request

#Accept: application/vnd.github.v3+json




#requests.get('https://gist.github.com/paulmillr/2657075', auth=HTTPBasicAuth('user', 'pass'))



def findUsers(soup_tbody):
    usersDictionary = {}
    for el in soup_tbody.find_all('tr'):
        #soup_td = soup_tbody.find_all('td')
        #print(el.find_all('td')[0].find('a').text)
        user = el.find_all('td')[0].find('a').text
        usersDictionary[user] = 0
    return usersDictionary

def extractUsersMeanStars():
    usersDictionary = {}
    result = requests.get('https://gist.github.com/paulmillr/2657075').text
    soup = BeautifulSoup(result, 'html.parser')
    soup_tbody = soup.tbody
    usersDictionary = findUsers(soup_tbody)
    # print(soup_tbody.find_all('tr')[0].find_all('td'))
    for el in usersDictionary:
        usersDictionary[el] = float(extractUsersStars(el))
    print(sorted(usersDictionary, key=usersDictionary.__getitem__, reverse=True))
    return usersDictionary

# test connexion 1
def extractUsersStars(username):
    #token = '40af341916805f9e563bbfccc96ed3ce897a4f7b'
    token = getMyToken
    user = 'westleyb'
    url = 'https://gist.github.com/paulmillr/2657075'
    stars_mean_total = 0.0
    stars_mean = 0.0
    nb_stars_count = 0
    result = requests.get('https://api.github.com/users/' + str(username) + '/repos', auth=('westleyb', '40af341916805f9e563bbfccc96ed3ce897a4f7b'))
    #print(result)
    for el in result.json():
        for el2 in el:
            if el2 == 'stargazers_count':
                stars_mean += int(el['stargazers_count'])
                nb_stars_count += 1

    if nb_stars_count > 0:
        stars_mean_total = stars_mean / nb_stars_count
    else:
        stars_mean_total = 0
    return stars_mean_total


def getMyToken():
    return open('/Users/Wes/CloudStation/Big Data/Master Spe BGD/6 - INFMDI 721 - Kit Big data/token_github.txt', 'r').read()

extractUsersMeanStars()