import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def getSoupUrl(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup

def extractListContributors(soup):
    for i in range(1,256):
        contributorsTab = pd.DataFrame(soup.find_all(scope="row"))
        return contributorsTab

soupUrl = getSoupUrl('https://gist.github.com/paulmillr/2657075')
contrib_rows = extractListContributors(soupUrl)
print(contrib_rows)
