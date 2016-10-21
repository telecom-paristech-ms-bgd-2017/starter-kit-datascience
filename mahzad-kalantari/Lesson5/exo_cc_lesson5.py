
from bs4 import BeautifulSoup
import requests


import requests
from bs4 import BeautifulSoup
import re




url = "http://base-donnees-publique.medicaments.gouv.fr/index.php/"

params = {'page': 1, 'affliste': 0, 'affNumero': 0, 'isAlphabet': 0, 'inClauseSubst': 0,
          'typeRecherche': 0, 'choixRecherche': 'medicament', 'txtCaracteres': 'ibuprofene'}



res = requests.post(url, data=params)
soup = BeautifulSoup(res.text)

cells = soup.find_all('td', {'class' : 'ResultRowDeno'})

listeName = []
listeGr = []
listeType = []
for cell in cells:
    res = cell.find('a' , {'class' : 'standart'}).text
    dose = (re.findall('[0-9]{3,4}', res))
    print(dose)
