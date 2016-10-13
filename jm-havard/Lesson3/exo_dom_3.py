
# coding: utf-8

# In[1]:


import requests
#import json
#import numpy as np
#import requests.auth
#import operator
from bs4 import BeautifulSoup
#from collections import OrderedDict

#Token = "f6b118221bc4d142dbf582caef4fcead69e1a000"
#GITHUB_API = 'https://api.github.com'


#********************** Partie 1 : Crawling pour recupperer les noms des users
url = 'https://gist.github.com/paulmillr/2657075'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

table = soup.find("table")
rows = list()
columns = []
names = []

for row in table.find_all("tr"):
    rows.append(row)

for row in rows:
    columns.append(row.find_all("td"))

columns.pop(0)

for column in columns:
    names.append(column[0].text.split()[0].replace(u'\xe9', '').replace(
        u'\u0142', '').replace(u'\u0144', ''))

print(names)
#
#**************************** Partie 2 : Moyenne nombre étoiles de chaque user
#headers = {"Authorization": "token " + Token}

#dictionary = {}
#for name in names:
#    stars = []

    # Get all repos for one user
#    url = GITHUB_API + "/users/" + name + "/repos"
#    print(url)
#    r = requests.get(url=url, headers=headers)
#    repos_data = json.loads(r.text)
#    for data in repos_data:
#        stars.append(data['watchers_count'])
#    mean_stars = (np.mean(stars))
#    dictionary[name] = mean_stars

#sorted_dictionary = OrderedDict(
#    sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True))

#print("Les utilisateurs les mieux etoiles : \n")

#del sorted_dictionary['jfrazelle']

#for keys, values in sorted_dictionary.items():
#    print(str(keys) + " : " + str(values))


# In[2]:

len(names)


# In[ ]:



