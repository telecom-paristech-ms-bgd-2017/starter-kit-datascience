

import requests
from bs4 import BeautifulSoup

result = requests.get('https://www.youtube.com/watch?v=34Na4j8AVgA').text

#print(result)

soup = BeautifulSoup(result, 'html.parser')
print(soup.title)
number_view = int(soup.find(class_='watch-view-count').text.replace('vues','').replace('\xa0',''))
print(number_view)
# def extractIntFromDOM(soup, classname):
#     res_str =  soup.find(class=classname).text.replace(u'\xa0','').replace('vues','')
#     res = int(res_str)
#     return res

# def extractLikeDislikeFromDOM(soup, classname, position):
#     res_str =  soup.find(class=classname)[position].find(class_="yt-uix-button-content")
#     res = int(res_str)
#     return res

# def computeIndicatorForPage():





