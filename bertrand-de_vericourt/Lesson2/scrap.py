#from lxml import html
import requests
from bs4 import BeautifulSoup

# une API permet de donner accès aux ressources de manières programmatiques, 
# pour éviter les surcharges dues aux scrap

r = requests.get('https://www.youtube.com/watch?v=kOkQ4T5WO9E')

# on cherche "parse html python" >> on tombe sur BeautifulSoup


soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())
# Display nb of views

def getViews(soup, className):
	res_str = soup.find('div', class_=className).text.replace('\xa0','').replace('vues','')
	res = int(res_str)
	return res

def getLikesDislikes(soup, className, position):
	soup.find('span', class_=className).find('span', class_="yt-uix-button-content").text.replace('\xa0', '')
	res_str = soup.find_all(class_=className)[position].text.replace('\xa0','')
	res = int(res_str)
	return res

Views = getViews(soup, 'watch-view-count')
Likes = getLikesDislikes(soup, 'like-button-renderer', 0)
Dislikes = getLikesDislikes(soup, 'like-button-renderer', 1)

print("views: " + Views)
print("Likes: " + Likes)
print("Dislikes: " + Dislikes)