import requests
from bs4 import BeautifulSoup
import googlemaps
from datetime import datetime
from pandas import DataFrame, Series

def getCities(nbCities):
	
	url = requests.get('http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/')
	soup = BeautifulSoup(url.text,'html.parser')
	tab = soup.find_all('tr')
	cities = []
	for el in range(1,nbCities + 1):
		cities.append(tab[el].find_all('td')[1].text.replace('\n','').strip())
	return cities


cities = getCities(10)
print(cities)

gmaps = googlemaps.Client(key='AIzaSyCGsmB_h2JBdl1XKL-5Ky_ipCbmkyXh_Sk')

distances = gmaps.distance_matrix(cities,cities)['rows']

clean_distances = []
for row in distances:
	clean_distances.append(map(lambda x:x['distance']['text'],row['elements']))


df = DataFrame(clean_distances,index=cities,columns=cities)
print(df)


