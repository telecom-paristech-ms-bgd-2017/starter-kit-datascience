
from bs4 import BeautifulSoup
import requests


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



url = "http://base-donnees-publique.medicaments.gouv.fr/index.php/"

params = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0, 'inClauseSubst': 0,
          'typeRecherche': 0, 'choixRecherche': 'medicament', 'txtCaracteres': 'ibuprofene'}

res = requests.post(url, data=params)
soup = BeautifulSoup(res.text)

cells = soup.find_all('td', {'class' : 'ResultRowDeno'})

listeName = []
listeName2 = []
listeDosage = []
listeType = []
listeUnite=[]
result=[]

for cell in cells:
    res = cell.find('a' , {'class' : 'standart'}).text
    tokens = (re.findall(r'(.*)\s(\d{1,4})\s(mg?)(?:\/\d+ mg?)?\s?(.*),\s(\S*)\s(\S*)', res))

    if len(tokens) > 0 and len(tokens[0]) >= 3:
            
            listeName.append(tokens[0][0])
            listeName2.append(tokens[0][3].strip())
            listeDosage.append((tokens[0][1]))
            listeUnite.append(tokens[0][2])
            listeType.append(tokens[0][4].strip())
       
df =  pd.DataFrame([listeName,listeName2,listeDosage,listeUnite,listeType], index=['nom','nom2','dosage', 'quantité', 'Type'] )
#print(df.head(10))
print(df)
