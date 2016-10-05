import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.youtube.com/watch?v=mbDnymjtVKg")
soup = BeautifulSoup(result.text, "html.parser")

balise = str(soup.find(class_="watch-view-count").text).replace('\xa0', '').replace('vues', '')
print(balise)
