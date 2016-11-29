import requests
from bs4 import BeautifulSoup

#Accept: application/vnd.github.v3+json


def findUsers(soup_tbody):
    usersDictionary = {}
    for el in soup_tbody.find_all('tr'):
        user = el.find_all('td')[0].find('a').text
        usersDictionary[user] = 0
    return usersDictionary

def extractUsersMeanStars():
    usersDictionary = {}
    url = 'https://gist.github.com/paulmillr/2657075'
    result = requests.get(url).text
    soup = BeautifulSoup(result, 'html.parser')
    soup_tbody = soup.tbody
    usersDictionary = findUsers(soup_tbody)
    i = 1
    for el in usersDictionary:
        usersDictionary[el] = round(float(extractUsersStars(el)), 2)
        print(str(i) + ' - ' + el + ' : ' + str(round(float(extractUsersStars(el)), 2)))
        i += 1
    return usersDictionary

# Récupération du nombre de stars moyen par contributeur
def extractUsersStars(username):
    token = getMyToken()
    user = 'westleyb'
    stars_mean_total = 0.0
    stars_mean = 0.0
    nb_stars_count = 0
    result = requests.get('https://api.github.com/users/' + str(username) + "/repos", auth=(user, token))
    # print(result)
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

# Récupération du token GitHub
def getMyToken():
    return open('/Users/Wes/CloudStation/big_data/MSBGD/6-INFMDI721-Kit_Big_data/token_github.txt', 'r').read()



users_dic = extractUsersMeanStars()
users_dic = sorted(users_dic.values(), reverse=True)
print(users_dic)
print()
''''
i = 1
print('Contributors sorted by average star count')
for el in users_dic:
    print(str(i) + ' - ' + str(el) + ' : ' + str(users_dic[el]))
    i += 1
'''
# print(sorted(users_dic, key=users_dic.__getitem__, reverse=True))
