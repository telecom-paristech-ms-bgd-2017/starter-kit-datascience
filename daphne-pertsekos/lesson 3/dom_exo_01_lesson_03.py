from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import pandas as pd
import numpy as np

authentification = {'Authorization': "token {}".format('12705e58d107678d6c910cf49c7feee706f0239e')}

def get_DOM(url):
    html_doc = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def get_names(soup):
    article = soup.find("div", {'id':"readme"})
    users = article.find("table").find_all("tr")
    names = []
    for user in users[1:]:
        names.append( user.td.a.text)
    return names

def get_star(name):
    url = 'https://api.github.com/users/' + name + '/repos'

    jsonData = requests.get(url, headers=authentification)
    jsonToPython = json.loads(jsonData.text)
    star = [jsonToPython[i]['stargazers_count'] for i in range(len(jsonToPython))]
    return np.mean(star)


url ="https://gist.github.com/paulmillr/2657075"
soup = get_DOM(url)
names = get_names(soup)
print("names shape : {}".format(len(names)))

stars = []
for name in names:
    stars.append(get_star(name))

d = {'Names': names, 'Average Stars': stars}
df = pd.DataFrame(data=d, index=None)
result = df.sort_values('Average Stars', ascending=False)

print("Classement")
print(result)

