import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

medicament = "ibuprofene"
medicament2 = "levothyroxime"

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"

data = {
    "page": 1,
    "affliste": 0,
    "affNumero": 0,
    "isAlphabet": 0,
    "inClauseSubst": 0,
    "nomSubstances": "",
    "typeRecherche": 0,
    "choixRecherche": "medicament",
    "paginationUsed": 0,
    "txtCaracteres": "ibuprofene",
    "btnMedic.x": 0,
    "btnMedic.y": 0,
    "btnMedic": "Rechercher",
    "radLibelle": 2,
    "txtCaracteresSub": "",
    "radLibelleSub": 4
}

request = requests.post(url, data=data)
soup = BeautifulSoup(request.text, "html.parser")

lignes = soup.find("table", {"class": "tablealigncenter"}).find_all(
    "tr", recursive=False)[3].td.table.find_all("tr", recursive=False)

df = pd.DataFrame()
for ligne in lignes[1:]:
    info_ligne = ligne.find("a").string
    print(info_ligne)
    print(len(info_ligne.split(" ")))
