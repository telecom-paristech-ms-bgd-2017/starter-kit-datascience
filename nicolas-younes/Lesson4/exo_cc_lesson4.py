import googlemaps
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd

url = "http://www.toutes-les-villes.com/villes-population.html"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
list_tr = soup.find_all("a")
print(list_tr[2].text)

gmaps = googlemaps.Client(key="AIzaSyC0DqQvDskkEJxeD7ZiFGDZLzNunPJDywY")

list_city_temp = pd.read_csv("villes_france.csv")
list_city = list_city_temp[["nom", "population"]]
sorted_list_city_by_pop = list_city.sort(["population"], ascending=False)

now = datetime.now()
n = 30
reduced_list_city = list(sorted_list_city_by_pop["nom"][0:n])
print(reduced_list_city)

i = 0
j = 0
results = np.zeros([n, n])
for c1 in reduced_list_city:
    j = 0
    for c2 in reduced_list_city:
        results[j, i] = round(gmaps.distance_matrix(str(c1), str(c2))["rows"][0]["elements"][0]["distance"]["value"] / 1000, 2)
        j += 1
    i += 1

print(results)

