from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
#@ MahzadK October 2016

def extractNameFromGit() :
    r3 = requests.get("https://gist.github.com/paulmillr/2657075")
    soup = BeautifulSoup(r3.text, 'html.parser')
    cells = soup.find_all('th', { 'scope' : 'row' })

    listeNom=[]
    for cell in cells:
        sibling = cell.findNextSibling ()
        listeNom.append(sibling.findNext('a').contents[0]) # pour afficher que les noms
     #listeNom.append(sibling.findNext('a')) #pour afficher les liens avec les noms
    return listeNom


def CountStars(name) :
    sum=0
    authentification = {'Authorization': 'token %s' % '063a434006ff262948b25f1fa91fe4f624db54ff'}
    urlRepos = 'https://api.github.com/users/' + name + '/repos'
    rGit = requests.get(urlRepos, headers=authentification)
    data = json.loads(rGit.text)
    temp = [float(data[i]['stargazers_count']) for i in range(len(data)) ]
    return np.mean(temp)



# Main Programm
listeNom = []
listeNom= extractNameFromGit()
df =  pd.DataFrame([listeNom])
df =  df.T
df.to_csv('out.csv', sep =';')

listeMoyenne =[]
for nom in listeNom :
    moy = CountStars(nom)
    listeMoyenne.append(moy)

d = {'nom': listeNom, 'moyenne': listeMoyenne }

df2 = pd.DataFrame(data=d).sort('moyenne', ascending=False)
df2.to_csv('res2.csv', sep =';')
