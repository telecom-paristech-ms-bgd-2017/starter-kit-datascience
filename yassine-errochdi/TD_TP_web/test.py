from bs4 import BeautifulSoup
import requests

r = requests.get("https://www.youtube.com/watch?v=DSHin9S7sx8")

soup = BeautifulSoup(r.text, 'html.parser')
balise = soup.find(class_='')

print(soup.title)
