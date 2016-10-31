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


def getContent():
    result = requests.get("https://gist.github.com/paulmillr/2657075")
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup

    
def extractNameFromDOM(soup):
    res_str = soup.find_all("tr") 
    tab_users = []
    for element in res_str:
        if element.find('td') is not None:
            temp=element.find('td')
            temp2=temp.find('a')
            tab_users.append(temp2.string)
    title = soup.title.text
    print('=====')
    print(title)        
    return tab_users

data = getContent()
results = extractNameFromDOM(data)
s = pd.DataFrame(results, range(256))
print(s)

#API not yet done...