# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:34:44 2016

@author: Stephan
"""

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

authentification = {'Authorization': 'token %s' % 'e1eb47220603d6c1648c2d53a88060e3b3e61e7a'}

#def getContent():

result = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(result.text, 'html.parser')
name_lines = soup.find_all('tr')
names = []

#def extractNameFromDOM(soup):

for line in name_lines:
    if line.find('td') is not None:
        temp = line.find('td')
        temp2 = temp.find('a')
        names.append(temp2.string)

title = soup.title.text
print('=====')
print(title)

#data = getContent()
#results = extractNameFromDOM(data)
#s = pd.DataFrame(results, range(256))
#print(s)
        
def get_star(name):
    url = 'https://api.github.com/users/' + name + '/repos'
    jsonData = requests.get(url, headers = authentification)
    jsonToPython = json.loads(jsonData.text)
    star = [jsonToPython[i]['stargazers_count'] for i in range(len(jsonToPython))]
    return np.mean(star)

stars= []
for name in names:
    stars.append(get_star(name))
    
dico = {'Names': names, 'Average Stars': stars}
df = pd.DataFrame(data = dico, index = None)
result = df.sort_values('Average Stars', ascending = False)

print(result)

