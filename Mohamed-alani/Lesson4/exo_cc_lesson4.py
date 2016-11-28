import requests
from bs4 import BeautifulSoup
import pandas as pd

urlVille = "http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"
resultats = requests.get(urlVille)
soup_villes = BeautifulSoup(resultats.text, 'html.parser')


villes30 = []
for i in range(30):
    villes30.append(soup_villes.findAll("tr")[i+1].findAll("td")[1].text.replace("\n","").replace(" ",""))

df = pd.DataFrame(index = villes30, columns = villes30)

keyGoogle = "AIzaSyDZt_js7QfeWNdYdmd3SsX3bFPUZoLDNlw"
headers = {"Authorization": "token " + keyGoogle}

for ville1 in villes30:
    for ville2 in villes30:
        try:
            url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(ville1),str(ville2))
            kk = requests.get(url, headers=headers).json()
            df[ville1][ville2]=(kk['rows'][0]['elements'][0]['distance']['text'])
        except Exception as e:
            continue

print(df)
