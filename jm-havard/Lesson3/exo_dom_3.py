
# coding: utf-8

# In[3]:


import requests

from bs4 import BeautifulSoup

# n'etant pas a l'aise sur python 
# je me suis inspiré du programme d'un de mes camarades 
# qui m'a paru assez simple 
# je le completerai plus tard pour essayer de recuper le reste de l'exercice

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


# In[2]:

len(names)


# In[ ]:



