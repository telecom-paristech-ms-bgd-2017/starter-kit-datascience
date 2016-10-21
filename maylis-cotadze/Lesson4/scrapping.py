import requests
from bs4 import BeautifulSoup

url = ""

r = requests.get(url)

soup = BeautifulSoup(r.content)

links = soup.find_all("a")

for link in links:
    if "http" in links:
        print ("<a href='%s'>%s</a>"%(link.get("href"), link.text))

g_data = soup.find_all("div",{"class":"info"})

for item in g_data:
    #print item.contents # Separate the child element form the parent class (list of list)
    #print item.contents[0].text
    print item.contents[0].find_all({"a", "class":"business-name"})[0].text
    print item.contents[1].find_all("li",{"class": "adr"})[1].text
    
