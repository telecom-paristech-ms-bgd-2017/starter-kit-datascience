import requests
from bs4 import BeautifulSoup
import sys
import numpy as np

URL = "https://gist.github.com/paulmillr/2657075"
def loadHTML():
    resultats = requests.get(URL)
    return BeautifulSoup(resultats.text, 'html.parser')

def getUsers():
    soup_git = loadHTML()
    users = []
    contribs = []
    tab = soup_git.find_all('tr')
    for i in range(1, len(tab)):
        users.append(tab[i].find_all("td")[0].text.split(' ')[0])
        contribs.append(tab[i].find_all("td")[1].text.split(' ')[0])

    return (users, contribs)

def viewUsers():
    users,contribs = getUsers()
    for i in range(len(users)):
        print("User "+str(i)+" : "+users[i]+", Contributions : "+str(contribs[i]))

def api():
    users,contribs = getUsers()
    token = "71b67aa555c42d2efcc0d6927f481b8120bb7a73"
    headers = {"Authorization": "token " + token}
    dico = {}
    for user in users :
        r = requests.get("https://api.github.com/users/"+user+"/repos", headers=headers)
        profil = r.json()
        stars = []
        for item in profil :
            stars.append(item["stargazers_count"])
        if (len(stars) == 0):
            dico[user] = 0
        else :
            dico[user] = sum(stars)/len(stars)

    return dico
print(api())
