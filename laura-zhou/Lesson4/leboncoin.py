import urllib.request
from bs4 import BeautifulSoup 
import requests 
import pandas as pd


# url ile de france renault zoe
url_ile_de_france = "https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&parrot=0&brd=Renault&mdl=Zoe"
url_aquitaine = "https://www.leboncoin.fr/voitures/offres/aquitaine/?th=1&parrot=0&brd=Renault&mdl=Zoe"

url = url_ile_de_france
s = urllib.request.urlopen(url).read()

#make soup
soup = BeautifulSoup(s,"html.parser")
res=soup.find_all("ul")  
