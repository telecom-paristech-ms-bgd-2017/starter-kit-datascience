from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

url = "https://gist.github.com/paulmillr/2657075"
html = urlopen(url)

obj = BeautifulSoup(html, "lxml")
id = list()
for link in obj.findAll('a', attrs={'href': re.compile("^https://")}):
    id.append(link.get_text())

pos = id.index('GrahamCampbell')
names = id[8:264]
names = [a for a in names if len(a) > 1]
names = [a for a in names if '.com' not in a]

Token = '5bb94d493aeaad4f4ddbf960eeb8168df761c3ec'
headers = {"Authorization": "token " + Token}

d = dict()
for name in names:
    url = "https://api.github.com/users/" + name + "/repos"
    request = requests.get(url, headers=headers)
    profil = request.json()
    tot_star = 0
    count = 0

    for i in range(len(profil)):
        tot_star += profil[i]['stargazers_count']
        mean_star = tot_star / len(profil)
    d[name] = mean_star

u = list(d.items())
final = pd.DataFrame(u, columns = ['Names', 'Stars'])
print(final.sort('Stars', ascending = False))


