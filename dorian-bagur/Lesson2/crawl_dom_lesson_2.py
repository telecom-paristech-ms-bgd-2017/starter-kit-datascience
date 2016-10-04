import requests
from bs4 import BeautifulSoup


result = requests.get('https://www.youtube.com/watch?v=kOkQ4T5WO9E')
soup = BeautifulSoup(result.text, "html.parser")


def extractTitle(soup):
    return soup.title.text


def extractViews(soup):
    return int(soup.find(class_="watch-view-count").text.replace("vues", "")
               .replace("\xa0", ""))

print("Title: " + extractTitle(soup))
print("Number of views: " + str(extractViews(soup)))
