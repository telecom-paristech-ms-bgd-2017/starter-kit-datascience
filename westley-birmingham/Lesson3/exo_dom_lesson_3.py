import requests
#from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup
import os
from requests_oauthlib import OAuth1
from urllib2 import urlopen, Request

#Accept: application/vnd.github.v3+json




#requests.get('https://gist.github.com/paulmillr/2657075', auth=HTTPBasicAuth('user', 'pass'))



def findUsers(soup_tbody):
    usersDictionary = {}
    for el in soup_tbody.find_all('tr'):
        #soup_td = soup_tbody.find_all('td')
        print(el.find_all('td')[0].find('a').text)
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

# test connexion 1
def extractUsersStars():
    token = '40af341916805f9e563bbfccc96ed3ce897a4f7b'
    user = 'westleyb'
    url = 'https://gist.github.com/paulmillr/2657075'

    r = requests.get('https://api.github.com/users/GrahamCampbell/repos', auth=('westleyb', '40af341916805f9e563bbfccc96ed3ce897a4f7b'))
    r.json()



    ########

    # url = 'https://github.com/login/oauth/access_token'
    # auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
    #                   'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')

    # urll = '"Authorization: token OAUTH-TOKEN" https: // api.github.com'
    # rezl = requests.get(urll, auth=(user, token))
    # print(rezl)




    # os.path.dirname(os.path.realpath('__file__'))
    # token = open('../token_github.txt', 'r').read()
    # print(token)
    # username + ':' + token + ' https://api.github.com/GrahamCampbell'
    # GitHub(access_token='abc1234567xyz')~


#url = 'https://gist.github.com/paulmillr/2657075'
#auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
#                  'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')

#result =  requests.get(url, auth=auth)

#soup = BeautifulSoup(result, 'html.parser')
