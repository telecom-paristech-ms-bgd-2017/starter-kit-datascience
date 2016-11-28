# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Author Manu
"""

import requests
from bs4 import BeautifulSoup

def getTop256contributors():
    page_contributors = requests.get("https://gist.github.com/paulmillr/2657075")
    soup_contributors = BeautifulSoup(page_contributors.text, 'html.parser')
    print(soup_contributors.prettify())
    list_contributors = map(lambda x: x['href'] , soup_contributors.find_all(class_='tbody'))
    print(list_contributors)
    return

getTop256contributors()
