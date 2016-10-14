from bs4 import BeautifulSoup
import requests
import json
import pandas as import pd
import numpy as np

r = requests.get("https://gist.github.com/paulmillr/2657075")
soup = BeautifulSoup(r3.text, 'html.parser')
nl = soup.find_all('tr')
names=[]

for line in nl :
    temp = line.find('td')
    temp2 = temp.find('a')
    names.append(temp2.string)
    
