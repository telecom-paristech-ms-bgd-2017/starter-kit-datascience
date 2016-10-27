import requests
from bs4 import BeautifulSoup

#Accept: application/vnd.github.v3+json


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
        usersDictionary[el] = round(float(extractUsersStars(el)), 2)
    return usersDictionary

# test connexion 1
def extractUsersStars(username):
    token = getMyToken
    user = 'westleyb'
    url = 'https://gist.github.com/paulmillr/2657075'
    stars_mean_total = 0.0
    stars_mean = 0.0
    nb_stars_count = 0
    result = requests.get('https://api.github.com/users/' + str(username) + '/repos', auth=(user, token))
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


usersDic = extractUsersMeanStars()
print(sorted(usersDic, key=usersDic.__getitem__, reverse=True) + '\n')