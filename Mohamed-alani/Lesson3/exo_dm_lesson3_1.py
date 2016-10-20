import requests
from bs4 import BeautifulSoup
import sys

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
viewUsers()
