from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

# replace 'my key " by 7a0fee0f5a7b5ec182dcd0d0189b2384ac225fd2

authentification = {'Authorization': 'token %s' % 'my key'}

r3 = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(r3.text, 'html.parser')
name_lines = soup.find_all('tr')
names=[]

for line in name_lines:
    if line.find('td') is not None:
        temp=line.find('td')
        temp2=temp.find('a')
        names.append(temp2.string)


def get_star(name):
    url = 'https://api.github.com/users/' + name + '/repos'
    jsonData = requests.get(url, headers=authentification)
    jsonToPython = json.loads(jsonData.text)
    star = [jsonToPython[i]['stargazers_count'] for i in range(len(jsonToPython))]
    if star not empty:
        return np.mean(star)
    else:
        return 0


stars=[]
for name in names:
    stars.append(get_star(name))
    
d = {'Names': names, 'Average Stars': stars}
df = pd.DataFrame(data=d, index=None)
result = df.sort_values('Average Stars',ascending=False)

print result
    
    